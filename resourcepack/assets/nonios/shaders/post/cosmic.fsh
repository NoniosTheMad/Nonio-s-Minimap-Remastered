#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:cosmic v3, final pass - "magical light".
// Every light (pass 1) blooms at three scales, each with its own colour shift:
//   Small  = tight halo in the light's own colour,
//   Mid    = aura shifted toward violet/magenta,
//   Large  = soft spill shifted toward teal/blue (also falls on nearby terrain).
// The hue shifts drift slowly over time, the halos shimmer (animated noise), and small
// sharp lights sparkle with four-point glints. In the sky the large scale becomes nebula
// gloom (the v2 moon-behind-leaves aura is the same mechanism, now on purpose).
// Shadows get a cool lift and the sky a deep-space grade at night, so it stays playable.
// v4 (#55): + the v2 aura (moon behind leaves: violet -> teal glow around the tree, on the sky and on
// the leaves themselves), + a real night sky: a nebula and a star field fixed to the sky (decoded from
// the code the demo overlay sky.fsh hides in the sky colour), + a stronger moon with a corona.
// v5 (#64): the sky code is decoded by cosmic_code.fsh, which drops every pixel whose check bits fail
// (v4 read stars out of the clear colour below the horizon and out of the moon texture). The treetop gloom
// is the FIRST Cosmic's (v2) again, term for term: its star pass (cosmic_gloom.fsh), 4 px glow x3 with a
// slow twinkle, 14 px cross spikes, and the violet -> teal nebula from the 24 px blur (x40 gain), on the sky
// and spilled on the ground at the v2 strengths. It replaces the v4 re-creation (aura), which only had the
// nebula term.

uniform sampler2D InSampler;
uniform sampler2D LightSampler;
uniform sampler2D SmallSampler;
uniform sampler2D MidSampler;
uniform sampler2D LargeSampler;
uniform sampler2D AuraSampler;    // blurred sky code: g, b = nebula fields
uniform sampler2D CodeSampler;    // validated sky code: r = star level / 3
uniform sampler2D GloomSampler;   // v2 star pass
uniform sampler2D GGlowSampler;   // its 4 px blur
uniform sampler2D GNebSampler;    // its 24 px blur
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform CosmicConfig {
    vec4 SpaceColor;       // deep-space sky tint at night
    vec4 ShadowColor;      // cool lift in dark terrain
    vec4 AuraA;            // v2 gloom nebula: sparse colour (v2 NebulaA)
    vec4 AuraB;            // v2 gloom nebula: dense colour (v2 NebulaB)
    vec4 NebColA;          // sky nebula field A
    vec4 NebColB;          // sky nebula field B
    vec4 StarColor;
    float SmallStrength;
    float MidStrength;
    float LargeStrength;
    float MidHue;          // hue rotation (radians) of the mid aura
    float LargeHue;        // hue rotation of the large spill
    float HueDrift;        // extra rotation swing over time
    float Saturation;      // of the halos
    float Shimmer;         // animated noise on the halos (0..1)
    float SparkleStrength;
    float SparkleLength;   // pixels
    float Spill;           // how much large halo lights terrain
    float ShadowLift;
    float SpaceStrength;
    float AuraGain;        // v2 NebulaGain (40)
    float AuraStrength;    // v2 NebulaStrength (0.35)
    float AuraSpill;       // v2 Spill (0.35)
    float NebStrength;
    float StarStrength;
    float StarSpike;       // pixels
    float MoonCorona;
    float GloomStars;      // v2 StarBoost (1.2)
    float GloomGlow;       // v2 GlowStrength (3.0)
    float GloomSpike;      // v2 SpikeStrength (0.9)
    float GloomSpikeLength;// v2 SpikeLength (14 px)
    float GloomTwinkle;    // v2 Twinkle (0.25)
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);
const float TAU = 6.28318530718;

vec3 hueRotate(vec3 c, float a) {
    // rotation around the grey axis
    const vec3 k = vec3(0.57735);
    float ca = cos(a);
    return c * ca + cross(k, c) * sin(a) + k * dot(k, c) * (1.0 - ca);
}

vec3 saturate3(vec3 c, float s) {
    float l = dot(c, Luma);
    return max(mix(vec3(l), c, s), 0.0);
}

float hash(vec2 p) {
    return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453);
}

float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash(i), hash(i + vec2(1.0, 0.0)), f.x),
               mix(hash(i + vec2(0.0, 1.0)), hash(i + vec2(1.0, 1.0)), f.x), f.y);
}

// star level 0..3 from the validated sky code
float starAt(ivec2 p) {
    p = clamp(p, ivec2(0), ivec2(InSize) - 1);
    return floor(texelFetch(CodeSampler, p, 0).r * 3.0 + 0.5);
}

void main() {
    vec2 px = 1.0 / InSize;
    vec3 c = texture(InSampler, texCoord).rgb;
    float l = dot(c, Luma);

    float d = texture(DepthSampler, texCoord).r;
    float far = mix(1.0 - d, d, DepthReversed);
    float sky = 1.0 - step(1e-6, far);

    // time: GameTime is 0..1 per 24000 ticks; integer cycles keep it seamless
    float t = GameTime * TAU;
    float drift = sin(t * 40.0) * HueDrift;      // ~30 s swing

    // shimmer: two drifting noise layers (screen space)
    vec2 aspect = vec2(InSize.x / InSize.y, 1.0);
    float n1 = noise(texCoord * aspect * 9.0 + vec2(sin(t * 300.0), cos(t * 300.0)) * 0.8);
    float n2 = noise(texCoord * aspect * 23.0 - vec2(t * 600.0, t * 450.0));
    float shimmer = 1.0 + Shimmer * ((n1 - 0.5) * 1.2 + (n2 - 0.5) * 0.8);

    vec3 small = texture(SmallSampler, texCoord).rgb;
    vec3 mid = texture(MidSampler, texCoord).rgb;
    vec3 large = texture(LargeSampler, texCoord).rgb;

    small = saturate3(small, Saturation);
    mid = saturate3(hueRotate(mid, MidHue + drift), Saturation);
    large = saturate3(hueRotate(large, LargeHue - drift), Saturation);

    // sparkle: four-point glints on small sharp lights, twinkling
    vec3 glint = vec3(0.0);
    for (int i = 1; i <= 10; i++) {
        float k = float(i) / 10.0;
        vec2 o = vec2(k * SparkleLength) * px;
        vec2 od = o * 0.7071;
        float w = (1.0 - k) * (1.0 - k);
        vec4 a = texture(LightSampler, texCoord + vec2(o.x, 0.0)) + texture(LightSampler, texCoord - vec2(o.x, 0.0))
               + texture(LightSampler, texCoord + vec2(0.0, o.y)) + texture(LightSampler, texCoord - vec2(0.0, o.y));
        vec4 b = texture(LightSampler, texCoord + od) + texture(LightSampler, texCoord - od)
               + texture(LightSampler, texCoord + vec2(od.x, -od.y)) + texture(LightSampler, texCoord - vec2(od.x, -od.y));
        glint += (a.rgb * a.a + b.rgb * b.a * 0.35) * w;
    }
    float twinkle = 0.6 + 0.4 * sin(t * 900.0 + n1 * TAU * 2.0);
    glint *= SparkleStrength * twinkle / 8.0;

    vec3 halo = small * SmallStrength + (mid * MidStrength + large * LargeStrength) * shimmer;

    // --- night factor from the sky itself (dark sky = night); terrain uses the large halo's absence
    float dark = 1.0 - smoothstep(0.06, 0.35, l);

    // --- sky: deep-space grade + nebula gloom from the large scale
    vec3 skyCol = mix(c, c * SpaceColor.rgb * 2.0, dark * SpaceStrength);
    skyCol += halo + glint + large * LargeStrength * shimmer * dark;

    // --- terrain: light spill + cool shadow lift
    vec3 ground = c * (1.0 + large * Spill) + halo + glint;
    ground += ShadowColor.rgb * ShadowLift * (1.0 - smoothstep(0.0, 0.4, l));

    // --- the v2 gloom (first Cosmic, c65d643), same terms and strengths
    vec4 gStars = texture(GloomSampler, texCoord);
    vec3 gGlow = texture(GGlowSampler, texCoord).rgb;
    vec3 gNeb = texture(GNebSampler, texCoord).rgb;
    vec3 gSpikes = vec3(0.0);
    for (int i = 1; i <= 12; i++) {
        float k = float(i) / 12.0;
        vec2 o = vec2(k * GloomSpikeLength) * px;
        float w = (1.0 - k) * (1.0 - k);
        gSpikes += (texture(GloomSampler, texCoord + vec2(o.x, 0.0)).rgb + texture(GloomSampler, texCoord - vec2(o.x, 0.0)).rgb
                  + texture(GloomSampler, texCoord + vec2(0.0, o.y)).rgb + texture(GloomSampler, texCoord - vec2(0.0, o.y)).rgb) * w;
    }
    gSpikes /= 6.0;
    float gTw = 1.0 + GloomTwinkle * sin(GameTime * TAU * 600.0);
    float n = dot(gNeb, Luma) * AuraGain;
    vec3 auraCol = mix(AuraA.rgb, AuraB.rgb, smoothstep(0.3, 2.0, n)) * smoothstep(0.0, 1.0, n);
    vec3 gLight = gStars.rgb * GloomStars + gGlow * GloomGlow * gTw + gSpikes * GloomSpike;
    skyCol += gLight + auraCol * AuraStrength;
    ground += auraCol * AuraStrength * AuraSpill + gGlow * GloomGlow * AuraSpill;
    vec4 aura = texture(AuraSampler, texCoord);

    // --- night sky: nebula + star field (sky code, fixed to world directions)
    float night = dark * sky;
    vec3 neb = NebColA.rgb * aura.g + NebColB.rgb * aura.b;
    neb *= 0.75 + 0.5 * n1;
    skyCol += neb * NebStrength * night;
    ivec2 ip = ivec2(gl_FragCoord.xy);
    float s0 = starAt(ip) / 3.0;
    float soft = 0.0;
    float spike = 0.0;
    for (int i = 1; i <= 7; i++) {
        float k = float(i) / 8.0;
        int o = max(1, int(float(i) * StarSpike / 7.0));
        float m = max(max(starAt(ip + ivec2(o, 0)), starAt(ip - ivec2(o, 0))), max(starAt(ip + ivec2(0, o)), starAt(ip - ivec2(0, o))));
        spike += step(2.5, m) * (1.0 - k) * (1.0 - k);       // only the brightest stars (level 3) get spikes
        if (i <= 2) soft += m / 3.0 * (i == 1 ? 0.5 : 0.25); // small soft glow on every star
    }
    float tw = 0.65 + 0.35 * sin(t * 1300.0 + hash(floor(gl_FragCoord.xy / 3.0)) * TAU);
    skyCol += StarColor.rgb * ((s0 * s0 + soft * 0.5) * StarStrength * tw + spike * 0.3) * night;

    // --- moon: brighter disc + cool corona (mid/large halos of the bright sky light)
    float moon = smoothstep(0.55, 0.9, l) * sky;
    skyCol += skyCol * moon * vec3(0.25, 0.3, 0.4);
    skyCol += (mid * 0.6 + large) * MoonCorona * vec3(0.75, 0.88, 1.15) * night;

    vec3 col = mix(ground, skyCol, sky);
    // soft shoulder instead of a hard clip, keeps halo colours
    col = col / (1.0 + max(col - 1.0, 0.0) * 0.5);
    fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}
