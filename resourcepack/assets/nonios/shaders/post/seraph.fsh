#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:angel v5 ("seraph") - composite. Built from scratch in tools/shaderlab against the user's own
// reference (demos/shaders/reference/angel_gemini_user.jpg): golden god rays streaming diagonally from a
// bright upper-right light, a strong warm bloom, drifting motes/sparkles (denser in the beams), a pastel
// lavender-gold haze that lifts distance and shadows, a slight rainbow fringe on beams and highlights.
// Terms, in order:
//  - day key: the average brightness of the soft copy (16 taps) -> day (gold) vs night (silver-lavender);
//    every light term scales with it, so nights stay dark and moonlit instead of grey,
//  - night gain: exposure x NightGain when the day key is low (the world stays readable, moonlit),
//  - gilding (Gild): green-dominant pixels pushed toward amber, again after the light terms so gold light over
//    leaves reads cream-gold, never lime (by day only; at night foliage stays silver),
//  - chromatic aberration: R and B sampled slightly apart, radially, only where the image is bright,
//  - pastel split toning: shadows tinted lilac, highlights cream-gold, the range lifted (high key),
//  - Orton diffusion: the soft copy screen-blended back (luminous surfaces),
//  - aerial haze: 1 - exp(-density * dist) toward a lavender->gold haze colour, brighter by day,
//  - bloom: 3 downsampled scales, gold, screen blend,
//  - god rays (seraph_rays): gold shafts; R and B are read a little apart along the radial direction
//    (taken from the halo gradient) so each beam edge splits into a soft rainbow; a halo and a faint
//    prism arc around the light centre,
//  - motes: many tiny sparkles + a few large soft bokeh discs drifting up, weighted toward the beams,
//  - lifted milky blacks, bright warm edge glow, soft highlight shoulder, near-white settled on cream,
//  - living entities with HP: unchanged from Angel v4 (entity-marker body in HP-tinted ironbow, HP halo,
//    white-hot outline core), see angel.fsh.

uniform sampler2D InSampler;
uniform sampler2D Bloom1Sampler;
uniform sampler2D Bloom2Sampler;
uniform sampler2D Bloom3Sampler;
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

layout(std140) uniform SeraphConfig {
    vec4 Gold;           // bloom / ray tint by day
    vec4 Silver;         // the same by night (moonlight)
    vec4 Lavender;       // shadow lift / haze far colour
    float Exposure;
    float BloomStrength;
    float RayStrength;
    float Spectral;      // rainbow fringe across the beams
    float HazeDensity;
    float HazeMax;
    float Orton;
    float Contrast;
    float BlackLift;
    float Saturation;
    float Golden;        // tri-tone grade amount
    float Aberration;    // px at the screen edge
    float Motes;
    float Vignette;
    float GlowStrength;  // HP halo
    float BodyHeat;
    float CoreWhite;
    float MinBright;
    float Tolerance;
    float Near;
    float DepthReversed;
    float Gild;          // green foliage -> gold (hue push of green toward amber)
    float NightGain;     // exposure lift at night (moonlit, not black)
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

vec3 spectrum(float x) {
    // pastel prism 0..1: rose -> gold -> sky cyan -> lavender (no lime: green fringes read as sickly)
    vec3 a = vec3(1.0, 0.62, 0.72);
    vec3 b = vec3(1.0, 0.86, 0.5);
    vec3 c = vec3(0.62, 0.88, 1.0);
    vec3 d = vec3(0.8, 0.66, 1.0);
    x = fract(x) * 4.0;
    vec3 col = x < 1.0 ? mix(a, b, x) : x < 2.0 ? mix(b, c, x - 1.0) : x < 3.0 ? mix(c, d, x - 2.0) : mix(d, a, x - 3.0);
    return col;
}

float marker(vec2 uv) {
    vec3 q = floor(texture(InSampler, uv).rgb * 255.0 + 0.5);
    vec3 par = mod(q, 2.0);
    return (par.r > 0.5 && par.g < 0.5 && par.b > 0.5) ? 1.0 : 0.0;
}

float closeness(vec3 n, vec3 team) {
    return 1.0 - smoothstep(0.1, 0.35, distance(n, team));
}

vec3 screen(vec3 a, vec3 b) {
    return 1.0 - (1.0 - a) * (1.0 - clamp(b, 0.0, 1.0));
}

void main() {
    vec2 px = 1.0 / InSize;
    vec2 aspect = vec2(InSize.x / InSize.y, 1.0);
    vec3 c0 = texture(InSampler, texCoord).rgb;
    float l0 = dot(c0, Luma);

    float d = texture(DepthSampler, texCoord).r;
    float z = mix(1.0 - d, d, DepthReversed);
    float isSky = 1.0 - step(1e-6, z);
    float dist = Near / max(z, 1e-6);

    // --- day key: average of the soft copy
    float avg = 0.0;
    for (int y = 0; y < 4; y++) {
        for (int x = 0; x < 4; x++) {
            avg += dot(texture(SoftSampler, (vec2(x, y) + 0.5) / 4.0).rgb, Luma);
        }
    }
    avg /= 16.0;
    float day = smoothstep(0.12, 0.4, avg);
    vec3 warm = mix(Silver.rgb, Gold.rgb, day);
    vec3 soft = texture(SoftSampler, texCoord).rgb;
    soft = mix(vec3(dot(soft, Luma)), soft, 0.35) * mix(Silver.rgb, Gold.rgb * 1.1, day);   // warm diffusion
    float key = clamp(dot(soft, Luma) * 1.6 + 0.03, 0.0, 1.0);   // local brightness

    // --- chromatic aberration on bright areas
    vec2 rc = texCoord - 0.5;
    vec2 ca = rc * px * Aberration * 2.0 * smoothstep(0.45, 0.9, l0);
    vec3 c = vec3(texture(InSampler, texCoord + ca).r, c0.g, texture(InSampler, texCoord - ca).b);
    vec3 col = c * Exposure * mix(NightGain, 1.0, day);
    // hue-preserving shoulder: the gain must not push lava / lamps / end rods past 1 (the S-curve below
    // turns values > 1.5 negative: lava went green, bright particles black)
    float cm = max(col.r, max(col.g, col.b));
    col *= cm > 0.8 ? (0.8 + 0.2 * (1.0 - exp(-(cm - 0.8) / 0.2))) / cm : 1.0;

    // --- gilding: greens lean to pale glowing gold-green (hue AND luminance), keeping a hint of green
    float gx = max(col.g - max(col.r, col.b), 0.0);
    col.r += gx * Gild * mix(0.2, 0.7, day);
    col.b += gx * Gild * 0.15 * day;
    col *= 1.0 + min(gx, 0.12) * Gild * 1.6 * day;   // dark leaves glow, bright grass is not blown to chartreuse
    col = max(col, 0.0);

    // --- pastel grade
    float cl = dot(col, Luma);
    col = max(mix(vec3(cl), col, mix(Saturation, 1.0, 0.4 * isSky)), 0.0);
    // split toning (pastel, high key): shadows pulled toward lilac, highlights toward cream-gold, the
    // whole range lifted (screen) so the image is airy; hues survive (green stays a pale gold-green)
    float tl = clamp(cl * 1.2, 0.0, 1.0);
    vec3 shadowTint = Lavender.rgb / max(dot(Lavender.rgb, Luma), 0.01);
    vec3 hiTint = mix(warm, vec3(1.0), 0.35) / max(dot(mix(warm, vec3(1.0), 0.35), Luma), 0.01);
    vec3 tinted = col * mix(shadowTint, hiTint, smoothstep(0.15, 0.75, tl));
    col = mix(col, tinted, Golden * (1.0 - 0.7 * isSky));
    // v5b: no global lift. Highlights pushed warm-gold, shadows keep their depth (only tinted, never raised)
    float hiW = smoothstep(0.45, 0.95, tl) * day * (1.0 - isSky);
    col = screen(col, warm * hiW * Golden * 0.35);

    // --- Orton diffusion
    float softL = dot(soft, Luma);
    col = screen(col, soft * smoothstep(0.35, 0.85, softL) * 1.5 * Orton * (1.0 - 0.6 * isSky));
    col = clamp(col, 0.0, 1.0);
    col = mix(col, col * col * (3.0 - 2.0 * col), Contrast * (1.0 - isSky));

    // --- aerial haze toward a lavender-gold glow (bright by day, dim by night)
    float haze = min(1.0 - exp(-dist * HazeDensity), HazeMax) * smoothstep(24.0, 96.0, dist) * (1.0 - isSky);
    vec3 hazeCol = mix(Lavender.rgb, warm, 0.2) * mix(0.25, 1.05, key) * mix(0.5, 1.0, day);
    col = mix(col, hazeCol, haze);

    // --- bloom
    vec3 b1 = texture(Bloom1Sampler, texCoord).rgb;
    vec3 b2 = texture(Bloom2Sampler, texCoord).rgb;
    vec3 b3 = texture(Bloom3Sampler, texCoord).rgb;
    vec3 bloom = b1 * 0.6 + b2 * 0.9 + b3 * 1.3;
    bloom = mix(vec3(dot(bloom, Luma)), bloom, 0.25) * warm;   // light, not leaf colour: no lime halos
    col = screen(col, bloom * BloomStrength * (1.0 - 0.45 * isSky));

    // --- god rays with a spectral fringe, halo
    vec4 ray = texture(RaysSampler, texCoord);
    // radial direction toward the light = gradient of the halo (g falls off with distance from the centre)
    vec2 e = vec2(4.0 / 320.0, 4.0 / 180.0);
    vec2 grad = vec2(texture(RaysSampler, texCoord + vec2(e.x, 0.0)).g - texture(RaysSampler, texCoord - vec2(e.x, 0.0)).g,
                     texture(RaysSampler, texCoord + vec2(0.0, e.y)).g - texture(RaysSampler, texCoord - vec2(0.0, e.y)).g);
    vec2 toLight = grad / max(length(grad), 1e-5);
    // prism split: red sampled a little farther out than blue (each beam edge gets a soft rainbow)
    vec2 sp = toLight * 0.012 * Spectral * (0.6 + 0.8 * smoothstep(0.3, 0.75, ray.r));
    vec3 shafts3 = vec3(texture(RaysSampler, texCoord - sp).r, ray.r, texture(RaysSampler, texCoord + sp).r) * mix(0.7, 1.0, day);
    float bright = smoothstep(0.3, 0.75, ray.r);
    vec3 rayCol = mix(warm, spectrum(ray.b) * mix(0.8, 1.0, day), Spectral * (0.15 + 0.6 * bright));
    float dampen = (1.0 - 0.45 * smoothstep(0.65, 1.0, cl)) * (1.0 - 0.35 * isSky);
    col = screen(col, rayCol * shafts3 * RayStrength * dampen);
    col = screen(col, warm * ray.g * 0.3 * RayStrength * mix(0.4, 1.0, day));
    // a faint prism arc around the light (a ring at one halo level, coloured across its width)
    float arcX = (ray.g - 0.22) / 0.07;
    float arc = exp(-arcX * arcX) * Spectral * day;
    col = screen(col, spectrum(0.5 + arcX * 0.18) * arc * 0.22);

    // --- motes: sparkles (many, tiny) + bokeh (few, large), drifting up, denser in the beams
    float secs = GameTime * 1200.0;
    vec3 motes = vec3(0.0);
    // sparkles: a grid of cells in drifting space, one point per cell
    for (int layer = 0; layer < 3; layer++) {
        float fl = float(layer);
        float cells = 16.0 + 12.0 * fl;
        vec2 p = texCoord * aspect * cells;
        p.y -= secs * (0.12 + 0.08 * fl);
        p.x += sin(secs * 0.3 + fl * 2.0 + texCoord.y * 4.0) * 0.4;
        vec2 id = floor(p);
        vec2 f = fract(p);
        float h = hash(id + fl * 31.0);
        if (h < 0.75) {
            vec2 pos = vec2(hash(id + 3.1 + fl), hash(id + 7.3 + fl)) * 0.7 + 0.15;
            float rr = length(f - pos);
            float tw = 0.5 + 0.5 * sin(secs * (2.0 + 3.0 * h) + h * 40.0);
            float size = 0.07 + 0.1 * hash(id + 9.9);
            float s = smoothstep(size, 0.0, rr) + 0.25 * exp(-rr * rr / (size * size * 6.0));
            motes += mix(vec3(1.0, 0.72, 0.32), vec3(1.0, 0.92, 0.7), hash(id + 5.5)) * s * tw * 1.4;
        }
    }
    vec3 bokeh = vec3(0.0);
    for (int i = 0; i < 10; i++) {
        float fi = float(i);
        float sp = 0.012 + 0.016 * hash(vec2(fi, 1.3));
        float life = fract(secs * sp * 0.5 + hash(vec2(fi, 7.7)));
        vec2 p = vec2(hash(vec2(fi, 3.1)) * aspect.x, -0.1 + life * 1.2);
        p.x += 0.04 * sin(secs * 0.3 + fi * 2.1);
        float rad = 0.02 + 0.035 * hash(vec2(fi, 5.9));
        float dd = length(texCoord * aspect - p) / rad;
        float disc = smoothstep(1.0, 0.8, dd) * (0.25 + 0.2 * smoothstep(0.6, 0.98, dd));
        bokeh += mix(vec3(1.0, 0.85, 0.6), vec3(0.95, 0.9, 1.0), hash(vec2(fi, 9.1))) * disc * sin(life * 3.14159);
    }
    float inBeam = smoothstep(0.08, 0.45, ray.r);
    vec3 m = motes * (0.03 + 1.2 * inBeam) * (1.0 - 0.8 * isSky) + bokeh * (0.4 + 0.6 * inBeam);
    col = screen(col, m * Motes * warm * mix(0.3, 1.0, key));

    // --- gild again after the light terms: gold light over olive leaves must read cream-gold, not lime
    float gy = max(col.g - max(col.r, col.b), 0.0) * (1.0 - isSky);
    col += gy * Gild * day * vec3(0.6, -0.1, 0.0);

    // --- milky lift, bright edges, shoulder
    // night: a stronger silver-lavender lift so the moonlit world reads instead of going black
    vec3 liftCol = mix(mix(Silver.rgb, Lavender.rgb, 0.5) * 0.42, Lavender.rgb * 0.75, day);
    float shadowW = 1.0 - smoothstep(0.0, 0.4, dot(col, Luma));
    col = mix(col, col * shadowTint, 0.35 * Golden * shadowW * day);   // lavender in the shadows, depth kept
    col = mix(col, liftCol, BlackLift * mix(3.0, 1.0, day) * shadowW * mix(1.0, 0.35, day));
    vec2 vc = rc * vec2(1.0, 1.15);
    float edge = smoothstep(0.12, 0.45, dot(vc, vc));
    col = mix(col, hazeCol * 1.1, edge * Vignette * smoothstep(0.3, 0.8, dot(col, Luma)));
    col = col / (1.0 + max(col - 0.92, 0.0) * 0.7);
    // nothing reaches paper white: the brightest areas (sun flood) settle on cream
    float wht = smoothstep(0.82, 0.98, min(col.r, min(col.g, col.b)));
    col = mix(col, vec3(1.0, 0.95, 0.84) * max(col.r, max(col.g, col.b)), wht * 0.6 * day);

    // --- living entities: thermal body + HP halo (Angel v4, unchanged)
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
    vec3 thermal = ironbow(0.35 + l0 * 0.65) * mix(vec3(1.0), tn, 0.35);
    col = mix(col, thermal, body * BodyHeat);

    vec3 gn = g.rgb / max(max(g.r, max(g.g, g.b)), 1e-4);
    float heartbeat = pow(wave(1440.0), 6.0);
    float pulse = 1.0 + closeness(gn, RED) * 1.2 * heartbeat + closeness(gn, PURPLE) * 0.8 * wave(2400.0)
                + closeness(gn, AQUA) * 1.6 * wave(4200.0);
    col += g.rgb * GlowStrength * pulse;

    float mx = max(c0.r, max(c0.g, c0.b));
    vec3 n = c0 / max(mx, 1e-4);
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
