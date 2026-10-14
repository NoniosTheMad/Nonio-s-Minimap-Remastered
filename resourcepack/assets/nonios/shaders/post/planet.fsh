#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:planet v2 - small-planet curvature (screen-space, steady, no wobble).
// On a sphere of radius R, a point at distance d sits d^2 / 2R lower; on screen that is a downward shift
// S = k * d (k = 1 / (4 R tanHalfFov)). Sky and anything past MaxDist (far clouds) count as MaxDist.
// v1 found each pixel's source with a 6-step fixed-point iteration; where depth jumps (cloud edges,
// leaves, silhouettes) it oscillated and produced torn, smeared clouds and ghost bands (#56).
// v2 marches up the column from the output pixel and takes the FIRST source whose own shift lands it
// here (= the nearest surface wins, like a height-field ray march), then refines the hit by bisection.
// The shift fades out toward the top of the screen (FadeStart..1), so the mapping always covers the
// whole screen: no stretched top row, and the sky / clouds bend smoothly instead of tearing.

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
    float FadeStart;     // screen height (0..1) where the bend starts to fade out toward the top
    float Near;
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const int STEPS = 40;

float dist(vec2 uv) {
    ivec2 p = clamp(ivec2(uv * InSize), ivec2(0), ivec2(InSize) - 1);
    float d = texelFetch(DepthSampler, p, 0).r;
    float z = mix(1.0 - d, d, DepthReversed);
    return min(Near / max(z, 1e-6), MaxDist);
}

// screen shift (uv) of the content at uv
float shiftAt(vec2 uv, float k) {
    return k * dist(uv) * (1.0 - smoothstep(FadeStart, 1.0, uv.y));
}

void main() {
    float k = 1.0 / (4.0 * Radius * TanHalfFov);
    float maxT = k * MaxDist;
    float dt = maxT / float(STEPS);
    float x = texCoord.x;
    float y = texCoord.y;

    // f(t) = shift(y + t) - t: positive = that source lands above us, <= 0 = it reaches down to here
    float lo = 0.0;
    float flo = shiftAt(vec2(x, y), k);
    float hi = -1.0;
    float fhi = 0.0;
    if (flo <= 0.0) {
        hi = 0.0;
    } else {
        for (int i = 1; i <= STEPS; i++) {
            float t = float(i) * dt;
            float ys = min(y + t, 1.0);
            float f = shiftAt(vec2(x, ys), k) - t;
            if (f <= 0.0 || ys >= 1.0) {
                hi = t;
                fhi = f;
                break;
            }
            lo = t;
            flo = f;
        }
        if (hi < 0.0) {
            hi = maxT;
        }
        for (int j = 0; j < 6; j++) {
            float m = 0.5 * (lo + hi);
            float f = shiftAt(vec2(x, min(y + m, 1.0)), k) - m;
            if (f <= 0.0) {
                hi = m;
                fhi = f;
            } else {
                lo = m;
                flo = f;
            }
        }
        // a jump in depth (not a real crossing) is a disocclusion: fill it from the far side
        if (flo - fhi > 3.0 * dt) {
            hi = lo;
        }
    }
    vec3 c = texture(InSampler, vec2(x, min(y + hi, 1.0))).rgb;
    fragColor = vec4(c, 1.0);
}
