#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:cinematic v2 - a restrained film look, rebuilt from scratch.
// v1 tone-mapped an already display-ready image a second time (ACES on Minecraft's LDR frame: whites went
// grey, everything murky), fanned fake god rays from a fixed point above the screen whatever the sun was
// doing, and washed distant terrain into grey haze with a seam at the sky. All of that is gone.
// Now, in order:
//   halation   - the blurred highlights bleed back in, tinted red-orange (film's red-layer glow), screen blend,
//   grade      - gentle S-curve that keeps white white, slightly lifted blacks, warm highlights /
//                teal shadows by luminance (teal-orange, subtle), a touch less saturation in the shadows,
//   vignette   - soft, inside the picture area,
//   grain      - luminance-weighted (strongest in the mid-tones), new every tick,
//   letterbox  - black bars for a 2.39:1 frame (at least MinBar per side on very wide screens).

uniform sampler2D InSampler;
uniform sampler2D BloomSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform FilmConfig {
    vec4 HalationColor;   // tint of the highlight bleed
    vec4 ShadowTint;      // added to the shadows (teal)
    vec4 HighlightTint;   // added to the highlights (warm)
    float Halation;
    float Bloom;          // neutral part of the highlight bleed
    float Contrast;       // S-curve amount 0..1
    float BlackLift;
    float Saturation;
    float ShadowDesat;
    float Vignette;
    float Grain;
    float FrameAspect;    // 2.39
    float MinBar;         // minimum bar height per side (fraction of the screen)
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

vec3 screen(vec3 a, vec3 b) {
    return 1.0 - (1.0 - a) * (1.0 - b);
}

void main() {
    vec3 c = texture(InSampler, texCoord).rgb;
    vec3 b = texture(BloomSampler, texCoord).rgb;

    // --- halation + a little neutral bloom
    float bl = dot(b, Luma);
    c = screen(c, clamp(HalationColor.rgb * bl * Halation + b * Bloom, 0.0, 1.0));

    // --- grade: S-curve (white stays white, black stays near black)
    vec3 s = c * c * (3.0 - 2.0 * c);
    c = mix(c, s, Contrast);
    c = BlackLift + (1.0 - BlackLift) * c;
    float l = dot(c, Luma);
    // split tone: teal shadows, warm highlights, both fading out toward the extremes
    float sh = (1.0 - smoothstep(0.0, 0.55, l)) * smoothstep(0.0, 0.08, l);
    float hi = smoothstep(0.45, 1.0, l) * (1.0 - smoothstep(0.92, 1.0, l));
    c += ShadowTint.rgb * sh + HighlightTint.rgb * hi;
    // saturation, a bit lower in the shadows
    float sat = Saturation * (1.0 - ShadowDesat * (1.0 - smoothstep(0.05, 0.4, l)));
    c = mix(vec3(dot(c, Luma)), c, sat);

    // --- picture area (letterbox)
    float aspect = InSize.x / InSize.y;
    float bar = max(0.5 * (1.0 - aspect / FrameAspect), MinBar);
    float y = texCoord.y;
    float inside = smoothstep(bar - 0.75 / InSize.y, bar + 0.75 / InSize.y, y)
                 * smoothstep(bar - 0.75 / InSize.y, bar + 0.75 / InSize.y, 1.0 - y);

    // --- vignette inside the frame
    vec2 v = vec2((texCoord.x - 0.5) * aspect, (y - 0.5) / max(1.0 - 2.0 * bar, 0.1));
    c *= 1.0 - Vignette * smoothstep(0.3, 1.1, length(v));

    // --- grain: two hashes ~ triangular noise, strongest in the mid-tones
    vec2 gp = gl_FragCoord.xy + fract(GameTime * 1000.0) * vec2(173.0, 91.0);
    float g = hash(gp) + hash(gp + 37.1) - 1.0;
    l = clamp(dot(c, Luma), 0.0, 1.0);
    c += g * Grain * (0.35 + 2.6 * l * (1.0 - l));

    fragColor = vec4(clamp(c, 0.0, 1.0) * inside, 1.0);
}
