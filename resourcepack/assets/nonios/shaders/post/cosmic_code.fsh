#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:cosmic - decode the sky code (written by the demo overlay's core/sky.fsh, see nonios_sky_code in
// nonios_mark.glsl) and keep it only where it is real.
// v4 trusted the low bits of every sky pixel (#64): the clear colour below the horizon decoded as a wall of
// stars (white static), and the moon, blended on top of the coded sky, as a striped "symbol". Each code now
// carries a check bit (parity XOR a per-pixel key); a pixel counts only if it and its 12 nearest neighbours
// (3x3 + the 4 at distance 2) all pass. Random or constant low bits pass that with odds ~1/8000.
// Out: r = star level / 3, g = nebula A (0..1), b = nebula B (0..1), a = valid.

// same as nonios_key in the overlay's nonios_mark.glsl (inlined: the game pack must not need the overlay)
int nonios_key(ivec2 p) {
    uint h = uint(p.x) * 1973u + uint(p.y) * 9277u + 7u;
    h ^= h >> 7u;
    h *= 0x2c1b3c6du;
    h ^= h >> 12u;
    return int((h >> 3u) & 1u);
}

uniform sampler2D InSampler;
uniform sampler2D DepthSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform CodeConfig {
    float DepthReversed;
};

layout(location = 0) out vec4 fragColor;

ivec3 bitsAt(ivec2 p) {
    return ivec3(floor(texelFetch(InSampler, p, 0).rgb * 255.0 + 0.5)) & 3;
}

bool ok(ivec2 p) {
    ivec2 sz = ivec2(InSize) - 1;
    if (p.x < 0 || p.y < 0 || p.x > sz.x || p.y > sz.y) return true;   // screen edge: don't punish
    float d = texelFetch(DepthSampler, p, 0).r;
    if (mix(1.0 - d, d, DepthReversed) >= 1e-6) return false;         // geometry
    ivec3 q = bitsAt(p);
    int chk = nonios_key(p) ^ (q.r & 1) ^ (q.r >> 1) ^ (q.g & 1) ^ (q.b & 1) ^ (q.b >> 1);
    return chk == (q.g >> 1);
}

void main() {
    ivec2 p = ivec2(gl_FragCoord.xy);
    bool valid = true;
    for (int y = -1; y <= 1; y++)
        for (int x = -1; x <= 1; x++)
            valid = valid && ok(p + ivec2(x, y));
    valid = valid && ok(p + ivec2(2, 0)) && ok(p - ivec2(2, 0)) && ok(p + ivec2(0, 2)) && ok(p - ivec2(0, 2));
    if (!valid) {
        fragColor = vec4(0.0);
        return;
    }
    ivec3 q = bitsAt(p);
    fragColor = vec4(float(q.b) / 3.0, float(q.r) / 3.0, float(q.g & 1), 1.0);
}
