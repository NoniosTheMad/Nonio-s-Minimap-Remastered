#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:cinematic, pass 1 - bright pass.
// rgb = the part of each pixel above Threshold (soft knee), fed to the bloom blur.
// a   = sky luminance (sky = nothing drawn = depth 0 with reversed depth), the
//       light source for the fake god rays in pass 2.

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform BrightConfig {
    float Threshold;      // 0..1, brightness where bloom starts
    float Knee;           // softness of the threshold
    float SkyThreshold;   // sky luma that starts to cast rays (keeps the night sky dark)
    float DepthReversed;  // 1 = reversed depth (26.2+), 0 = classic
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);

void main() {
    vec3 c = texture(InSampler, texCoord).rgb;
    float bright = max(c.r, max(c.g, c.b));

    float soft = clamp(bright - Threshold + Knee, 0.0, 2.0 * Knee);
    soft = soft * soft / (4.0 * Knee + 1e-5);
    float contribution = max(soft, bright - Threshold) / max(bright, 1e-5);
    vec3 bloom = c * clamp(contribution, 0.0, 1.0);

    float d = texture(DepthSampler, texCoord).r;
    float far = mix(1.0 - d, d, DepthReversed);   // 0 at the sky / far plane
    float sky = 1.0 - step(1e-6, far);
    float skyLight = sky * smoothstep(SkyThreshold, 1.0, dot(c, Luma));

    fragColor = vec4(bloom, skyLight);
}
