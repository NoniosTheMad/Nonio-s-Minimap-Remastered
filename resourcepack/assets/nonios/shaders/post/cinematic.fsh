#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:cinematic, final pass - the "RTX feel" without ray tracing:
// depth haze (aerial perspective) + bloom + god rays, filmic (ACES) tone map
// in linear light, warm split-tone grade, saturation, vignette, film grain.

uniform sampler2D InSampler;
uniform sampler2D BloomSampler;
uniform sampler2D RaysSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform CinematicConfig {
    vec4 RayColor;       // god ray tint
    vec4 HazeTint;       // rgb = distant colour tint, a = how much haze brightens
    vec4 ShadowTint;     // split tone, multiplies dark tones
    vec4 HighlightTint;  // split tone, multiplies bright tones
    float Exposure;
    float BloomStrength;
    float RayStrength;
    float HazeDensity;   // per block
    float HazeMax;       // 0..1 cap
    float Near;          // camera near plane in blocks, turns depth into distance
    float Saturation;
    float Contrast;
    float Vignette;
    float Grain;
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);

vec3 toLinear(vec3 c) { return pow(max(c, vec3(0.0)), vec3(2.2)); }
vec3 toGamma(vec3 c)  { return pow(max(c, vec3(0.0)), vec3(1.0 / 2.2)); }

// Narkowicz's ACES filmic fit.
vec3 aces(vec3 x) {
    return clamp((x * (2.51 * x + 0.03)) / (x * (2.43 * x + 0.59) + 0.14), 0.0, 1.0);
}

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
    vec3 c = texture(InSampler, texCoord).rgb;

    // --- depth haze: far terrain fades towards a warm, desaturated version of
    // itself (follows the scene's own brightness, so nights stay dark).
    float d = texture(DepthSampler, texCoord).r;
    float far = mix(1.0 - d, d, DepthReversed);            // ~ Near / distance
    float isSky = 1.0 - step(1e-6, far);
    float dist = Near / max(far, 1e-6);
    float haze = (1.0 - exp(-dist * HazeDensity)) * HazeMax * (1.0 - isSky);
    float l = dot(c, Luma);
    c = mix(c, vec3(l) * HazeTint.rgb * (1.0 + HazeTint.a), haze);

    // --- light: bloom + rays, added in linear space
    vec3 lin = toLinear(c);
    lin += toLinear(texture(BloomSampler, texCoord).rgb) * BloomStrength;
    lin += texture(RaysSampler, texCoord).r * toLinear(RayColor.rgb) * RayStrength;

    // --- filmic tone map
    c = toGamma(aces(lin * Exposure));

    // --- grade
    c = clamp((c - 0.5) * Contrast + 0.5, 0.0, 1.0);
    float t = dot(c, Luma);
    c *= mix(ShadowTint.rgb, HighlightTint.rgb, smoothstep(0.05, 0.85, t));
    c = mix(vec3(dot(c, Luma)), c, Saturation);

    // --- vignette (aspect-corrected) + per-tick film grain
    vec2 v = texCoord - 0.5;
    v.x *= InSize.x / InSize.y;
    c *= 1.0 - Vignette * smoothstep(0.35, 1.0, length(v));
    float grain = hash(texCoord * InSize + fract(GameTime * 1000.0) * vec2(97.0, 59.0)) - 0.5;
    c += grain * Grain;

    fragColor = vec4(clamp(c, 0.0, 1.0), 1.0);
}
