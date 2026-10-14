#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:fog.glsl>
#include <minecraft:dynamictransforms.glsl>
#include <minecraft:nonios_mark.glsl>

// nonios: vanilla sky + an invisible code for the Cosmic post effect (two lowest bits per channel,
// at most 3/255): nebula fields A, B and stars, with a check bit (see nonios_sky_code in nonios_mark.glsl). The fields are functions of
// the world direction, so the nebula and the stars Cosmic paints from them stay fixed in the sky as you
// turn. Players without Cosmic see the vanilla sky.

layout(location = 0) in float sphericalVertexDistance;
layout(location = 1) in float cylindricalVertexDistance;
layout(location = 2) in vec3 skyPos;

layout(location = 0) out vec4 fragColor;

float hash13(vec3 p3) {
    p3 = fract(p3 * 0.1031);
    p3 += dot(p3, p3.zyx + 31.32);
    return fract((p3.x + p3.y) * p3.z);
}

float vnoise(vec3 p) {
    vec3 i = floor(p);
    vec3 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    float a = mix(mix(hash13(i), hash13(i + vec3(1, 0, 0)), f.x), mix(hash13(i + vec3(0, 1, 0)), hash13(i + vec3(1, 1, 0)), f.x), f.y);
    float b = mix(mix(hash13(i + vec3(0, 0, 1)), hash13(i + vec3(1, 0, 1)), f.x), mix(hash13(i + vec3(0, 1, 1)), hash13(i + vec3(1, 1, 1)), f.x), f.y);
    return mix(a, b, f.z);
}

float fbm(vec3 p) {
    return (vnoise(p) * 0.5 + vnoise(p * 2.03) * 0.25 + vnoise(p * 4.01) * 0.125 + vnoise(p * 8.05) * 0.0625) / 0.9375;
}

void main() {
    fragColor = apply_fog(ColorModulator, sphericalVertexDistance, cylindricalVertexDistance, 0.0, FogSkyEnd, FogSkyEnd, FogSkyEnd, FogColor);

    vec3 dir = normalize(skyPos);
    float up = smoothstep(-0.02, 0.12, dir.y);
    // a "galactic" band across the sky: the nebula is densest along it
    float band = exp(-pow(dot(dir, normalize(vec3(0.42, 0.30, 0.86))) / 0.38, 2.0));
    float a = clamp((fbm(dir * 2.6 + vec3(3.1, 0.0, 1.7)) - 0.38) * 2.4, 0.0, 1.0) * (0.3 + 0.7 * band) * up;
    float b = clamp((fbm(dir * 4.2 + vec3(0.0, 7.7, 2.3)) - 0.46) * 2.8, 0.0, 1.0) * (0.2 + 0.8 * band) * up;

    // stars: one candidate per direction cell, denser along the band
    vec3 g = dir * 260.0;
    vec3 cell = floor(g);
    float h = hash13(cell);
    float star = 0.0;
    if (h < 0.012 + 0.05 * band) {
        vec3 p = cell + 0.5 + (vec3(hash13(cell + 1.7), hash13(cell + 4.3), hash13(cell + 8.9)) - 0.5) * 0.5;
        float d = length(g - p);
        float lvl = 1.0 + floor(hash13(cell + 12.1) * 2.99);
        star = (d < 0.42 ? lvl : 0.0) * up;
    }

    vec3 code = nonios_sky_code(a, b, star, ivec2(gl_FragCoord.xy));
    vec3 q = floor(clamp(fragColor.rgb, 0.0, 1.0) * 255.0 + 0.5);
    fragColor.rgb = (q - mod(q, 4.0) + code) / 255.0;
}
