#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:neon, final pass - a grey, dimmed world with neon tubes on every edge.
// Tubes: hot white-ish core + the edge's own saturated colour + a wide glow, with a
// faint mains hum flicker.

uniform sampler2D InSampler;
uniform sampler2D EdgeSampler;
uniform sampler2D GlowSampler;
uniform sampler2D WideSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform NeonConfig {
    float Dim;           // brightness of the grey world
    float Saturation;    // colour left in the world (0 = grey)
    float CoreStrength;
    float CoreWhite;     // how white the tube core gets
    float GlowStrength;
    float WideStrength;
    float Hum;           // flicker amount
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);
const float TAU = 6.28318530718;

void main() {
    vec3 c = texture(InSampler, texCoord).rgb;
    float l = dot(c, Luma);
    vec3 world = mix(vec3(l), c, Saturation) * Dim;

    vec4 e = texture(EdgeSampler, texCoord);
    vec3 glow = texture(GlowSampler, texCoord).rgb;
    vec3 wide = texture(WideSampler, texCoord).rgb;

    float hum = 1.0 - Hum * (0.5 + 0.5 * sin(GameTime * TAU * 2400.0)) * (0.5 + 0.5 * sin(GameTime * TAU * 170.0));

    vec3 core = mix(e.rgb, vec3(1.0) * e.a, CoreWhite * e.a) * CoreStrength;
    vec3 col = world + (core + glow * GlowStrength + wide * WideStrength) * hum;
    col = col / (1.0 + max(col - 1.0, 0.0) * 0.6);
    fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}
