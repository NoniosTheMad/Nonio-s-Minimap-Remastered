#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:comic - colour layer: posterised flat colours, halftone dots in the
// shadows, warm paper highlights. Add the ink lines layer for the full
// comic-book look (preset "Comic book" = comic + ink).

uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform ComicConfig {
    vec4 PaperColor;
    float Levels;        // brightness bands
    float Saturation;
    float DotSize;       // halftone cell, pixels
    float DotStrength;
};

layout(location = 0) out vec4 fragColor;

vec3 rgb2hsv(vec3 c) {
    vec4 K = vec4(0.0, -1.0 / 3.0, 2.0 / 3.0, -1.0);
    vec4 p = mix(vec4(c.bg, K.wz), vec4(c.gb, K.xy), step(c.b, c.g));
    vec4 q = mix(vec4(p.xyw, c.r), vec4(c.r, p.yzx), step(p.x, c.r));
    float d = q.x - min(q.w, q.y);
    float e = 1.0e-10;
    return vec3(abs(q.z + (q.w - q.y) / (6.0 * d + e)), d / (q.x + e), q.x);
}

vec3 hsv2rgb(vec3 c) {
    vec4 K = vec4(1.0, 2.0 / 3.0, 1.0 / 3.0, 3.0);
    vec3 p = abs(fract(c.xxx + K.xyz) * 6.0 - K.www);
    return c.z * mix(K.xxx, clamp(p - K.xxx, 0.0, 1.0), c.y);
}

void main() {
    // --- flat colour: posterise brightness, punch up saturation
    vec3 hsv = rgb2hsv(texture(InSampler, texCoord).rgb);
    float v = hsv.z;
    hsv.z = max(floor(v * Levels + 0.5) / Levels, 0.06);
    hsv.y = clamp(hsv.y * Saturation, 0.0, 1.0);
    vec3 col = hsv2rgb(hsv);

    // --- halftone dots in the shadows (45-degree grid in screen pixels)
    vec2 p = mat2(0.7071, -0.7071, 0.7071, 0.7071) * (texCoord * InSize) / DotSize;
    vec2 cell = fract(p) - 0.5;
    float darkness = smoothstep(0.25, 0.85, 1.0 - v);
    float radius = sqrt(darkness) * 0.55;
    float aa = 1.5 / DotSize;
    float dots = 1.0 - smoothstep(radius - aa, radius + aa, length(cell));
    col *= 1.0 - DotStrength * dots * darkness;

    // --- paper-coloured highlights
    col = mix(col, PaperColor.rgb, smoothstep(0.8, 1.0, v) * 0.5);

    fragColor = vec4(col, 1.0);
}
