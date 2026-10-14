#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:thermal, pass 1 - read the heat markers the shaders-demo core shaders hide in the two lowest
// bits of every colour channel (see include/nonios_mark.glsl):
//   entity   tag 1,0,1  -> warm-blooded (every entity body, incl. your hand), emissive layers hottest
//   terrain  tag 0,1,0  -> heat 0..7 from block light + texture (lava, fire, torch flames, glowstone,
//                          magma, lanterns are hot; blocks next to a light are warm)
//   particle tag 1,1,0  -> heat 0..7 (flames)
// Blended surfaces (water, glass, clouds, shadows) carry no valid code: they read as cold.
// A pixel is trusted only if enough neighbours carry the same tag (and a similar heat), so random
// low bits from blended pixels don't speckle.
// Out: r = heat 0..1, g = hot mask (bloom source), b = entity, a = 1.

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform HeatConfig {
    float EntityHeat;     // base heat of an entity body (0..1)
    float ColdLuma;       // how much brightness warms unmarked surfaces
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

const vec3 Luma = vec3(0.2126, 0.7152, 0.0722);

ivec3 codeAt(ivec2 p) {
    ivec2 sz = ivec2(InSize) - 1;
    vec3 c = texelFetch(InSampler, clamp(p, ivec2(0), sz), 0).rgb;
    return ivec3(floor(c * 255.0 + 0.5));
}

// 0 none, 1 entity, 2 terrain, 3 particle
int tagOf(ivec3 q) {
    ivec3 lo = q & 1;
    ivec3 hi = (q >> 1) & 1;
    if (lo == ivec3(1, 0, 1) && hi.r == hi.g && hi.g == hi.b) return 1;
    if (lo == ivec3(0, 1, 0)) return 2;
    if (lo == ivec3(1, 1, 0)) return 3;
    return 0;
}

int heatOf(ivec3 q) {
    ivec3 hi = (q >> 1) & 1;
    return hi.r + 2 * hi.g + 4 * hi.b;
}

void main() {
    ivec2 p = ivec2(gl_FragCoord.xy);
    vec3 c = texelFetch(InSampler, p, 0).rgb;
    float l = dot(c, Luma);

    float d = texelFetch(DepthSampler, p, 0).r;
    float far = mix(1.0 - d, d, DepthReversed);
    bool sky = far < 1e-6;

    ivec3 q0 = codeAt(p);
    int t0 = tagOf(q0);
    int h0 = heatOf(q0);
    int agree = 0;
    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            if (x == 0 && y == 0) continue;
            ivec3 q = codeAt(p + ivec2(x, y));
            if (tagOf(q) != t0) continue;
            if (t0 == 1 || abs(heatOf(q) - h0) <= 1) agree++;
        }
    }

    float heat;
    float entity = 0.0;
    if (sky) {
        heat = smoothstep(0.9, 1.0, l) * 0.9;                        // the sun disc
    } else if (t0 == 1 && agree >= 3) {
        entity = 1.0;
        heat = h0 == 7 ? 1.0 : EntityHeat + (1.0 - EntityHeat) * l;  // eyes / glowing layers hottest
    } else if ((t0 == 2 && agree >= 4) || (t0 == 3 && agree >= 3)) {
        heat = float(h0) / 7.0;
    } else {
        heat = l * ColdLuma;                                          // water, glass, clouds: cold
    }
    fragColor = vec4(heat, smoothstep(0.45, 0.95, heat), entity, 1.0);
}
