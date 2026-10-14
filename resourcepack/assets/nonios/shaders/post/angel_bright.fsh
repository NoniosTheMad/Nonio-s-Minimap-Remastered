#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:angel v4, pass 1 - light extraction.
// rgb = everything brighter than Threshold (soft knee), warmed slightly: the source of the dreamy bloom.
// a   = "heaven light": bright sky (sun, bright clouds, horizon glow), weighted so the sun dominates.
//       The rays pass finds the light centre from it and scatters it into shafts.

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform AngelBrightConfig {
    float Threshold;
    float Knee;
    float SkyThreshold;
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);

void main() {
    vec3 c = texture(InSampler, texCoord).rgb;
    float l = dot(c, Luma);
    float mx = max(c.r, max(c.g, c.b));
    float br = mix(l, mx, 0.35);   // mostly luminance: a saturated blue sky is not "bright"

    float soft = clamp(br - Threshold + Knee, 0.0, 2.0 * Knee);
    soft = soft * soft / (4.0 * Knee + 1e-5);
    float k = clamp(max(soft, br - Threshold) / max(br, 1e-5), 0.0, 1.0);

    float d = texture(DepthSampler, texCoord).r;
    float far = mix(1.0 - d, d, DepthReversed);
    float sky = 1.0 - step(1e-6, far);

    // the sky glows less than surfaces (else the whole top of the screen would bloom)
    vec3 bloom = c * k * (1.0 - 0.55 * sky);
    // heaven light: the sun (near white) counts far more than blue sky
    float heaven = sky * pow(smoothstep(SkyThreshold, 1.0, l), 2.0) * (0.35 + 0.65 * smoothstep(0.8, 0.97, min(c.r, min(c.g, c.b)) / max(mx, 1e-4) * mx));
    // plain bright sky counts a little too: with the sun out of view the shafts come from above
    heaven = max(heaven, sky * 0.22 * smoothstep(0.35, 0.8, l));
    fragColor = vec4(bloom, heaven);
}
