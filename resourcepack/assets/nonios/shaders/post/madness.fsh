#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:madness v3 - the Hunger takes the mind (monster class at low HP).
// Intensity (0..1) comes from one of ten JSONs (madness_1..10). The datapack eases the level toward
// the HP target one step at a time, so the darkness closes and opens gradually instead of jumping.
// v3 (#66): no figures or faces. Built in tools/shaderlab first (reference: demos/shaders/reference/monster.gif).
//  - the tunnel is an ellipse fitted to the screen (Ellipse: 0 = circle, 1 = screen shape),
//  - creeping darkness: the edge is a domain-warped fbm field, like ink spreading in water, with a
//    blood-red glow where the ink meets the image,
//  - tendrils: ridged noise in log-polar space (so they taper toward their tips and branch), crawling
//    inward from the ink,
//  - veins: voronoi cracks under the ink's edge that flush red with each heartbeat,
//  - radial chromatic smear, desaturation and a red grade toward the edge; the view breathes with the
//    heartbeat (same 20-tick period as nonios:monster) and drifts slowly.

uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform MadnessConfig {
    vec4 InkColor;
    vec4 VeinColor;
    float Intensity;
    float Tendrils;
    float Veins;
    float Bleed;      // chromatic smear + red grade
    float Breath;
    float Drift;      // slow drifting warp
    float Ellipse;    // 0 circle .. 1 ellipse with the screen's aspect
};

layout(location = 0) out vec4 fragColor;

const float TAU = 6.28318530718;
const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float hash3(vec3 p) {
    p = fract(p * 0.1031);
    p += dot(p, p.zyx + 31.32);
    return fract((p.x + p.y) * p.z);
}

float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), f.x),
               mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), f.x), f.y);
}

float noise3(vec3 p) {
    vec3 i = floor(p);
    vec3 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    float a = mix(mix(hash3(i), hash3(i + vec3(1, 0, 0)), f.x), mix(hash3(i + vec3(0, 1, 0)), hash3(i + vec3(1, 1, 0)), f.x), f.y);
    float b = mix(mix(hash3(i + vec3(0, 0, 1)), hash3(i + vec3(1, 0, 1)), f.x), mix(hash3(i + vec3(0, 1, 1)), hash3(i + vec3(1, 1, 1)), f.x), f.y);
    return mix(a, b, f.z);
}

float fbm(vec2 p) {
    float s = 0.0;
    float a = 0.5;
    for (int i = 0; i < 5; i++) {
        s += a * noise(p);
        p = mat2(1.6, 1.2, -1.2, 1.6) * p + vec2(3.1, 1.7);
        a *= 0.5;
    }
    return s / 0.97;
}

// ridged noise in 3D (lines where the noise crosses 0.5)
float ridged3(vec3 p) {
    float s = 0.0;
    float a = 0.6;
    for (int i = 0; i < 3; i++) {
        float n = 1.0 - abs(noise3(p) * 2.0 - 1.0);
        s = max(s, pow(n, 6.0) * a / 0.6);
        p = p * 2.1 + vec3(5.2, 1.3, 2.8);
        a *= 0.7;
    }
    return s;
}

// voronoi: distance to the nearest cell border (F2 - F1)
float cracks(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    float f1 = 8.0;
    float f2 = 8.0;
    for (int y = -1; y <= 1; y++)
    for (int x = -1; x <= 1; x++) {
        vec2 g = vec2(x, y);
        vec2 o = vec2(hash(i + g), hash(i + g + 17.3));
        float d = length(g + o - f);
        if (d < f1) { f2 = f1; f1 = d; } else if (d < f2) { f2 = d; }
    }
    return f2 - f1;
}

void main() {
    float I = clamp(Intensity, 0.0, 1.0);
    float A = InSize.x / InSize.y;
    float t = GameTime * TAU;   // one turn per 20 min

    // heartbeat, same timing as nonios:monster (every 20 ticks)
    float ph = fract(GameTime * 1200.0);
    float beat = exp(-pow((ph - 0.10) * 22.0, 2.0)) + 0.6 * exp(-pow((ph - 0.32) * 22.0, 2.0));

    // circle space (height units) for the image warp, tunnel space for the darkness
    vec2 q = (texCoord - 0.5) * vec2(A, 1.0);
    vec2 e = (texCoord - 0.5) * 2.0 * vec2(A / mix(1.0, A, Ellipse), 1.0);   // 1 = edge midpoints
    float r = length(e);
    float ang = atan(e.y, e.x);

    // slow drifting warp + breathing
    vec2 flow = vec2(noise(q * 2.2 + vec2(t * 45.0, t * 23.0)), noise(q * 2.2 + vec2(-t * 31.0, t * 52.0) + 17.0)) - 0.5;
    vec2 wq = q + flow * Drift * I * (0.01 + 0.025 * r * r);
    wq *= 1.0 - Breath * I * 0.018 * beat;
    vec2 uv = wq / vec2(A, 1.0) + 0.5;

    // radial chromatic smear, grows toward the edge
    vec2 rad = (uv - 0.5) * Bleed * I * 0.02 * r * r;
    vec3 c;
    c.r = texture(InSampler, uv + rad).r;
    c.g = texture(InSampler, uv).g;
    c.b = texture(InSampler, uv - rad).b;

    // --- creeping darkness: domain-warped fbm edge (ink in water)
    vec2 ep = e * 1.6;
    vec2 w1 = vec2(fbm(ep + vec2(t * 18.0, -t * 11.0)), fbm(ep + vec2(5.2, 1.3) - vec2(t * 13.0, t * 16.0)));
    float n = fbm(ep * 1.3 + w1 * 2.4 + vec2(-t * 9.0, t * 7.0));
    float reach = mix(1.5, 0.56, pow(I, 0.8));    // where the darkness starts (tunnel radius)
    float edge = r + (n - 0.5) * (0.35 + 0.3 * I) - reach;
    // soft ink: a wispy outer band (fbm detail) before the solid black
    float wisp = fbm(ep * 3.1 - w1 * 1.7 + vec2(t * 21.0, 0.0));
    float ink = smoothstep(-0.12, 0.3, edge + (wisp - 0.5) * 0.18);
    ink = ink * ink * (3.0 - 2.0 * ink);
    float rim = exp(-pow((edge + 0.06) / 0.09, 2.0));

    // --- tendrils: ridged noise in log-polar space, seamless in angle, crawling inward
    float lr = log(max(r, 0.02));
    vec3 tp = vec3(cos(ang) * 2.2, sin(ang) * 2.2, lr * 3.2 + t * 40.0) + vec3(w1 * 0.7, 0.0);
    float rid = ridged3(tp);
    float tipR = reach - mix(0.15, 0.45, I) * Tendrils;     // tendrils reach this far inside the tunnel
    float along = clamp((r - tipR) / max(reach - tipR, 0.05), 0.0, 1.0);   // 0 at the tips, 1 at the ink
    float th = mix(0.97, 0.55, along * along);               // thinner toward the tips
    float tend = smoothstep(th, th + 0.04, rid) * step(tipR, r) * Tendrils;
    ink = max(ink, tend);

    // --- veins: cracks just inside the ink edge, flushing red with each beat
    vec2 vp = e * 5.0 + w1 * 1.5;
    float cr = cracks(vp);
    float vein = (1.0 - smoothstep(0.015, 0.05, cr)) * smoothstep(-0.18, 0.0, edge) * (1.0 - smoothstep(0.1, 0.3, edge));
    vein *= Veins * (0.15 + 0.85 * beat) * smoothstep(0.15, 0.5, I) * 0.7;

    // --- grade: desaturate + red toward the edge
    float lum = dot(c, Luma);
    float toward = smoothstep(reach - 0.6, reach, r) * I;
    c = mix(c, vec3(lum) * vec3(1.1, 0.62, 0.58), toward * Bleed * 0.8);
    c = mix(c, c * vec3(1.12, 0.88, 0.88), I * 0.4);

    vec3 col = c;
    col = mix(col, col * vec3(1.3, 0.5, 0.45) + VeinColor.rgb * 0.12, rim * (0.5 + 0.3 * beat) * smoothstep(0.0, 0.3, I));
    // in the dark the ink's edge still breathes a faint blood glow, so the tunnel reads at night
    col += VeinColor.rgb * rim * (1.0 - smoothstep(0.02, 0.2, lum)) * (0.08 + 0.12 * beat) * smoothstep(0.0, 0.3, I);
    col = mix(col, InkColor.rgb, clamp(ink, 0.0, 1.0));
    col = mix(col, VeinColor.rgb * 1.2, clamp(vein, 0.0, 1.0) * (1.0 - tend));

    // the whole frame darkens slightly with each beat at high madness
    col *= 1.0 - 0.22 * I * beat;
    fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}
