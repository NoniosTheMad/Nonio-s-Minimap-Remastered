#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:angel v5 ("seraph"), pass 2 - god rays, at a small fixed-size target.
// 1. Light centre: brightness^4-weighted centroid of the heaven mask (alpha of the extract) on a 24x14
//    grid. Every pixel computes the same grid, so all agree and the centre glides as you turn.
//    No bright sky on screen: the centre falls back to FallbackOrigin (upper right, off screen), so
//    shafts still stream diagonally across the frame like in the reference.
// 2. Radial scatter (GPU Gems 3 ch. 13): each pixel marches toward the centre gathering the heaven mask
//    with decay. Sky seen through leaves and over ridges streams into shafts; occluders cut gaps.
// 3. Broad beams: a low-frequency angular pattern (a few wide lobes with gaps) multiplies the scatter
//    and adds a faint "beam body" that crosses the scene even where no sky is behind it, so the shafts
//    read as wide diagonal bands, not a glow. The lobes drift and breathe slowly (time-blended noise,
//    seamless around the circle).
// Out: r = shafts, g = halo around the light centre, b = position across the beam (0..1, rainbow fringe),
//      a = how much of the screen is lit sky (day/night key).

uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform SeraphRayConfig {
    vec2 FallbackOrigin;
    float RayLength;
    float RayDecay;
    float Lobes;        // beams around the full circle (only ~1/6 of it is on screen from an off-screen light)
    float BeamBody;     // beams that cross the scene without sky behind them
    float Breathe;
};

layout(location = 0) out vec4 fragColor;

const int STEPS = 40;
const float TAU = 6.28318530718;

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453);
}

// periodic value noise (period P cells), smooth
float pnoise(float x, float P, float seed) {
    float i = floor(x);
    float f = fract(x);
    f = f * f * (3.0 - 2.0 * f);
    return mix(hash(vec2(mod(i, P), seed)), hash(vec2(mod(i + 1.0, P), seed)), f);
}

// noise that evolves in time by cross-fading two seeds (no drift along the angle = no seam)
float tnoise(float x, float P, float t, float seed) {
    float k = floor(t);
    float f = fract(t);
    f = f * f * (3.0 - 2.0 * f);
    return mix(pnoise(x, P, seed + k), pnoise(x, P, seed + k + 1.0), f);
}

void main() {
    vec2 acc = vec2(0.0);
    float wsum = 0.0;
    float area = 0.0;
    float peak = 0.0;
    for (int y = 0; y < 14; y++) {
        for (int x = 0; x < 24; x++) {
            vec2 uv = (vec2(x, y) + 0.5) / vec2(24.0, 14.0);
            float m = texture(InSampler, uv).a;
            float w = m * m * m * m;
            acc += uv * w;
            wsum += w;
            area += m;
            peak = max(peak, m);
        }
    }
    // how much of the screen is near the peak: a sun disc is a few cells, an overcast-bright sky is many
    float wide = 0.0;
    for (int y = 0; y < 14; y++) {
        for (int x = 0; x < 24; x++) {
            wide += step(0.7 * peak, texture(InSampler, (vec2(x, y) + 0.5) / vec2(24.0, 14.0)).a);
        }
    }
    wide /= 336.0;
    area /= 336.0;
    // a light is "found" only if there is a real peak (the sun / moon): a broad evenly bright sky
    // has no peak and the beams come from the fallback (upper right, off screen) instead
    float found = smoothstep(0.0004, 0.004, wsum / 336.0) * smoothstep(0.45, 0.75, peak)
                * (1.0 - smoothstep(0.04, 0.1, wide));
    vec2 origin = mix(FallbackOrigin, acc / max(wsum, 1e-6), found);

    // radial scatter toward the centre
    vec2 delta = (origin - texCoord) * RayLength / float(STEPS);
    vec2 uv = texCoord + delta * hash(texCoord * OutSize + fract(GameTime * 977.0));
    float weight = 1.0;
    float total = 0.0;
    float norm = 0.0;
    for (int i = 0; i < STEPS; i++) {
        vec2 q = clamp(uv, vec2(0.0), vec2(1.0));
        total += texture(InSampler, q).a * weight;
        norm += weight;
        weight *= RayDecay;
        uv += delta;
    }
    float shafts = total / norm;

    // broad beams around the centre
    vec2 aspect = vec2(OutSize.x / OutSize.y, 1.0);
    vec2 r = (texCoord - origin) * aspect;
    float ang = atan(r.y, r.x) / TAU + 0.5;
    float t = GameTime * 1200.0;   // seconds
    float n1 = tnoise(ang * Lobes, Lobes, t * 0.05, 3.0);
    float n2 = tnoise(ang * Lobes * 3.0, Lobes * 3.0, t * 0.08, 11.0);
    float lobe = smoothstep(0.42, 0.8, n1 * 0.7 + n2 * 0.4);
    float breathe = 0.75 + 0.25 * sin(t * 0.7 + n1 * 6.0);
    float beam = mix(1.0, lobe * breathe * 1.6, Breathe);
    // position across a beam: fract of the fine angle, for the spectral fringe
    float across = fract(ang * Lobes * 3.0 + 0.15 * sin(t * 0.05));

    float dist = length(r);
    // the beam body fades with distance from the centre and is stronger when the light is up and bright
    float sky = clamp(area * 3.0, 0.0, 1.0);
    float body = BeamBody * lobe * breathe * exp(-dist * 0.6) * (0.5 + 0.5 * sky);
    // gaps between beams stay clear even where the scatter is strong (broad bright sky)
    float rays = shafts * beam * mix(1.0, 0.25 + 0.75 * lobe, Breathe) + body * (0.75 + 0.25 * found);

    float glow = exp(-dist * 2.6) * (0.3 + 0.7 * found);
    fragColor = vec4(rays, glow, across, area);
}
