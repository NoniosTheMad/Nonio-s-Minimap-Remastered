#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:planet - small-planet curvature (screen-space, steady, no wobble).
// On a sphere of radius R, terrain at distance d sits d^2 / 2R lower; on screen that is a
// downward shift proportional to d. Each output pixel searches upward for the source pixel
// whose own distance makes it land here (fixed-point iteration on the depth buffer), so far
// terrain sinks smoothly below a raised horizon, near terrain stays put. Runs last in the stack.

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform PlanetConfig {
    float Radius;        // planet radius in blocks
    float TanHalfFov;    // tan(fov / 2), 70 deg -> 0.70
    float MaxDist;       // distance used for sky / beyond render distance
    float Near;
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

float dist(vec2 uv) {
    float d = texture(DepthSampler, uv).r;
    float z = mix(1.0 - d, d, DepthReversed);
    return min(Near / max(z, 1e-6), MaxDist);
}

void main() {
    // screen shift (in uv) for a point at distance d: drop / (2 d tanHalf) with drop = d^2 / 2R
    float k = 1.0 / (4.0 * Radius * TanHalfFov);
    vec2 s = texCoord;
    for (int i = 0; i < 6; i++) {
        s.y = texCoord.y + k * dist(s);
    }
    vec3 c = s.y <= 1.0 ? texture(InSampler, s).rgb : texture(InSampler, vec2(s.x, 1.0)).rgb;
    fragColor = vec4(c, 1.0);
}
