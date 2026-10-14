#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:cosmic, pass 2 - the moon-behind-leaves aura (v2) + the sky code.
// r = v2 "star" density: sky pixels brighter than their ring of neighbours while the surrounding sky is
//     dark. Next to the moon every gap between dark leaves passes this test; the big blurs after this
//     pass spread that cluster into the coloured aura around the tree (feedback #55: keep it).
// g, b = nebula fields A, B decoded from the sky code the demo overlay sky.fsh writes (two lowest bits
//     of R and G), fixed to world directions; blurred next into smooth nebula clouds.

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform AuraConfig {
    float StarGain;       // high-pass gain (v2: 4)
    float DarkSky;        // surrounding sky luma above which it is ignored (v2: 0.3)
    float BrightStart;    // luma where moon pixels count (v2: 0.75)
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);

float lumaAt(vec2 uv) {
    return dot(texture(InSampler, uv).rgb, Luma);
}

void main() {
    vec2 px = 1.0 / InSize;
    vec3 c = texture(InSampler, texCoord).rgb;
    float l = dot(c, Luma);

    float d = texture(DepthSampler, texCoord).r;
    float far = mix(1.0 - d, d, DepthReversed);
    float sky = 1.0 - step(1e-6, far);

    float ring = 0.0;
    for (int i = 0; i < 8; i++) {
        float a = float(i) * 0.785398;
        ring += lumaAt(texCoord + vec2(cos(a), sin(a)) * 3.0 * px);
    }
    ring /= 8.0;

    float gate = 1.0 - smoothstep(DarkSky * 0.6, DarkSky, ring);
    float star = clamp((l - ring - 0.02) * StarGain, 0.0, 1.0) * gate;
    float bright = smoothstep(BrightStart, 1.0, l);
    float s = max(star, bright) * sky;
    // v2 used the luma of (normalised colour * s)
    float density = dot(min(c / max(l, 0.25), vec3(2.0)), Luma) * s;

    ivec3 q = ivec3(floor(texelFetch(InSampler, ivec2(gl_FragCoord.xy), 0).rgb * 255.0 + 0.5)) & 3;
    vec2 neb = vec2(q.rg) / 3.0 * sky;

    fragColor = vec4(density, neb, 1.0);
}
