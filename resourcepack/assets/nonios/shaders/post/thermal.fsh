#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:thermal, final pass - infrared camera.
// Heat comes from pass 1 (markers written by the demo overlay core shaders): living things, lava, fire,
// magma, torches and other lights glow white / yellow / red, their surroundings warm up, and the rest of
// the world is a cold dark blue-violet with faint depth edges so it stays readable. Hot things bloom.

uniform sampler2D InSampler;
uniform sampler2D HeatSampler;
uniform sampler2D GlowSampler;
uniform sampler2D WideSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform ThermalConfig {
    vec4 ColdDark;       // coldest colour
    vec4 ColdLight;      // brightest cold colour
    vec4 EdgeColor;      // depth edges
    float ColdGamma;
    float HeatStart;     // heat where the hot palette takes over
    float GlowStrength;
    float WideStrength;
    float EdgeStrength;
    float Grain;
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);

// hot palette: violet -> red -> orange -> yellow -> white
vec3 hot(float t) {
    t = clamp(t, 0.0, 1.0) * 4.0;
    vec3 c0 = vec3(0.30, 0.03, 0.40);
    vec3 c1 = vec3(0.86, 0.08, 0.14);
    vec3 c2 = vec3(1.00, 0.46, 0.04);
    vec3 c3 = vec3(1.00, 0.86, 0.22);
    vec3 c4 = vec3(1.00, 1.00, 0.93);
    if (t < 1.0) return mix(c0, c1, t);
    if (t < 2.0) return mix(c1, c2, t - 1.0);
    if (t < 3.0) return mix(c2, c3, t - 2.0);
    return mix(c3, c4, t - 3.0);
}

float invDepth(vec2 uv) {
    float d = texture(DepthSampler, uv).r;
    return mix(1.0 - d, d, DepthReversed);
}

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
    vec2 px = 1.0 / InSize;
    vec3 c = texture(InSampler, texCoord).rgb;
    float l = dot(c, Luma);
    vec4 h = texture(HeatSampler, texCoord);
    float heat = h.r;

    float z = invDepth(texCoord);
    float sky = 1.0 - step(1e-6, z);

    // --- cold world
    vec3 cold = mix(ColdDark.rgb, ColdLight.rgb, pow(clamp(l, 0.0, 1.0), ColdGamma));
    float lap = abs(invDepth(texCoord - vec2(px.x, 0.0)) + invDepth(texCoord + vec2(px.x, 0.0)) - 2.0 * z)
              + abs(invDepth(texCoord - vec2(0.0, px.y)) + invDepth(texCoord + vec2(0.0, px.y)) - 2.0 * z);
    float edge = smoothstep(1.0, 2.5, lap / max(z, 1e-6) * 60.0) * (1.0 - sky);
    cold += EdgeColor.rgb * edge * EdgeStrength;
    cold = mix(cold, ColdDark.rgb * 0.6, sky * (1.0 - smoothstep(0.5, 1.0, l)));

    // --- heat
    float w = smoothstep(HeatStart, HeatStart + 0.2, heat);
    vec3 col = mix(cold, hot(heat), w);

    // --- bloom around hot things
    float g = texture(GlowSampler, texCoord).g;
    float wide = texture(WideSampler, texCoord).g;
    col += hot(0.55 + 0.45 * g) * g * GlowStrength;
    col += hot(0.35 + 0.4 * wide) * wide * WideStrength;

    // --- sensor grain (changes every tick)
    col += (hash(texCoord * InSize + floor(GameTime * 24000.0)) - 0.5) * Grain;

    fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}
