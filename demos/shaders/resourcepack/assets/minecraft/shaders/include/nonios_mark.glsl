#ifndef NONIOS_MARK_GLSL
#define NONIOS_MARK_GLSL

// nonios markers: invisible codes in the two lowest bits of each colour channel (+-3/255),
// written by the demo overlay core shaders and read back by the nonios post effects.
//   bit 0 (R,G,B) = tag:   entity 1,0,1   terrain 0,1,0   particle 1,1,0
//   bit 1 (R,G,B) = data:  entity 0,0,0 (1,1,1 = emissive layer); terrain/particle = heat 0..7
// Sky pixels (no depth) carry their own code (see sky.fsh): R,G = nebula fields, B = star.
// Only opaque output is marked (blending would scramble the bits).

vec3 nonios_mark(vec3 c, vec3 low, vec3 hi) {
    vec3 q = floor(clamp(c, 0.0, 1.0) * 255.0 + 0.5);
    q = q - mod(q, 4.0) + low + 2.0 * hi;
    return q / 255.0;
}

vec3 nonios_heat_bits(float heat) {
    float l = floor(clamp(heat, 0.0, 1.0) * 7.0 + 0.5);
    return vec3(mod(l, 2.0), mod(floor(l / 2.0), 2.0), floor(l / 4.0));
}

// heat of a block surface: blockLight = 0..1 block light at the face, tex = raw texture colour.
// Only the emitters themselves are hot: a light-emitting block's own faces sit at block light >= 14
// (lava, fire, torches, glowstone, lanterns, shroomlight...), and its texture is bright and warm
// (or near-white, like a torch flame core). Blocks merely lit by a torch get 13 or less: cold.
// Ordinary terrain gets no heat at all (warmth around a source is done in screen space by the
// post effect, smoothly), so far terrain can't speckle.
float nonios_block_heat(vec3 tex, float blockLight) {
    float mx = max(tex.r, max(tex.g, tex.b));
    float mn = min(tex.r, min(tex.g, tex.b));
    float lit = smoothstep(0.89, 0.92, blockLight);
    float warm = smoothstep(0.2, 0.45, tex.r - tex.b) * smoothstep(0.72, 0.9, mx);
    float white = smoothstep(0.86, 0.96, mn);
    return lit * max(warm, white * 0.85);
}

#endif
