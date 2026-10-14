#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:madness v2 - the Hunger takes the mind (monster class at low HP).
// Intensity (0..1) comes from one of ten JSONs (madness_1..10). The datapack eases the level toward
// the HP target one step at a time, so the tunnel closes and opens gradually instead of jumping.
//  - ink tunnel: ridged noise flowing inward from the screen edges,
//  - tendrils: tapering fingers reaching in from the edges, writhing,
//  - silhouettes: tall thin figures with long arms at the edge of sight, swaying, smoking away,
//  - faces in the dark: pale hollow-eyed faces that surface only where the image is dark,
//  - colour bleed (reds drip, channels smear) and a slow drifting warp of the whole view,
//  - the view breathes with the monster heartbeat (same 20-tick period).

uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform MadnessConfig {
    vec4 InkColor;
    vec4 FaceColor;
    float Intensity;
    float Tendrils;
    float Watchers;   // silhouettes and faces
    float Bleed;
    float Breath;
    float Drift;      // slow drifting warp
};

layout(location = 0) out vec4 fragColor;

const float TAU = 6.28318530718;
const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), f.x),
               mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), f.x), f.y);
}

float ridged(vec2 p) {
    float s = 0.0;
    float a = 0.5;
    for (int i = 0; i < 4; i++) {
        s += a * (1.0 - abs(noise(p) * 2.0 - 1.0));
        p = p * 2.03 + vec2(1.7, 9.2);
        a *= 0.5;
    }
    return s;
}

float capsule(vec2 p, vec2 a, vec2 b, float r) {
    vec2 pa = p - a;
    vec2 ba = b - a;
    float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0);
    return length(pa - ba * h) - r;
}

// a tall thin figure, feet at the origin, height 1
float figure(vec2 p, float sway) {
    p.x -= sway * p.y * p.y;
    float d = length((p - vec2(0.0, 0.9)) * vec2(1.0, 0.85)) - 0.07;
    d = min(d, capsule(p, vec2(0.0, 0.8), vec2(0.0, 0.42), 0.055));
    d = min(d, capsule(p, vec2(-0.025, 0.42), vec2(-0.045, 0.0), 0.022));
    d = min(d, capsule(p, vec2(0.025, 0.42), vec2(0.05, 0.0), 0.022));
    // arms hang past the knees
    d = min(d, capsule(p, vec2(-0.06, 0.76), vec2(-0.12 - sway * 0.3, 0.16), 0.016));
    d = min(d, capsule(p, vec2(0.06, 0.76), vec2(0.11 - sway * 0.3, 0.14), 0.016));
    return d;
}

// a pale face with hollow eyes and a long open mouth; returns (mask, shade)
vec2 face(vec2 f, float open) {
    float head = length(f * vec2(1.0, 0.76)) - 0.5;
    float mask = 1.0 - smoothstep(-0.08, 0.04, head);
    vec2 e1 = (f - vec2(-0.17, 0.08)) * vec2(1.0, 1.35);
    vec2 e2 = (f - vec2(0.17, 0.08)) * vec2(1.0, 1.35);
    float eyes = 1.0 - smoothstep(0.07, 0.13, min(length(e1), length(e2)));
    vec2 m = (f - vec2(0.0, -0.27)) / vec2(0.15, 0.03 + 0.09 * open);
    float mouth = 1.0 - smoothstep(0.7, 1.1, length(m));
    float shade = 0.75 + 0.25 * f.y - 0.9 * max(eyes, mouth);
    return vec2(mask, clamp(shade, 0.0, 1.0));
}

void main() {
    float I = clamp(Intensity, 0.0, 1.0);
    vec2 aspect = vec2(InSize.x / InSize.y, 1.0);
    vec2 q = (texCoord - 0.5) * aspect;
    float r = length(q);
    vec2 dir = q / max(r, 1e-4);
    float t = GameTime * TAU;   // t * 1.0 = one turn per 20 min

    // heartbeat, same timing as nonios:monster (1200 cycles / 24000 ticks = every 20 ticks)
    float ph = fract(GameTime * 1200.0);
    float beat = exp(-pow((ph - 0.10) * 22.0, 2.0)) + 0.6 * exp(-pow((ph - 0.32) * 22.0, 2.0));

    // slow drifting warp: a low-frequency flow field that changes over ~20-40 s, stronger at the edges
    vec2 flow = vec2(noise(q * 2.2 + vec2(t * 45.0, t * 23.0)),
                     noise(q * 2.2 + vec2(-t * 31.0, t * 52.0) + 17.0)) - 0.5;
    vec2 wq = q + flow * Drift * I * (0.012 + 0.03 * r * r);
    // breathing + a slowly turning swirl toward the edges
    float sw = r * r * I * 0.22 * sin(t * 37.0 + noise(vec2(t * 20.0, 3.0)) * 2.0);
    vec2 rq = mat2(cos(sw), -sin(sw), sin(sw), cos(sw)) * wq;
    rq *= 1.0 - Breath * I * 0.02 * beat;
    vec2 uv = rq / aspect + 0.5;

    // colour bleed: drips + a channel smear whose direction drifts
    float drip = noise(vec2(uv.x * 60.0, t * 40.0)) * noise(vec2(uv.x * 13.0, 3.0 + t * 8.0));
    vec2 dUv = vec2(0.0, drip * Bleed * I * 0.03);
    float sa = t * 25.0 + noise(vec2(t * 15.0, 1.0)) * TAU;
    vec2 sdir = normalize(dir + 0.6 * vec2(cos(sa), sin(sa)));
    vec2 smear = sdir * Bleed * I * 0.006 * (0.6 + 0.4 * noise(vec2(t * 120.0, r * 8.0)));
    vec3 c;
    c.r = texture(InSampler, uv + dUv + smear).r;
    c.g = texture(InSampler, uv + dUv * 0.3).g;
    c.b = texture(InSampler, uv - smear).b;
    c = mix(c, c * vec3(1.15, 0.85, 0.85), I * 0.5);
    float lum = dot(c, Luma);

    // ink tunnel
    float rid = ridged(dir * 3.0 + vec2(r * 4.0 - t * 30.0, t * 7.0));
    float reach = mix(0.95, 0.38, I * Tendrils);
    float ink = smoothstep(reach + 0.05, reach + 0.32, r + rid * 0.28 * (0.6 + 0.4 * I));
    ink = max(ink, smoothstep(0.55, 0.95, rid) * smoothstep(reach - 0.05, reach + 0.25, r) * 0.8);

    // tendrils: tapering fingers from the edge, writhing (more and longer with intensity)
    float ang = atan(q.y, q.x);
    for (int i = 0; i < 6; i++) {
        float fi = float(i);
        float h = hash(vec2(fi, 4.7));
        if (h > 0.2 + 0.8 * I * Tendrils) continue;
        float tip = mix(0.9, 0.32, I * Tendrils) + 0.07 * sin(t * (11.0 + fi * 3.0) + h * TAU);
        float a0 = fi / 6.0 * TAU + h * 0.8 + 0.25 * sin(t * 6.0 + fi);
        float a = a0 + 0.22 * sin(r * 9.0 - t * (40.0 + h * 30.0) + fi * 2.0) * (r - tip);
        float da = abs(mod(ang - a + 3.14159, TAU) - 3.14159) * r;
        float w = 0.035 * clamp((r - tip) / 0.35, 0.0, 1.0);
        ink = max(ink, (1.0 - smoothstep(w * 0.5, w, da)) * step(tip, r));
    }
    vec3 col = mix(c, InkColor.rgb, clamp(ink, 0.0, 1.0));

    // silhouettes / faces: 3 slots, a new set every 120 ticks (200 cycles / 24000)
    float slotT = GameTime * 200.0;
    float slot = floor(slotT);
    float life = smoothstep(0.0, 0.35, fract(slotT)) * (1.0 - smoothstep(0.65, 1.0, fract(slotT)));
    for (int i = 0; i < 3; i++) {
        float fi = float(i);
        float h = hash(vec2(slot, fi * 7.3));
        if (h > I * Watchers) continue;
        float kind = hash(vec2(slot * 0.37, fi + 2.0));
        float side = hash(vec2(slot * 1.3, fi)) < 0.5 ? -1.0 : 1.0;
        if (kind < 0.55) {
            // a figure standing at the edge of sight
            float x = side * mix(0.48, 0.8, hash(vec2(fi, slot * 0.7))) * aspect.x;
            float ht = mix(0.32, 0.55, hash(vec2(slot, fi + 9.0)));
            vec2 p = (q - vec2(x, mix(-0.32, -0.12, hash(vec2(fi + 3.0, slot))))) / ht;
            float sway = 0.12 * sin(t * (9.0 + fi * 4.0) + h * TAU);
            float d = figure(p, sway) * ht;
            d += (noise(p * 18.0 + vec2(0.0, t * 60.0)) - 0.5) * 0.012;
            float m = 1.0 - smoothstep(-0.004, 0.006, d);
            col = mix(col, InkColor.rgb, m * life * 0.9);
        } else {
            // a face surfacing where it is dark
            vec2 c0 = vec2(side * mix(0.15, 0.6, hash(vec2(fi, slot * 0.9))) * aspect.x,
                           mix(-0.3, 0.3, hash(vec2(slot, fi + 5.0))));
            float sz = mix(0.12, 0.22, hash(vec2(fi + 1.0, slot * 1.7)));
            vec2 f = (q - c0) / sz;
            f.x += 0.04 * sin(f.y * 6.0 + t * 30.0);
            vec2 fm = face(f, 0.5 + 0.5 * sin(t * 18.0 + h * TAU));
            float dark = 1.0 - smoothstep(0.05, 0.25, lum);
            float mottle = 0.8 + 0.4 * noise(f * 9.0 + 3.0);
            col = mix(col, FaceColor.rgb * fm.y * mottle, fm.x * dark * life * 0.45 * (0.5 + 0.5 * I));
        }
    }

    // the whole frame darkens slightly with each beat at high madness
    col *= 1.0 - 0.25 * I * beat;
    fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}
