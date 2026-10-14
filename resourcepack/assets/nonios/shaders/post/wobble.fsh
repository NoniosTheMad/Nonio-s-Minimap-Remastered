#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:wobble - distortion layer: wavy UVs + pulsing chromatic aberration.
// (The colour cycling moved to nonios:rainbow; "Cracy Frog" = wobble + rainbow.)
// Time: Globals.GameTime = ((worldTicks % 24000) + partialTick) / 24000, i.e. it
// runs 0..1 every 20 real minutes (1 unit = 1200 s). Every periodic term below
// uses a whole number of cycles per unit so the 20-minute wrap is seamless.

uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform WobbleConfig {
    float WaveAmplitude;   // UV offset, fraction of the screen
    float WaveFrequency;   // waves across the screen (radians per unit UV)
    float Aberration;      // RGB split, fraction of the screen at the corners
};

layout(location = 0) out vec4 fragColor;

const float TAU = 6.28318530718;

float phase(float cyclesPer20Min) {
    return GameTime * TAU * cyclesPer20Min;
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

    fragColor = vec4(r, g, b, 1.0);
}
