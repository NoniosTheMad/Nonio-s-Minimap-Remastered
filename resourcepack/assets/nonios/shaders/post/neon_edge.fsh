#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:neon, pass 1 - edges in their own saturated colour.
// Edge = depth discontinuity (relative second difference) + colour Sobel.
// Colour = the most colourful neighbour, pushed to full saturation and brightness,
// so every outline glows like a neon tube of the object's own colour.

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform NeonEdgeConfig {
    float DepthSensitivity;
    float ColorSensitivity;
    float MinChroma;       // greys below this become a pale tube
    float PaleTube;        // brightness of tubes on grey objects
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);

float invDepth(vec2 uv) {
    float d = texture(DepthSampler, uv).r;
    return mix(1.0 - d, d, DepthReversed);
}

void main() {
    vec2 px = 1.0 / InSize;
    float z = invDepth(texCoord);
    float lap = abs(invDepth(texCoord - vec2(px.x, 0.0)) + invDepth(texCoord + vec2(px.x, 0.0)) - 2.0 * z)
              + abs(invDepth(texCoord - vec2(0.0, px.y)) + invDepth(texCoord + vec2(0.0, px.y)) - 2.0 * z);
    float depthEdge = smoothstep(0.5, 1.5, lap / max(z, 1e-6) * DepthSensitivity);

    vec3 tl = texture(InSampler, texCoord + vec2(-px.x, px.y)).rgb;
    vec3 t  = texture(InSampler, texCoord + vec2(0.0, px.y)).rgb;
    vec3 tr = texture(InSampler, texCoord + vec2(px.x, px.y)).rgb;
    vec3 l  = texture(InSampler, texCoord + vec2(-px.x, 0.0)).rgb;
    vec3 c  = texture(InSampler, texCoord).rgb;
    vec3 r  = texture(InSampler, texCoord + vec2(px.x, 0.0)).rgb;
    vec3 bl = texture(InSampler, texCoord + vec2(-px.x, -px.y)).rgb;
    vec3 b  = texture(InSampler, texCoord + vec2(0.0, -px.y)).rgb;
    vec3 br = texture(InSampler, texCoord + vec2(px.x, -px.y)).rgb;
    vec3 gx = (tr + 2.0 * r + br) - (tl + 2.0 * l + bl);
    vec3 gy = (tl + 2.0 * t + tr) - (bl + 2.0 * b + br);
    float colorEdge = smoothstep(0.25, 0.8, length(gx) + length(gy)) * ColorSensitivity;

    float edge = clamp(max(depthEdge, colorEdge), 0.0, 1.0);

    // most colourful pixel of the cross
    vec3 best = c;
    float bestChroma = -1.0;
    vec3 cand[5] = vec3[5](c, t, l, r, b);
    for (int i = 0; i < 5; i++) {
        float mx = max(cand[i].r, max(cand[i].g, cand[i].b));
        float mn = min(cand[i].r, min(cand[i].g, cand[i].b));
        float ch = mx - mn;
        if (ch > bestChroma) {
            bestChroma = ch;
            best = cand[i];
        }
    }
    float mx = max(best.r, max(best.g, best.b));
    float mn = min(best.r, min(best.g, best.b));
    vec3 hue = (best - mn) / max(mx - mn, 1e-4);          // fully saturated, max channel = 1
    float colourful = smoothstep(MinChroma, MinChroma * 3.0, mx - mn);
    vec3 tube = mix(vec3(PaleTube), hue, colourful);

    fragColor = vec4(tube * edge, edge);
}
