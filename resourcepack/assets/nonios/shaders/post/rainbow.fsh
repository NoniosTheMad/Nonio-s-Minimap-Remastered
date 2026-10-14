#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:rainbow - colour layer: hue cycling with a ripple moving outward from
// the centre, boosted saturation. (Was the colour half of the old acid.)
// GameTime runs 0..1 every 20 real minutes; periodic terms use whole cycles.

uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform RainbowConfig {
    float HueCycles;    // full hue turns per 20 min (240 = one every 5 s)
    float Saturation;   // saturation multiplier
    float HueMix;       // 0 = original colours, 1 = fully shifted
    float Ripple;       // hue offset of the outward ripple
};

layout(location = 0) out vec4 fragColor;

const float TAU = 6.28318530718;

vec3 rgb2hsv(vec3 c) {
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void main() {
    vec3 color = texture(InSampler, texCoord).rgb;
    vec3 hsv = rgb2hsv(color);
    float ripple = Ripple * sin(length(texCoord - 0.5) * 18.0 - GameTime * TAU * 600.0);
    hsv.x = fract(hsv.x + fract(GameTime * floor(HueCycles)) + ripple);
    hsv.y = clamp(hsv.y * Saturation + 0.15, 0.0, 1.0);
    fragColor = vec4(mix(color, hsv2rgb(hsv), HueMix), 1.0);
}
