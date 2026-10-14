#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:thermal, pass 1 - find the heat SOURCES from the markers the shaders-demo core shaders hide in
// the two lowest bits of every colour channel (see include/nonios_mark.glsl):
//   entity   tag 1,0,1  -> warm-blooded body (emissive layers hotter)
//   terrain  tag 0,1,0  -> heat 0..7, non-zero only on light-emitting blocks (lava, fire, torch, glowstone...)
//   particle tag 1,1,0  -> heat 0..7 (flames)
// Nothing else is hot here: warmth around a source comes from blurring this mask (later passes).
// A pixel counts only if most neighbours carry the same tag, and a hot block pixel must also be bright on
// screen (emitters always are), so stray low bits can't speckle. The hand / held item (closer than
// HandDist blocks) is masked out and later drawn neutral.
// Out: r = source heat 0..1, g = same (bloom source), b = hand mask, a = 1.

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform HeatConfig {
    float EntityHeat;     // body heat (0..1)
    float Near;           // camera near plane in blocks
    float HandDist;       // closer than this (blocks) = hand / held item
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
    float z = mix(1.0 - d, d, DepthReversed);
    bool sky = z < 1e-6;
    float dist = Near / max(z, 1e-6);
    if (!sky && dist < HandDist) {
        fragColor = vec4(0.0, 0.0, 1.0, 1.0);
        return;
    }
    if (sky) {
        // the sun is hot, the moon is not (it is grey-blue, the sun is warm)
        float sun = smoothstep(0.88, 1.0, l) * smoothstep(0.08, 0.2, c.r - c.b);
        fragColor = vec4(sun * 0.9, sun * 0.9, 0.0, 1.0);
        return;
    }

    ivec3 q0 = codeAt(p);
    int t0 = tagOf(q0);
    int h0 = heatOf(q0);
    int agree = 0;
    for (int y = -1; y <= 1; y++) {
        for (int x = -1; x <= 1; x++) {
            if (x == 0 && y == 0) continue;
            ivec3 q = codeAt(p + ivec2(x, y));
            if (tagOf(q) != t0) continue;
            if (t0 == 1 || abs(heatOf(q) - h0) <= 2) agree++;
        }
    }

    float heat = 0.0;
    if (t0 == 1 && agree >= 4) {
        heat = h0 == 7 ? 0.95 : EntityHeat + 0.12 * l;
    } else if (t0 == 2 && agree >= 5 && h0 >= 3) {
        heat = (0.55 + 0.45 * float(h0) / 7.0) * smoothstep(0.3, 0.55, l);
    } else if (t0 == 3 && agree >= 3 && h0 >= 3) {
        heat = (0.55 + 0.45 * float(h0) / 7.0) * smoothstep(0.3, 0.55, l);
    }
    fragColor = vec4(heat, heat, 0.0, 1.0);
}
