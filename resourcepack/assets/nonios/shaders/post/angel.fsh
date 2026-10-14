#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:angel v4 (#63) - ethereal light, built in tools/shaderlab first (reference: demos/shaders/reference/angel.gif).
// v3 was "a bit of bloom + rays": correct but not ethereal. v4 layers the classic dreamy-photo recipe:
//  - Orton glow: the whole image blurred (Soft) is screen-blended back over itself, so every surface
//    gets a soft luminous diffusion, not only highlights,
//  - three-scale gold/white bloom (Bloom 6 px, BloomMid 18 px, BloomLarge 48 px) on bright things,
//  - volumetric light shafts from the brightest sky region (angel_rays: found, not fixed) + a soft
//    sun halo, tinted warm,
//  - luminous haze: distance lifts toward a warm white instead of grey (heaven is bright),
//  - pastel grade: gentle desaturation, warm highlights, lifted milky blacks, a bright soft
//    vignette (the edges glow instead of darkening),
//  - a few slow light motes (soft bokeh discs drifting up, twinkling; screen space, sparse).
// Living entities with HP: unchanged from v3 (entity-marker body in HP-tinted ironbow, HP halo, white-hot core).

uniform sampler2D InSampler;
uniform sampler2D BloomSampler;
uniform sampler2D BloomMidSampler;
uniform sampler2D BloomLargeSampler;
uniform sampler2D SoftSampler;
uniform sampler2D RaysSampler;
uniform sampler2D GlowSampler;
uniform sampler2D FillSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform AngelConfig {
    vec4 Gold;           // bloom tint
    vec4 RayColor;       // light shaft tint
    vec4 HazeColor;      // luminous distance haze
    vec4 LiftColor;      // milky black lift
    float BloomStrength;
    float RayStrength;
    float HazeDensity;
    float HazeMax;
    float Saturation;
    float Exposure;
    float Vignette;      // bright edge glow
    float Orton;         // screen blend of the soft copy
    float BlackLift;
    float Motes;
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

void main() {
    vec2 px = 1.0 / InSize;
    vec3 c = texture(InSampler, texCoord).rgb;
    float l = dot(c, Luma);

    float d = texture(DepthSampler, texCoord).r;
    float z = mix(1.0 - d, d, DepthReversed);
    float isSky = 1.0 - step(1e-6, z);
    float dist = Near / max(z, 1e-6);

    // --- ethereal light
    vec3 col = c * Exposure;
    // pastel: gentle desaturation, a bit more in the highlights
    float cl = dot(col, Luma);
    col = max(mix(vec3(cl), col, mix(Saturation - 0.15 * smoothstep(0.5, 1.0, cl), 1.0, isSky)), 0.0);
    // warm highlights, soft cool-free shadows
    col *= mix(vec3(1.0), vec3(1.04, 1.0, 0.93), smoothstep(0.35, 1.0, cl));

    // Orton diffusion: soft copy, brightened, screen-blended
    vec3 soft = texture(SoftSampler, texCoord).rgb;
    // scene key: how bright this part of the world is (haze and edge glow follow it, so nights stay dark)
    float key = clamp(dot(soft, Luma) * 1.7 + 0.04, 0.0, 1.0);
    soft = soft * soft * 1.6;
    col = 1.0 - (1.0 - col) * (1.0 - soft * Orton * (1.0 - 0.7 * isSky));
    // restore a little contrast after the diffusion (gentle S around mid grey)
    col = mix(col, col * col * (3.0 - 2.0 * col), 0.35 * (1.0 - isSky));

    // luminous haze with distance (bright warm white, not grey)
    float haze = min(1.0 - exp(-dist * HazeDensity), HazeMax) * (1.0 - isSky);
    col = mix(col, HazeColor.rgb * key * (0.85 + 0.15 * cl), haze);

    // three-scale bloom, gold to white
    vec3 b1 = texture(BloomSampler, texCoord).rgb;
    vec3 b2 = texture(BloomMidSampler, texCoord).rgb;
    vec3 b3 = texture(BloomLargeSampler, texCoord).rgb;
    vec3 bloom = b1 * 0.5 + b2 * 0.8 * Gold.rgb + b3 * 1.1 * Gold.rgb * Gold.rgb;
    col = 1.0 - (1.0 - col) * (1.0 - clamp(bloom * BloomStrength * (1.0 - 0.5 * isSky), 0.0, 1.0));

    // light shafts + soft sun halo
    vec4 ray = texture(RaysSampler, texCoord);
    float shafts = ray.r * (1.0 - 0.6 * isSky);
    col = mix(col, col * vec3(1.06, 1.02, 0.92) + RayColor.rgb * 0.12, isSky * clamp(ray.g * 1.5, 0.0, 1.0));
    col += RayColor.rgb * (shafts * RayStrength + ray.g * 0.3 * RayStrength) * (1.0 - 0.5 * smoothstep(0.6, 1.0, cl));

    // light motes: a few soft bokeh discs drifting upward
    float secs = GameTime * 1200.0;
    vec2 aspect = vec2(InSize.x / InSize.y, 1.0);
    vec3 motes = vec3(0.0);
    for (int i = 0; i < 9; i++) {
        float fi = float(i);
        float sp = 0.012 + 0.018 * hash(vec2(fi, 1.3));
        float life = fract(secs * sp * 0.6 + hash(vec2(fi, 7.7)));
        vec2 p = vec2(hash(vec2(fi, 3.1)), 0.0);
        p.y = -0.1 + life * 1.2;
        p.x += 0.03 * sin(secs * 0.4 + fi * 2.1) + 0.02 * sin(secs * 0.23 + fi);
        float rad = 0.014 + 0.03 * hash(vec2(fi, 5.9));
        float dd = length((texCoord - p) * aspect) / rad;
        float disc = smoothstep(1.0, 0.7, dd) * (0.35 + 0.25 * smoothstep(0.6, 0.95, dd)) + exp(-dd * dd * 0.5) * 0.3;
        float fade = sin(life * 3.14159) * (0.6 + 0.4 * sin(secs * 1.7 + fi * 4.0));
        motes += mix(vec3(1.0, 0.86, 0.55), vec3(1.0, 0.97, 0.9), hash(vec2(fi, 9.1))) * disc * fade;
    }
    col += motes * Motes * (0.35 + 0.65 * key) * (1.0 - 0.75 * smoothstep(0.4, 0.9, dot(col, Luma)));

    // milky lifted blacks
    col = LiftColor.rgb * BlackLift + col * (1.0 - BlackLift);
    // bright soft vignette: edges glow toward warm white
    vec2 vc = (texCoord - 0.5) * vec2(1.0, 1.15);
    float edge = smoothstep(0.12, 0.42, dot(vc, vc));
    col = mix(col, HazeColor.rgb * key, edge * Vignette);
    // soft shoulder: highlights glow instead of clipping
    col = col / (1.0 + max(col - 0.9, 0.0) * 0.6);

    // --- living entities: thermal body + HP halo
    vec4 g = texture(GlowSampler, texCoord);
    vec4 f = texture(FillSampler, texCoord);
    float vote = 0.0;
    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            vote += marker(texCoord + vec2(float(x), float(y)) * px);
        }
    }
    float body = smoothstep(5.0, 7.0, vote) * smoothstep(0.01, 0.06, f.a) * (1.0 - isSky);

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
