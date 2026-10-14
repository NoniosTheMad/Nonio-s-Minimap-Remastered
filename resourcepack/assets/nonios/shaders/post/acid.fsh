#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:acid - hue cycling, wavy UVs, chromatic aberration.
// Time: Globals.GameTime = ((worldTicks % 24000) + partialTick) / 24000, i.e. it
// runs 0..1 every 20 real minutes (1 unit = 1200 s). Every periodic term below
// uses a whole number of cycles per unit so the 20-minute wrap is seamless.

uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform AcidConfig {
    float WaveAmplitude;   // UV offset, fraction of the screen
    float WaveFrequency;   // waves across the screen (radians per unit UV)
    float Aberration;      // RGB split, fraction of the screen at the corners
    float HueCycles;       // full hue turns per 20 min (240 = one every 5 s)
    float Saturation;      // saturation multiplier
    float HueMix;          // 0 = original colours, 1 = fully shifted
};

layout(location = 0) out vec4 fragColor;

const float TAU = 6.28318530718;

float phase(float cyclesPer20Min) {
    return GameTime * TAU * cyclesPer20Min;
}

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
    // Zoom in slightly so the wobble never samples past the screen edge.
    float margin = WaveAmplitude + Aberration;
    vec2 uv = 0.5 + (texCoord - 0.5) * (1.0 - 2.0 * margin);

    // Wavy distortion: two crossing travelling waves (~0.3 Hz and ~0.25 Hz).
    uv.x += sin(uv.y * WaveFrequency + phase(360.0)) * WaveAmplitude;
    uv.y += cos(uv.x * WaveFrequency * 0.8 + phase(300.0)) * WaveAmplitude;

    // Chromatic aberration: split R/B radially, pulsing (~0.4 Hz).
    vec2 fromCenter = texCoord - 0.5;
    float pulse = 0.6 + 0.4 * sin(phase(480.0));
    vec2 split = fromCenter * Aberration * 2.0 * pulse;
    float r = texture(InSampler, uv + split).r;
    float g = texture(InSampler, uv).g;
    float b = texture(InSampler, uv - split).b;
    vec3 color = vec3(r, g, b);

    // Hue cycling: global rotation + a ripple that moves outward from the centre.
    vec3 hsv = rgb2hsv(color);
    float ripple = 0.12 * sin(length(fromCenter) * 18.0 - phase(600.0));
    hsv.x = fract(hsv.x + fract(GameTime * floor(HueCycles)) + ripple);
    hsv.y = clamp(hsv.y * Saturation + 0.15, 0.0, 1.0);
    vec3 shifted = hsv2rgb(hsv);

    fragColor = vec4(mix(color, shifted, HueMix), 1.0);
}
