#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:planet v3 - small-planet curvature (screen-space, continuous).
// On a sphere of radius R a point at distance d sits d^2 / 2R lower; on screen that is a downward shift
// S = k * d (k = 1 / (4 R tanHalfFov)). The output pixel at height y shows the source row y + t where
// t = S(y + t). v3 (#63) reads d from the smoothed distance field (planet_dist.fsh) instead of the raw
// depth: no micro-folds at block edges, so the image bends as one continuous sheet, the march finds the
// same crossing frame after frame, and the bisection result moves smoothly as you walk. The source is
// sampled bilinearly (no pixel snapping). Only the real fold near the far horizon remains: what lies behind
// it is hidden by the curve, as on a real small planet. The bend fades out toward the top of the screen.

uniform sampler2D InSampler;
uniform sampler2D DistSampler;

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
};

layout(location = 0) out vec4 fragColor;

const int STEPS = 32;

float decode(ivec2 p) {
    vec2 e = floor(texelFetch(DistSampler, p, 0).rg * 255.0 + 0.5);
    return (e.x * 256.0 + e.y) / 65535.0;
}

// smoothed distance (0..1 of MaxDist) at uv, linearly interpolated in y (x is fixed per column)
float distAt(vec2 uv) {
    vec2 s = uv * InSize - 0.5;
    ivec2 sz = ivec2(InSize) - 1;
    int x = clamp(int(floor(s.x + 0.5)), 0, sz.x);
    float fy = floor(s.y);
    int y0 = clamp(int(fy), 0, sz.y);
    int y1 = clamp(int(fy) + 1, 0, sz.y);
    return mix(decode(ivec2(x, y0)), decode(ivec2(x, y1)), s.y - fy);
}

float shiftAt(vec2 uv, float k) {
    return k * distAt(uv) * MaxDist * (1.0 - smoothstep(FadeStart, 1.0, uv.y));
}

void main() {
    float k = 1.0 / (4.0 * Radius * TanHalfFov);
    float maxT = k * MaxDist;
    float dt = maxT / float(STEPS);
    float x = texCoord.x;
    float y = texCoord.y;

    // f(t) = shift(y + t) - t, f(0) >= 0; the first t with f <= 0 is the nearest surface that lands here
    float lo = 0.0;
    float flo = shiftAt(vec2(x, y), k);
    float hi = maxT;
    float fhi = -1.0;
    for (int i = 1; i <= STEPS; i++) {
        float t = float(i) * dt;
        float f = y + t >= 1.0 ? -1.0 : shiftAt(vec2(x, y + t), k) - t;
        if (f <= 0.0) {
            hi = t;
            fhi = f;
            break;
        }
        lo = t;
        flo = f;
    }
    // smooth f: a few bisection steps, then the secant (linear) root inside the bracket
    for (int j = 0; j < 5; j++) {
        float m = 0.5 * (lo + hi);
        float f = y + m >= 1.0 ? -1.0 : shiftAt(vec2(x, y + m), k) - m;
        if (f <= 0.0) { hi = m; fhi = f; } else { lo = m; flo = f; }
    }
    float t = mix(lo, hi, clamp(flo / max(flo - fhi, 1e-6), 0.0, 1.0));
    vec3 c = texture(InSampler, vec2(x, min(y + t, 1.0))).rgb;
    fragColor = vec4(c, 1.0);
}
