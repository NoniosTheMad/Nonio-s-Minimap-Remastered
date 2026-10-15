#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:angel v5 ("seraph"), pass 1 - light extraction, written to a small fixed-size target (cheap).
// rgb = bloom source: everything brighter than Threshold through a soft knee, warmed toward gold.
//       Sky counts less than surfaces (a blue sky must not bloom the whole top of the screen), and
//       foliage/grass edges that are lit catch a little extra (the ref's leaves glow gold).
// a   = "heaven light": bright sky (sun, sunlit horizon, bright clouds); the sun dominates.
//       The rays pass finds the light centre from it and scatters it into shafts.

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform SeraphExtractConfig {
    float Threshold;
    float Knee;
    float SkyThreshold;
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);

void main() {
    // 4 taps: the target is ~1/4 res, average so thin bright details are not missed or aliased
    vec2 h = 0.5 / OutSize;
    vec3 c = vec3(0.0);
    float sky = 0.0;
    float sunny = 0.0;
    for (int i = 0; i < 4; i++) {
        vec2 o = vec2((i & 1) == 0 ? -h.x : h.x, (i & 2) == 0 ? -h.y : h.y) * 0.5;
        vec3 s = texture(InSampler, texCoord + o).rgb;
        float d = texture(DepthSampler, texCoord + o).r;
        float far = mix(1.0 - d, d, DepthReversed);
        float isSky = 1.0 - step(1e-6, far);
        c += s;
        sky += isSky;
        float l = dot(s, Luma);
        float mx = max(s.r, max(s.g, s.b));
        float whiteness = min(s.r, min(s.g, s.b)) / max(mx, 1e-4);   // sun ~ white, sky ~ blue
        float heaven = isSky * pow(smoothstep(SkyThreshold, 1.0, l), 2.0) * (0.3 + 0.7 * smoothstep(0.75, 0.95, whiteness * mx));
        heaven = max(heaven, isSky * 0.25 * smoothstep(0.3, 0.8, l));
        sunny += heaven;
    }
    c *= 0.25;
    sky *= 0.25;
    sunny *= 0.25;

    float l = dot(c, Luma);
    float mx = max(c.r, max(c.g, c.b));
    float br = mix(l, mx, 0.35);
    float soft = clamp(br - Threshold + Knee, 0.0, 2.0 * Knee);
    soft = soft * soft / (4.0 * Knee + 1e-5);
    float k = clamp(max(soft, br - Threshold) / max(br, 1e-5), 0.0, 1.0);
    vec3 bloom = c * k * (1.0 - 0.6 * sky);
    // warm the bloom source: highlights glow gold
    bloom *= vec3(1.05, 0.95, 0.75);
    fragColor = vec4(bloom, sunny);
}
