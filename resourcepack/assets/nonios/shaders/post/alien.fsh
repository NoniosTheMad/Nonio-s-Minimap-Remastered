#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:alien, final pass - alien heat sight (was "thermal" until round 5).
// The world is drawn cold (ironbow palette, low half), light sources and lava
// run hot, faint depth edges keep it readable. Heat signatures (glowing
// entities, see hp_sig) keep their HP-bracket colour with a white-hot
// core and a blurred halo:
//   red (low HP)                  - heartbeat pulse
//   light_purple (> 20 hearts)    - shimmering "about to burst"
//   aqua (> 40 hearts)            - faster, bigger burst (tiers double: log scale)

uniform sampler2D InSampler;
uniform sampler2D GlowSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform ThermalConfig {
    float WorldHeat;      // how hot the brightest ordinary block gets (0..1 of the palette)
    float EmissiveHeat;   // extra heat for near-white pixels (lights, lava, sun)
    float SkyCold;        // sky heat multiplier
    float EdgeHeat;       // depth-edge highlight
    float GlowStrength;   // halo intensity
    float CoreWhite;      // 0 = core keeps team colour, 1 = white-hot
    float MinBright;      // same as hp_sig
    float Tolerance;      // same as hp_sig
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);
const float TAU = 6.28318530718;

const vec3 RED    = vec3(1.0, 0.333, 0.333);
const vec3 PURPLE = vec3(1.0, 0.333, 1.0);
const vec3 AQUA   = vec3(0.333, 1.0, 1.0);

const vec3 TEAM[5] = vec3[5](
    RED,
    vec3(1.0, 0.667, 0.0),
    vec3(0.333, 1.0, 0.333),
    PURPLE,
    AQUA
);

// 0..1 wave with `cycles` periods per 20 real minutes (GameTime runs 0..1 every 20 min)
float wave(float cycles) {
    return 0.5 + 0.5 * sin(GameTime * TAU * cycles);
}

vec3 ironbow(float t) {
    t = clamp(t, 0.0, 1.0) * 6.0;
    vec3 c0 = vec3(0.00, 0.00, 0.05);
    vec3 c1 = vec3(0.08, 0.02, 0.32);
    vec3 c2 = vec3(0.42, 0.02, 0.55);
    vec3 c3 = vec3(0.82, 0.12, 0.30);
    vec3 c4 = vec3(1.00, 0.50, 0.05);
    vec3 c5 = vec3(1.00, 0.86, 0.30);
    vec3 c6 = vec3(1.00, 1.00, 0.95);
    if (t < 1.0) return mix(c0, c1, t);
    if (t < 2.0) return mix(c1, c2, t - 1.0);
    if (t < 3.0) return mix(c2, c3, t - 2.0);
    if (t < 4.0) return mix(c3, c4, t - 3.0);
    if (t < 5.0) return mix(c4, c5, t - 4.0);
    return mix(c5, c6, t - 5.0);
}

float invDepth(vec2 uv) {
    float d = texture(DepthSampler, uv).r;
    return mix(1.0 - d, d, DepthReversed);
}

float closeness(vec3 n, vec3 team) {
    return 1.0 - smoothstep(0.1, 0.35, distance(n, team));
}

void main() {
    vec2 px = 1.0 / InSize;
    vec3 c = texture(InSampler, texCoord).rgb;
    float m = max(c.r, max(c.g, c.b));

    // --- cold world
    float z = invDepth(texCoord);
    float isSky = 1.0 - step(1e-6, z);
    float heat = pow(dot(c, Luma), 1.2) * WorldHeat + smoothstep(0.85, 1.0, m) * EmissiveHeat;
    heat *= mix(1.0, SkyCold, isSky);

    float lap = abs(invDepth(texCoord - vec2(px.x, 0.0)) + invDepth(texCoord + vec2(px.x, 0.0)) - 2.0 * z)
              + abs(invDepth(texCoord - vec2(0.0, px.y)) + invDepth(texCoord + vec2(0.0, px.y)) - 2.0 * z);
    heat += smoothstep(1.0, 2.0, lap / max(z, 1e-6) * 60.0) * EdgeHeat;

    vec3 col = ironbow(heat);

    // --- halo from the blurred signatures, pulsing per bracket
    vec4 g = texture(GlowSampler, texCoord);
    vec3 gn = g.rgb / max(max(g.r, max(g.g, g.b)), 1e-4);
    float heartbeat = pow(wave(1440.0), 6.0);                   // ~1.2 Hz
    float pulse = 1.0
        + closeness(gn, RED) * 1.2 * heartbeat
        + closeness(gn, PURPLE) * 0.8 * wave(2400.0)            // ~2 Hz
        + closeness(gn, AQUA) * 1.6 * wave(4200.0);             // ~3.5 Hz
    col += g.rgb * GlowStrength * pulse;

    // --- white-hot core on the outline itself
    vec3 n = c / max(m, 1e-4);
    float best = 1e9;
    vec3 team = vec3(0.0);
    for (int i = 0; i < 5; i++) {
        float dd = distance(n, TEAM[i]);
        if (dd < best) {
            best = dd;
            team = TEAM[i];
        }
    }
    float w = (1.0 - smoothstep(Tolerance * 0.5, Tolerance, best)) * smoothstep(MinBright, MinBright + 0.15, m);
    col = mix(col, mix(team, vec3(1.0), CoreWhite), w);

    fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}
