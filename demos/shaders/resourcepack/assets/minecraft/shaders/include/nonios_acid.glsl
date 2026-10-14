#ifndef NONIOS_ACID_GLSL
#define NONIOS_ACID_GLSL

// nonios "Acid": the classic world warp (GLSL shaders mod "acid" formula).
// Distant geometry waves and curls up over the player and covers the sky; near the camera nothing moves.
// Per player switch: the night_vision effect. The overridden lightmap.fsh writes the night vision
// factor into the lightmap's alpha (1.0 = off, 1 - 8/255 = on); vertex shaders read texel (0,0).
// pos = camera-relative position (before the view rotation).

#include <minecraft:globals.glsl>
#include <minecraft:projection.glsl>

float nonios_acid_amount(sampler2D lightmap) {
    float a = texelFetch(lightmap, ivec2(0, 0), 0).a;
    // world only: orthographic projections (GUI, inventory paperdoll) have ProjMat[3][3] = 1
    float perspective = step(ProjMat[3][3], 0.5);
    return clamp((1.0 - a) * 255.0 / 8.0, 0.0, 1.0) * perspective;
}

vec3 nonios_acid_warp(vec3 pos, float amount) {
    if (amount <= 0.0) return pos;
    // Original used worldTime/143, /256, /200 (ticks). Integer cycles per GameTime (0..1 per 24000 ticks)
    // keep it seamless when GameTime wraps: 27, 15, 19 cycles = periods of ~889, 1600, 1263 ticks.
    const float TAU = 6.28318530718;
    float t1 = sin(TAU * GameTime * 27.0);
    float t2 = sin(TAU * GameTime * 15.0);
    float t3 = sin(TAU * GameTime * 19.0);
    // keep a minimum bend so the effect never fully flattens while it is on
    t2 = sign(t2) * max(abs(t2), 0.35);
    t3 = sign(t3) * max(abs(t3), 0.35);
    float d2 = pos.x * pos.x + pos.z * pos.z;
    vec3 p = pos;
    p.y += 5.0 * sin(d2 * t1 / 1000.0);
    float om = sin(d2 * t2 / 5000.0) * t3;
    float x = p.x, y = p.y;
    p.y = x * sin(om) + y * cos(om);
    p.x = x * cos(om) - y * sin(om);
    return mix(pos, p, amount);
}

#endif
