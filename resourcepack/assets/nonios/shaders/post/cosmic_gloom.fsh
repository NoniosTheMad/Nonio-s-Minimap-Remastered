#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:cosmic, gloom pass = the FIRST Cosmic (v2, c65d643) star pass, verbatim (#64: restore the
// treetop gloom). Next to the moon every sky gap between dark leaves passes the star test; the 4 px
// glow, the spikes and the 24 px nebula blur of this image make the violet/teal gloom around treetops.
// Original header:
// isolate light sources in the sky.
// Stars = sky pixels brighter than their surroundings (small-scale high-pass),
// only where the surrounding sky is dark (so daytime clouds don't sparkle).
// Sun/moon = bright sky pixels. Out: rgb = light colour, a = star strength.
// Everything after this pass is derived from this image, so the glow and
// nebula clouds stay locked to the sky as you turn (no camera data needed).

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform StarConfig {
    float StarGain;       // high-pass gain
    float DarkSky;        // surrounding sky luma above which stars are ignored
    float BrightStart;    // luma where sun/moon pixels start to count
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);

float lumaAt(vec2 uv) {
    return dot(texture(InSampler, uv).rgb, Luma);
}

void main() {
    vec2 px = 1.0 / InSize;
    vec3 c = texture(InSampler, texCoord).rgb;
    float l = dot(c, Luma);

    float d = texture(DepthSampler, texCoord).r;
    float far = mix(1.0 - d, d, DepthReversed);
    float sky = 1.0 - step(1e-6, far);

    float ring = 0.0;
    for (int i = 0; i < 8; i++) {
        float a = float(i) * 0.785398;
        ring += lumaAt(texCoord + vec2(cos(a), sin(a)) * 3.0 * px);
    }
    ring /= 8.0;

    float gate = 1.0 - smoothstep(DarkSky * 0.6, DarkSky, ring);
    float star = clamp((l - ring - 0.02) * StarGain, 0.0, 1.0) * gate;
    float bright = smoothstep(BrightStart, 1.0, l);
    float s = max(star, bright) * sky;

    // normalise brightness so faint stars still glow in their own colour
    fragColor = vec4(min(c / max(l, 0.25), vec3(2.0)) * s, star * sky);
}
