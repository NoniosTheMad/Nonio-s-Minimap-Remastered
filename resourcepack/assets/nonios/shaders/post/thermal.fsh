#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:thermal v3, final pass - a FLIR-style infrared camera (ironbow palette).
// Everything becomes one continuous "temperature" T and is coloured through a single smooth palette:
//   - cold world: a dark, low-contrast gradient from the scene brightness, with soft local detail and
//     faint depth edges (like FLIR's edge overlay), cooling with distance; the sky is coldest,
//   - sources (pass 1): living things warm (orange-yellow), emitters (lava, fire, torches, glowstone)
//     and flames hottest (white),
//   - warmth around a source: the source mask blurred at two sizes, so it falls off smoothly,
//   - hand / held item: neutral,
//   - sensor noise and a little lens falloff are added to T, before the palette.

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
    float AmbientBase;    // T of a black surface
    float AmbientRange;   // T added by full scene brightness
    float Detail;         // local contrast (soft texture detail)
    float EdgeStrength;   // depth edges
    float FarCool;        // how much distance cools
    float GlowStrength;   // tight warmth around sources
    float WideStrength;   // wide warmth around sources
    float SkyTemp;
    float HandTemp;
    float Noise;
    float Vignette;
    float Near;
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);

// ironbow: black -> indigo -> purple -> magenta -> red-orange -> orange -> yellow -> white
vec3 ironbow(float t) {
    vec3 c[8] = vec3[8](
        vec3(0.00, 0.00, 0.02), vec3(0.07, 0.02, 0.28), vec3(0.33, 0.02, 0.53), vec3(0.68, 0.07, 0.50),
        vec3(0.91, 0.28, 0.20), vec3(1.00, 0.56, 0.03), vec3(1.00, 0.84, 0.24), vec3(1.00, 1.00, 0.93));
    float x = clamp(t, 0.0, 1.0) * 7.0;
    int i = int(min(floor(x), 6.0));
    float f = x - float(i);
    f = f * f * (3.0 - 2.0 * f) * 0.35 + f * 0.65;   // soften the joints between stops
    return mix(c[i], c[i + 1], f);
}

float lumAt(vec2 uv) {
    return dot(texture(InSampler, uv).rgb, Luma);
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
    float l = lumAt(texCoord);
    vec4 h = texture(HeatSampler, texCoord);
    float glow = texture(GlowSampler, texCoord).g;
    float wide = texture(WideSampler, texCoord).g;

    float z = invDepth(texCoord);
    float sky = 1.0 - step(1e-6, z);
    float dist = Near / max(z, 1e-6);

    // --- cold world: brightness -> a narrow, dark band of T; local detail kept soft
    float avg = 0.25 * (lumAt(texCoord + vec2(2.0, 0.0) * px) + lumAt(texCoord - vec2(2.0, 0.0) * px)
                      + lumAt(texCoord + vec2(0.0, 2.0) * px) + lumAt(texCoord - vec2(0.0, 2.0) * px));
    float base = AmbientBase + AmbientRange * sqrt(clamp(mix(avg, l, 0.5), 0.0, 1.0));
    base += Detail * clamp(l - avg, -0.15, 0.15);
    float lap = abs(invDepth(texCoord - vec2(px.x, 0.0)) + invDepth(texCoord + vec2(px.x, 0.0)) - 2.0 * z)
              + abs(invDepth(texCoord - vec2(0.0, px.y)) + invDepth(texCoord + vec2(0.0, px.y)) - 2.0 * z);
    base += EdgeStrength * smoothstep(1.0, 3.0, lap / max(z, 1e-6) * 60.0);
    base *= 1.0 - FarCool * smoothstep(12.0, 160.0, dist);
    float T = mix(base, SkyTemp, sky);

    // --- warmth spreading from sources, then the sources themselves
    // compressed, so a small torch still shows a halo and a lava lake does not wash everything white
    T += GlowStrength * (1.0 - exp(-4.0 * glow)) + WideStrength * (1.0 - exp(-4.0 * wide));
    T = max(T, h.r);

    // --- hand / held item: neutral
    T = mix(T, HandTemp + 0.06 * l, h.b);

    // --- sensor: noise (per tick) and lens falloff
    T += (hash(gl_FragCoord.xy + floor(GameTime * 24000.0) * vec2(7.3, 3.1)) - 0.5) * Noise;
    vec2 v = texCoord - 0.5;
    v.x *= InSize.x / InSize.y;
    T *= 1.0 - Vignette * dot(v, v);

    fragColor = vec4(ironbow(T), 1.0);
}
