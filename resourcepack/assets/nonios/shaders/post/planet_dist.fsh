#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:planet v3, passes 1-2: a smooth distance field for the bend.
// v2 shifted each pixel by its own depth, so every block step, tree edge and the terrain/sky seam made a
// small fold in the mapping, and the column march jumped between folds: the landscape moved in "steps"
// (#63). v3 bends by a SMOOTHED distance (Gaussian, ~3 % of the screen height), so the mapping is smooth
// and the inverse search below is continuous.
// Pass 1 (Mode 0): depth -> distance, Gaussian along x. Pass 2 (Mode 1): the same along y.
// Values are stored as 16 bits in r (high byte) + g (low byte) of distance / MaxDist; they are read with
// texelFetch (never filtered: filtering would mix the bytes).

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform DistConfig {
    float Mode;          // 0 = from depth, along x; 1 = from pass 1, along y
    float Spread;        // Gaussian sigma as a fraction of the screen height
    float MaxDist;
    float Near;
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

float fromDepth(ivec2 p) {
    float d = texelFetch(DepthSampler, p, 0).r;
    float z = mix(1.0 - d, d, DepthReversed);
    return min(Near / max(z, 1e-6), MaxDist) / MaxDist;
}

float decode(ivec2 p) {
    vec2 e = floor(texelFetch(InSampler, p, 0).rg * 255.0 + 0.5);
    return (e.x * 256.0 + e.y) / 65535.0;
}

vec4 encode(float v) {
    float q = floor(clamp(v, 0.0, 1.0) * 65535.0 + 0.5);
    float hi = floor(q / 256.0);
    return vec4(hi / 255.0, (q - hi * 256.0) / 255.0, 0.0, 1.0);
}

void main() {
    ivec2 p = ivec2(gl_FragCoord.xy);
    ivec2 sz = ivec2(InSize) - 1;
    float sigma = max(Spread * InSize.y, 1.0);
    int n = 12;                                   // taps per side
    float stepPx = sigma * 2.5 / float(n);
    ivec2 dir = Mode < 0.5 ? ivec2(1, 0) : ivec2(0, 1);
    float sum = 0.0;
    float wsum = 0.0;
    for (int i = -n; i <= n; i++) {
        float o = float(i) * stepPx;
        ivec2 q = clamp(p + dir * int(floor(o + 0.5)), ivec2(0), sz);
        float w = exp(-0.5 * (o * o) / (sigma * sigma));
        float v = Mode < 0.5 ? fromDepth(q) : decode(q);
        sum += v * w;
        wsum += w;
    }
    fragColor = encode(sum / wsum);
}
