#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:madness - the Hunger takes the mind (monster class at low HP).
// Intensity (0..1, one JSON per HP tier) drives everything:
//  - ink tendrils creep in from the screen edges and writhe (ridged noise flowing inward),
//  - watchers: dark shapes with pale eyes appear in the periphery, a new set every ~6 s,
//  - colour bleeds: reds drip downward, channels smear apart,
//  - the view breathes in sync with the monster heartbeat (same 20-tick period).

uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform MadnessConfig {
    vec4 InkColor;
    vec4 EyeColor;
    float Intensity;
    float Tendrils;
    float Watchers;
    float Bleed;
    float Breath;
};

layout(location = 0) out vec4 fragColor;

const float TAU = 6.28318530718;

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

void main() {
    float I = clamp(Intensity, 0.0, 1.0);
    vec2 aspect = vec2(InSize.x / InSize.y, 1.0);
    vec2 q = (texCoord - 0.5) * aspect;
    float r = length(q);
    vec2 dir = q / max(r, 1e-4);
    float t = GameTime * TAU;

    // heartbeat, same timing as nonios:monster (1200 cycles / 24000 ticks = every 20 ticks)
    float ph = fract(GameTime * 1200.0);
    float beat = exp(-pow((ph - 0.10) * 22.0, 2.0)) + 0.6 * exp(-pow((ph - 0.32) * 22.0, 2.0));

    // breathing + slow swirl toward the edges
    float sw = r * r * I * 0.25 * sin(t * 37.0);
    vec2 rq = mat2(cos(sw), -sin(sw), sin(sw), cos(sw)) * q;
    rq *= 1.0 - Breath * I * 0.02 * beat;
    vec2 uv = rq / aspect + 0.5;

    // colour bleed: drips + channel smear
    float drip = noise(vec2(uv.x * 60.0, t * 40.0)) * noise(vec2(uv.x * 13.0, 3.0));
    vec2 dUv = vec2(0.0, drip * Bleed * I * 0.03);
    vec2 smear = dir * Bleed * I * 0.006 * (0.6 + 0.4 * noise(vec2(t * 120.0, r * 8.0)));
    vec3 c;
    c.r = texture(InSampler, uv + dUv + smear).r;
    c.g = texture(InSampler, uv + dUv * 0.3).g;
    c.b = texture(InSampler, uv - smear).b;
    c = mix(c, c * vec3(1.15, 0.85, 0.85), I * 0.5);

    // tendrils: inward-flowing ridged noise around the edge
    float rid = ridged(dir * 3.0 + vec2(r * 4.0 - t * 30.0, t * 7.0));
    float reach = mix(0.95, 0.38, I * Tendrils);
    float ink = smoothstep(reach + 0.05, reach + 0.32, r + rid * 0.28 * (0.6 + 0.4 * I));
    ink = max(ink, smoothstep(0.55, 0.95, rid) * smoothstep(reach - 0.05, reach + 0.25, r) * 0.8);
    vec3 col = mix(c, InkColor.rgb, clamp(ink, 0.0, 1.0));

    // watchers: 3 slots, new positions every 120 ticks (200 cycles / 24000)
    float slotT = GameTime * 200.0;
    float slot = floor(slotT);
    float life = sin(fract(slotT) * 3.14159);
    for (int i = 0; i < 3; i++) {
        float h = hash(vec2(slot, float(i) * 7.3));
        if (h > I * Watchers) continue;
        float a = hash(vec2(slot * 1.3, float(i))) * TAU;
        float rr = mix(0.38, 0.5, hash(vec2(float(i), slot * 0.7)));
        vec2 c0 = vec2(cos(a), sin(a)) * rr * vec2(aspect.x * 0.9, 1.0);
        vec2 d = q - c0;
        // tall shadow body
        vec2 bd = d * vec2(9.0, 4.0);
        float body = exp(-dot(bd, bd));
        col = mix(col, InkColor.rgb, body * life * 0.85);
        // two eyes, blinking
        float blink = step(0.08, fract(slotT * 3.0 + h * 5.0));
        vec2 e1 = d - vec2(-0.012, 0.03);
        vec2 e2 = d - vec2(0.012, 0.03);
        float eyes = exp(-dot(e1, e1) * 30000.0) + exp(-dot(e2, e2) * 30000.0);
        float eyeGlow = exp(-dot(e1, e1) * 2500.0) + exp(-dot(e2, e2) * 2500.0);
        col += EyeColor.rgb * (eyes + eyeGlow * 0.25) * life * blink;
    }

    // the whole frame darkens slightly with each beat at high madness
    col *= 1.0 - 0.25 * I * beat;
    fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}
