#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:angel - majestic, ethereal world; thermal sight only on living things.
// World: lifted soft whites and golds, gentle bloom, luminous depth haze, drifting light motes.
// Living entities with HP (they glow while Angel/Thermal is on, team colour = HP bracket):
//  - body pixels are recognised by a marker the shaders demo entity.fsh writes into the colour's
//    lowest bits (R odd, G even, B odd), kept only near a glowing outline,
//  - those pixels get the thermal ironbow palette tinted by the HP colour,
//  - plus the thermal halo, white-hot outline core and the bracket pulse.
// Without the marker (other packs) the halo still shows, only the body tint is missing.

uniform sampler2D InSampler;
uniform sampler2D BloomSampler;
uniform sampler2D GlowSampler;
uniform sampler2D FillSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform AngelConfig {
    vec4 Gold;           // highlight / bloom tint
    vec4 HazeColor;      // luminous haze
    vec4 ShadowTint;     // lifted shadow colour
    float BloomStrength;
    float HazeDensity;
    float HazeMax;
    float Lift;          // shadow lift
    float Saturation;
    float Motes;         // drifting light motes (0 = off)
    float GlowStrength;  // HP halo
    float BodyHeat;      // thermal colouring of entity bodies
    float CoreWhite;
    float MinBright;
    float Tolerance;
    float Near;
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);
const float TAU = 6.28318530718;

const vec3 RED    = vec3(1.0, 0.333, 0.333);
const vec3 PURPLE = vec3(1.0, 0.333, 1.0);
const vec3 AQUA   = vec3(0.333, 1.0, 1.0);
const vec3 TEAM[5] = vec3[5](RED, vec3(1.0, 0.667, 0.0), vec3(0.333, 1.0, 0.333), PURPLE, AQUA);

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

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float marker(vec2 uv) {
    vec3 q = floor(texture(InSampler, uv).rgb * 255.0 + 0.5);
    vec3 par = mod(q, 2.0);
    return (par.r > 0.5 && par.g < 0.5 && par.b > 0.5) ? 1.0 : 0.0;
}

float closeness(vec3 n, vec3 team) {
    return 1.0 - smoothstep(0.1, 0.35, distance(n, team));
}

// one layer of drifting motes: cells of 1/scale, some hold one soft dot rising and swaying
float motes(vec2 p, float scale, float speed, float seed) {
    vec2 g = p * scale;
    g.y -= GameTime * speed;
    vec2 cell = floor(g);
    vec2 f = fract(g);
    float h = hash(cell + seed);
    if (h > 0.35) return 0.0;
    vec2 pos = vec2(hash(cell + seed + 3.1), hash(cell + seed + 7.7)) * 0.7 + 0.15;
    pos.x += 0.12 * sin(GameTime * TAU * (60.0 + h * 80.0) + h * 20.0);
    float d = length(f - pos);
    float tw = 0.5 + 0.5 * sin(GameTime * TAU * (300.0 + h * 400.0) + h * 40.0);
    return exp(-d * d * 900.0) * (0.4 + 0.6 * tw);
}

void main() {
    vec2 px = 1.0 / InSize;
    vec3 c = texture(InSampler, texCoord).rgb;
    float l = dot(c, Luma);

    float d = texture(DepthSampler, texCoord).r;
    float z = mix(1.0 - d, d, DepthReversed);
    float isSky = 1.0 - step(1e-6, z);
    float dist = Near / max(z, 1e-6);

    // --- ethereal world
    vec3 col = mix(vec3(l), c, Saturation);
    col = mix(col, ShadowTint.rgb, Lift * (1.0 - smoothstep(0.0, 0.5, l)));
    col *= mix(vec3(1.0), Gold.rgb, smoothstep(0.4, 1.0, l));
    vec3 bloom = texture(BloomSampler, texCoord).rgb * Gold.rgb;
    col = 1.0 - (1.0 - col) * (1.0 - clamp(bloom * BloomStrength, 0.0, 1.0));
    float haze = min(1.0 - exp(-dist * HazeDensity), HazeMax) * (1.0 - isSky);
    haze = max(haze, isSky * HazeMax * 0.5);
    col = mix(col, HazeColor.rgb, haze);

    if (Motes > 0.0) {
        vec2 aspect = vec2(InSize.x / InSize.y, 1.0);
        vec2 p = texCoord * aspect;
        float m = motes(p, 7.0, 60.0, 1.0) + motes(p, 13.0, 110.0, 5.0) * 0.6 + motes(p, 23.0, 180.0, 9.0) * 0.35;
        col += Gold.rgb * m * Motes;
    }

    // --- living entities: thermal body + HP halo
    vec4 g = texture(GlowSampler, texCoord);
    vec4 f = texture(FillSampler, texCoord);
    float vote = 0.0;
    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            vote += marker(texCoord + vec2(float(x), float(y)) * px);
        }
    }
    float body = smoothstep(5.0, 7.0, vote) * smoothstep(0.01, 0.06, f.a);

    vec3 tn = f.rgb / max(max(f.r, max(f.g, f.b)), 1e-4);
    vec3 thermal = ironbow(0.35 + l * 0.65) * mix(vec3(1.0), tn, 0.35);
    col = mix(col, thermal, body * BodyHeat);

    vec3 gn = g.rgb / max(max(g.r, max(g.g, g.b)), 1e-4);
    float heartbeat = pow(wave(1440.0), 6.0);
    float pulse = 1.0 + closeness(gn, RED) * 1.2 * heartbeat + closeness(gn, PURPLE) * 0.8 * wave(2400.0)
                + closeness(gn, AQUA) * 1.6 * wave(4200.0);
    col += g.rgb * GlowStrength * pulse;

    // white-hot core on the outline itself
    float mx = max(c.r, max(c.g, c.b));
    vec3 n = c / max(mx, 1e-4);
    float best = 1e9;
    vec3 team = vec3(0.0);
    for (int i = 0; i < 5; i++) {
        float dd = distance(n, TEAM[i]);
        if (dd < best) {
            best = dd;
            team = TEAM[i];
        }
    }
    float w = (1.0 - smoothstep(Tolerance * 0.5, Tolerance, best)) * smoothstep(MinBright, MinBright + 0.15, mx);
    col = mix(col, mix(team, vec3(1.0), CoreWhite), w * (1.0 - body));

    fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}
