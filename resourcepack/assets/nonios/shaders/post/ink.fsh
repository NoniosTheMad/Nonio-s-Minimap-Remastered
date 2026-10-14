#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:ink / nonios:neon - lines layer, drawn over whatever is below it.
// Edges = depth creases/silhouettes (second difference of 1/z, as in reaper)
// + strong luminance edges. A second, wider sample gives a soft glow.
//   ink:  Additive 0 -> dark lines mixed in
//   neon: Additive 1 -> coloured lines added on top, scene slightly darkened

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform InkConfig {
    vec4 LineColor;
    float DepthSensitivity;
    float LumaSensitivity;
    float LumaWeight;
    float LineWidth;      // pixels
    float GlowWidth;      // pixels, 0 = no glow
    float GlowWeight;
    float Additive;       // 0 = mix (ink), 1 = add (neon)
    float Darken;         // scene multiplier loss in additive mode
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Gray = vec3(0.299, 0.587, 0.114);

float luma(vec2 uv) {
    return dot(texture(InSampler, uv).rgb, Gray);
}

float invDepth(vec2 uv) {
    float d = texture(DepthSampler, uv).r;
    return mix(1.0 - d, d, DepthReversed);
}

float edges(float width) {
    vec2 px = width / InSize;
    float c = invDepth(texCoord);
    float l = invDepth(texCoord - vec2(px.x, 0.0));
    float r = invDepth(texCoord + vec2(px.x, 0.0));
    float u = invDepth(texCoord - vec2(0.0, px.y));
    float d = invDepth(texCoord + vec2(0.0, px.y));
    float lap = abs(l + r - 2.0 * c) + abs(u + d - 2.0 * c);
    float nearest = max(c, max(max(l, r), max(u, d)));
    float depthEdge = smoothstep(1.0, 2.0, lap / max(nearest, 1e-6) * DepthSensitivity);

    float gx = luma(texCoord + vec2(px.x, 0.0)) - luma(texCoord - vec2(px.x, 0.0));
    float gy = luma(texCoord + vec2(0.0, px.y)) - luma(texCoord - vec2(0.0, px.y));
    float lumaEdge = smoothstep(0.3, 0.6, length(vec2(gx, gy)) * LumaSensitivity) * LumaWeight;
    return max(depthEdge, lumaEdge);
}

void main() {
    vec3 col = texture(InSampler, texCoord).rgb;
    float line = edges(LineWidth);
    float glow = GlowWidth > 0.0 ? edges(GlowWidth) * GlowWeight : 0.0;
    float e = clamp(max(line, glow), 0.0, 1.0);

    vec3 inked = mix(col, LineColor.rgb, e);
    vec3 neon = col * (1.0 - Darken) + LineColor.rgb * (line + glow);
    fragColor = vec4(clamp(mix(inked, neon, Additive), 0.0, 1.0), 1.0);
}
