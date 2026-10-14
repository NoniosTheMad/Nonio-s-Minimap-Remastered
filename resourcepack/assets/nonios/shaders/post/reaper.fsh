#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:reaper - "sees all": black world, white outlines.
// Geometric edges come from the depth buffer (second derivative, so flat
// surfaces stay black at any angle); texture detail comes from a luminance
// Sobel and is drawn fainter. Entities get outlined by their depth silhouette.

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform ReaperConfig {
    vec4 LineColor;
    vec4 BackColor;
    float DepthSensitivity;
    float LumaSensitivity;
    float LumaWeight;
    float Ghost;
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Gray = vec3(0.299, 0.587, 0.114);

float luma(vec2 uv) {
    return dot(texture(InSampler, uv).rgb, Gray);
}

// Depth mapped to something proportional to 1/viewZ (near = large, sky = 0).
// 26.2+ uses a reversed depth buffer (near = 1); DepthReversed = 0 flips it back.
float invDepth(vec2 uv) {
    float d = texture(DepthSampler, uv).r;
    return mix(1.0 - d, d, DepthReversed);
}

void main() {
    vec2 px = 1.0 / InSize;

    // --- depth edges: 1/z is affine across a plane in screen space, so its
    // second difference is ~0 on flat faces and spikes on silhouettes/creases.
    float c  = invDepth(texCoord);
    float l  = invDepth(texCoord - vec2(px.x, 0.0));
    float r  = invDepth(texCoord + vec2(px.x, 0.0));
    float u  = invDepth(texCoord - vec2(0.0, px.y));
    float d  = invDepth(texCoord + vec2(0.0, px.y));
    float ul = invDepth(texCoord + vec2(-px.x, -px.y));
    float dr = invDepth(texCoord + vec2( px.x,  px.y));
    float ur = invDepth(texCoord + vec2( px.x, -px.y));
    float dl = invDepth(texCoord + vec2(-px.x,  px.y));
    float lap = abs(l + r - 2.0 * c) + abs(u + d - 2.0 * c)
              + 0.5 * (abs(ul + dr - 2.0 * c) + abs(ur + dl - 2.0 * c));
    float nearest = max(c, max(max(l, r), max(u, d)));
    float depthEdge = smoothstep(1.0, 2.0, lap / max(nearest, 1e-6) * DepthSensitivity);

    // --- luminance Sobel (texture detail, fainter)
    float tl = luma(texCoord + vec2(-px.x, -px.y));
    float t  = luma(texCoord + vec2( 0.0,  -px.y));
    float tr = luma(texCoord + vec2( px.x, -px.y));
    float ml = luma(texCoord + vec2(-px.x,  0.0));
    float mr = luma(texCoord + vec2( px.x,  0.0));
    float bl = luma(texCoord + vec2(-px.x,  px.y));
    float b  = luma(texCoord + vec2( 0.0,   px.y));
    float br = luma(texCoord + vec2( px.x,  px.y));
    float gx = (tr + 2.0 * mr + br) - (tl + 2.0 * ml + bl);
    float gy = (bl + 2.0 * b + br) - (tl + 2.0 * t + tr);
    float lumaEdge = smoothstep(0.25, 0.6, length(vec2(gx, gy)) * LumaSensitivity) * LumaWeight;

    float edge = clamp(max(depthEdge, lumaEdge), 0.0, 1.0);

    float gray = dot(texture(InSampler, texCoord).rgb, Gray);
    vec3 base = BackColor.rgb + vec3(gray) * Ghost;
    fragColor = vec4(mix(base, LineColor.rgb, edge), 1.0);
}
