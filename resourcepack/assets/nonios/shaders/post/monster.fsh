#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:monster - "Hunger" vision for the monster class.
// Blood-red monochrome; close things are sharp and bright, far things sink
// into murk (a predator's short range); silhouettes of anything nearby get a
// hot red rim; a heartbeat throbs through a barrel warp, colour split and
// pulsing dark vignette.

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform MonsterConfig {
    vec4 BloodColor;      // mid tones
    vec4 MurkColor;       // shadows and far distance
    vec4 HotColor;        // highlights and rims
    float Range;          // blocks that stay clear
    float Barrel;         // lens warp
    float Aberration;
    float RimStrength;
    float Vignette;
    float Pulse;          // heartbeat depth (0 = steady)
    float Near;           // camera near plane in blocks
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);
const float TAU = 6.28318530718;

float invDepth(vec2 uv) {
    float d = texture(DepthSampler, uv).r;
    return mix(1.0 - d, d, DepthReversed);
}

void main() {
    // heartbeat: double thump ~1 Hz (1200 cycles per 20 min)
    float t = fract(GameTime * 1200.0);
    float beat = exp(-pow((t - 0.10) * 22.0, 2.0)) + 0.6 * exp(-pow((t - 0.32) * 22.0, 2.0));
    float throb = 1.0 + Pulse * beat;

    // barrel warp, scaled so the corners stay on screen
    vec2 p = texCoord - 0.5;
    float r2 = dot(p, p);
    float k = Barrel * throb;
    vec2 uv = 0.5 + p * (1.0 + k * r2) / (1.0 + k * 0.5);

    // radial colour split
    vec2 split = p * Aberration * throb;
    vec3 c = vec3(texture(InSampler, uv + split).r,
                  texture(InSampler, uv).g,
                  texture(InSampler, uv - split).b);
    float l = dot(c, Luma);

    // distance: close = clear, far = murk
    vec2 px = 1.0 / InSize;
    float z = invDepth(uv);
    float isSky = 1.0 - step(1e-6, z);
    float dist = Near / max(z, 1e-6);
    float near = (1.0 - smoothstep(Range * 0.4, Range, dist)) * (1.0 - isSky);

    vec3 col = mix(MurkColor.rgb, BloodColor.rgb, smoothstep(0.0, 0.6, l));
    col = mix(col, HotColor.rgb, smoothstep(0.6, 1.0, l));
    col = mix(MurkColor.rgb * (0.6 + 0.4 * l), col, max(near, 0.25 * isSky));

    // hot rims on nearby silhouettes (depth second difference, like reaper)
    float lap = abs(invDepth(uv - vec2(px.x, 0.0)) + invDepth(uv + vec2(px.x, 0.0)) - 2.0 * z)
              + abs(invDepth(uv - vec2(0.0, px.y)) + invDepth(uv + vec2(0.0, px.y)) - 2.0 * z);
    float rim = smoothstep(1.0, 2.0, lap / max(z, 1e-6) * 60.0) * near;
    col = mix(col, HotColor.rgb, rim * RimStrength * (0.7 + 0.3 * beat));

    // pulsing vignette
    float v = smoothstep(0.25, 0.75, length(p) * (1.0 + 0.15 * beat));
    col *= 1.0 - Vignette * v;

    fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}
