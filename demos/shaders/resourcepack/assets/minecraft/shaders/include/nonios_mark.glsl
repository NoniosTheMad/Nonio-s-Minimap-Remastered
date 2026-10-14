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
// Light sources (lava, fire, torch flame, glowstone, magma, lanterns: warm, bright textures under
// full block light) are hot; the blocks around a light are warm; everything else is cold.
float nonios_block_heat(vec3 tex, float blockLight) {
    float mx = max(tex.r, max(tex.g, tex.b));
    float warm = clamp((tex.r - tex.b) * 2.2, 0.0, 1.0) * smoothstep(0.45, 0.8, mx);
    float source = smoothstep(0.78, 0.93, blockLight) * warm;
    float ambient = smoothstep(0.45, 1.0, blockLight) * 0.5;
    return max(ambient, source);
}

#endif
