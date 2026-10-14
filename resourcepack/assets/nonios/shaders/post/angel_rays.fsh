#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:angel v4, pass 2 - volumetric light shafts (screen-space radial scatter, GPU Gems 3 ch. 13 style).
// A post shader gets no sun position, so the light centre is FOUND: every pixel samples the same coarse
// grid of the heaven-light mask (alpha of pass 1, blurred) and takes the brightness^4-weighted centroid,
// so all pixels agree on it and it glides smoothly as you turn. Off-screen or no bright sky: the rays
// come from above the top of the screen, weaker ("light from heaven").
// Then each pixel marches toward the centre and gathers the mask with decay: sky seen through leaves,
// gaps and over ridges streams into soft shafts. A slow angular noise makes the shafts breathe.
// Out: r = shafts, g = light-centre glow (used for a soft sun halo), b = how much bright sky is on screen.

uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform AngelRayConfig {
    vec2 FallbackOrigin;  // uv used when no bright sky is visible (above the top centre)
    float RayLength;      // fraction of the way to the centre that is sampled
    float RayDecay;       // per-step falloff
    float Breathe;        // 0..1 slow angular modulation of the shafts
};

layout(location = 0) out vec4 fragColor;

const int STEPS = 48;
const float TAU = 6.28318530718;

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

// value noise with period P (the angle wraps around without a seam)
float vnoise(float x, float P, float seed) {
    float i = floor(x);
    float f = fract(x);
    f = f * f * (3.0 - 2.0 * f);
    return mix(hash(vec2(mod(i, P), seed)), hash(vec2(mod(i + 1.0, P), seed)), f);
}

void main() {
    // --- light centre: weighted centroid of the heaven mask on a 16 x 9 grid
    vec2 acc = vec2(0.0);
    float wsum = 0.0;
    float area = 0.0;
    for (int y = 0; y < 9; y++) {
        for (int x = 0; x < 16; x++) {
            vec2 uv = (vec2(x, y) + 0.5) / vec2(16.0, 9.0);
            float m = texture(InSampler, uv).a;
            float w = m * m * m * m;
            acc += uv * w;
            wsum += w;
            area += m;
        }
    }
    area /= 144.0;
    float found = smoothstep(0.0005, 0.004, wsum / 144.0);
    vec2 origin = mix(FallbackOrigin, acc / max(wsum, 1e-6), found);

    // --- radial march toward the centre
    vec2 delta = (origin - texCoord) * RayLength / float(STEPS);
    vec2 uv = texCoord + delta * hash(texCoord * InSize + fract(GameTime * 977.0));
    float weight = 1.0;
    float total = 0.0;
    float norm = 0.0;
    for (int i = 0; i < STEPS; i++) {
        vec2 q = clamp(uv, vec2(0.0), vec2(1.0));
        total += texture(InSampler, q).a * weight;
        norm += weight;
        weight *= RayDecay;
        uv += delta;
    }
    float shafts = total / norm;

    // slow breathing along the angle around the centre (shafts drift and shimmer gently)
    vec2 aspect = vec2(InSize.x / InSize.y, 1.0);
    vec2 r = (texCoord - origin) * aspect;
    float ang = atan(r.y, r.x) / TAU + 0.5;    // 0..1 around the centre
    float t = GameTime * 1200.0;               // seconds
    // the noise drifts in time, not along the angle, so the wrap stays seamless
    float n = 0.5 * vnoise(ang * 24.0, 24.0, floor(t * 0.15)) * (1.0 - fract(t * 0.15)) + 0.5 * vnoise(ang * 24.0, 24.0, floor(t * 0.15) + 1.0) * fract(t * 0.15)
            + 0.5 * vnoise(ang * 40.0, 40.0, 7.0 + floor(t * 0.1)) * (1.0 - fract(t * 0.1)) + 0.5 * vnoise(ang * 40.0, 40.0, 8.0 + floor(t * 0.1)) * fract(t * 0.1);
    float br = 0.45 + 0.9 * n * 0.5 + 0.1;
    shafts *= mix(1.0, br, Breathe);

    // soft glow around the light centre (works off screen too)
    float glow = exp(-length(r) * 3.0) * found;

    fragColor = vec4(shafts, glow, area, 1.0);
}
