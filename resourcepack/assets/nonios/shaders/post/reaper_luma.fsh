#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:reaper_luma - fallback/diagnostic for nonios:reaper without the depth
// buffer: grayscale + luminance Sobel only. If this works and reaper doesn't,
// depth sampling (use_depth_buffer) is the problem.

uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform ReaperConfig {
    vec4 LineColor;
    vec4 BackColor;
    float LumaSensitivity;
    float Ghost;
};

layout(location = 0) out vec4 fragColor;

const vec3 Gray = vec3(0.299, 0.587, 0.114);

float luma(vec2 uv) {
    return dot(texture(InSampler, uv).rgb, Gray);
}

void main() {
    vec2 px = 1.0 / InSize;

    float tl = luma(texCoord + vec2(-px.x, -px.y));
    float t  = luma(texCoord + vec2( 0.0,  -px.y));
    float tr = luma(texCoord + vec2( px.x, -px.y));
    float ml = luma(texCoord + vec2(-px.x,  0.0));
    float c  = luma(texCoord);
    float mr = luma(texCoord + vec2( px.x,  0.0));
    float bl = luma(texCoord + vec2(-px.x,  px.y));
    float b  = luma(texCoord + vec2( 0.0,   px.y));
    float br = luma(texCoord + vec2( px.x,  px.y));
    float gx = (tr + 2.0 * mr + br) - (tl + 2.0 * ml + bl);
    float gy = (bl + 2.0 * b + br) - (tl + 2.0 * t + tr);
    float edge = smoothstep(0.2, 0.5, length(vec2(gx, gy)) * LumaSensitivity);

    vec3 base = BackColor.rgb + vec3(c) * Ghost;
    fragColor = vec4(mix(base, LineColor.rgb, edge), 1.0);
}
