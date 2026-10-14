#version 330
#extension GL_ARB_separate_shader_objects : require

#include <minecraft:globals.glsl>

// nonios:cosmic, final pass - "the stars are alive".
// Sky: stars get a soft glow + four-point diffraction spikes, and nebula
// clouds grow out of the star density (large blur of the star image, coloured
// violet -> teal by how clustered it is), so they move with the sky.
// Ground: starlight spills over silhouettes, shadows get a cool blue lift and
// a violet/teal grade, so nights stay playable. Best at night (Midnight).

uniform sampler2D InSampler;
uniform sampler2D StarsSampler;
uniform sampler2D GlowSampler;
uniform sampler2D NebulaSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform CosmicConfig {
    vec4 StarLight;        // colour of the light the sky casts on the ground
    vec4 NebulaA;          // sparse nebula colour
    vec4 NebulaB;          // dense nebula colour
    float StarBoost;
    float GlowStrength;
    float SpikeStrength;
    float SpikeLength;     // pixels
    float NebulaGain;
    float NebulaStrength;
    float Spill;           // how much nebula light falls on terrain
    float ShadowLift;      // cool lift of dark terrain
    float Twinkle;
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);
const float TAU = 6.28318530718;

void main() {
    vec2 px = 1.0 / InSize;
    vec3 c = texture(InSampler, texCoord).rgb;
    float l = dot(c, Luma);

    float d = texture(DepthSampler, texCoord).r;
    float far = mix(1.0 - d, d, DepthReversed);
    float sky = 1.0 - step(1e-6, far);

    vec4 stars = texture(StarsSampler, texCoord);
    vec3 glow = texture(GlowSampler, texCoord).rgb;
    vec3 neb = texture(NebulaSampler, texCoord).rgb;

    // --- diffraction spikes (+ shape), fading with distance from the star
    vec3 spikes = vec3(0.0);
    for (int i = 1; i <= 12; i++) {
        float k = float(i) / 12.0;
        vec2 o = vec2(k * SpikeLength) * px;
        float w = (1.0 - k) * (1.0 - k);
        spikes += (texture(StarsSampler, texCoord + vec2(o.x, 0.0)).rgb
                 + texture(StarsSampler, texCoord - vec2(o.x, 0.0)).rgb
                 + texture(StarsSampler, texCoord + vec2(0.0, o.y)).rgb
                 + texture(StarsSampler, texCoord - vec2(0.0, o.y)).rgb) * w;
    }
    spikes /= 6.0;

    // --- slow global twinkle (~0.5 Hz breathing of the glow)
    float tw = 1.0 + Twinkle * sin(GameTime * TAU * 600.0);

    // --- nebula colour from star density
    float n = dot(neb, Luma) * NebulaGain;
    vec3 nebCol = mix(NebulaA.rgb, NebulaB.rgb, smoothstep(0.3, 2.0, n)) * smoothstep(0.0, 1.0, n);

    vec3 light = stars.rgb * StarBoost + glow * GlowStrength * tw + spikes * SpikeStrength;

    // --- sky
    vec3 skyCol = c + light + nebCol * NebulaStrength;

    // --- ground: starlight spill + cool shadow lift + grade
    vec3 ground = c + nebCol * NebulaStrength * Spill + glow * GlowStrength * Spill;
    ground += StarLight.rgb * ShadowLift * (1.0 - smoothstep(0.0, 0.45, l));
    float gl = dot(ground, Luma);
    ground *= mix(vec3(0.92, 0.95, 1.12), vec3(1.06, 0.98, 1.08), smoothstep(0.1, 0.8, gl));

    vec3 col = mix(ground, skyCol, sky);
    fragColor = vec4(clamp(col, 0.0, 1.0), 1.0);
}
