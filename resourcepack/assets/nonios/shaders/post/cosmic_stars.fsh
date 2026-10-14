#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:cosmic, pass 1 - find the light.
// The v2 "aura" (moon behind leaves) came from this pass: a pixel brighter than its
// ring of neighbours counts as a light, so every sky gap between dark leaves near a
// bright moon became a cluster of tiny "stars"; the blur passes then spread that cluster
// into a coloured gloom around the silhouette. v3 keeps that local-contrast test on
// purpose and applies it to the whole image (torches, lanterns, lava, glowstone, windows,
// moon, stars), plus an explicit silhouette rim where geometry meets bright sky.
// Contrast is a ratio, so lights glow at night and daylight surfaces mostly don't.
// Out: rgb = light (normalised colour * strength), a = sparkle mask (small sharp lights).

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform LightConfig {
    float ContrastGain;   // local-contrast lights (the aura source)
    float ContrastKnee;   // ratio (l - ring) / ring where a pixel starts to count
    float BrightStart;    // absolute luma where emissive / very bright pixels count
    float RimGain;        // sky-side rim around silhouettes
    float SkyBoost;       // extra weight for sky lights (stars, moon, leaf gaps)
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);

bool isSky(vec2 uv) {
    float d = texture(DepthSampler, uv).r;
    float far = mix(1.0 - d, d, DepthReversed);
    return far < 1e-6;
}

void main() {
    vec2 px = 1.0 / InSize;
    vec3 c = texture(InSampler, texCoord).rgb;
    float l = dot(c, Luma);
    float sky = isSky(texCoord) ? 1.0 : 0.0;

    // ring of neighbours at two radii: luma and how much of it is geometry
    float ring = 0.0;
    float geo = 0.0;
    for (int i = 0; i < 8; i++) {
        float a = float(i) * 0.785398;
        vec2 o = vec2(cos(a), sin(a)) * px;
        ring += dot(texture(InSampler, texCoord + o * 3.0).rgb, Luma);
        ring += dot(texture(InSampler, texCoord + o * 6.0).rgb, Luma);
        geo += isSky(texCoord + o * 3.0) ? 0.0 : 1.0;
    }
    ring /= 16.0;
    geo /= 8.0;

    // 1. local-contrast lights (ratio, so it works in the dark and stays calm in daylight)
    float ratio = (l - ring) / (ring + 0.04);
    float contrast = smoothstep(ContrastKnee, ContrastKnee * 4.0, ratio) * smoothstep(0.03, 0.15, l);
    // 2. emissive / very bright pixels (lava, glowstone, moon disc, torch flames)
    float bright = smoothstep(BrightStart, 1.0, l);
    // 3. sky-side rim: sky pixels touching geometry glow with the sky's own light
    float rim = sky * geo * (1.0 - geo) * 4.0 * smoothstep(0.02, 0.3, l);

    float s = contrast * ContrastGain + bright + rim * RimGain;
    s *= mix(1.0, SkyBoost, sky);

    // normalised colour: faint lights still glow in their own hue
    vec3 hue = min(c / max(l, 0.2), vec3(2.0));
    fragColor = vec4(hue * s, clamp(contrast + bright * 0.5, 0.0, 1.0));
}
