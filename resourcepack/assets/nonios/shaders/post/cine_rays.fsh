#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:cinematic, pass 2 - fake god rays (crepuscular rays).
// Post effects get no sun position, so the rays fan out from a fixed point
// (RayOrigin, default above the top centre of the screen). Each pixel marches
// towards it and gathers the sky-light mask from pass 1 (alpha): sky seen
// through leaves, windows and gaps streaks into the scene.

uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform RayConfig {
    vec2 RayOrigin;   // UV of the light point; y > 1 = above the screen top (use y < 0 if rays rise from the floor)
    float RayLength;  // fraction of the way to RayOrigin that is sampled
    float RayDecay;   // per-step falloff
};

layout(location = 0) out vec4 fragColor;

const int STEPS = 40;

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

void main() {
    vec2 stepUv = (RayOrigin - texCoord) * RayLength / float(STEPS);
    // Jitter the start per pixel to hide banding.
    vec2 uv = texCoord + stepUv * hash(texCoord * InSize);
    float weight = 1.0;
    float total = 0.0;
    float norm = 0.0;
    for (int i = 0; i < STEPS; i++) {
        total += texture(InSampler, clamp(uv, vec2(0.0), vec2(1.0))).a * weight;
        norm += weight;
        weight *= RayDecay;
        uv += stepUv;
    }
    fragColor = vec4(vec3(total / norm), 1.0);
}
