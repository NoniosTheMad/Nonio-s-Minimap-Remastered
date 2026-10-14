#version 330
#extension GL_ARB_separate_shader_objects : require

// nonios:hp_sig - find HP "heat signatures" (used by Alien and Angel).
// Post effects can't read health, so the datapack encodes it: entities glow
// (vanilla Glowing) and their team colour = HP bracket. The vanilla outline is
// composited into the main image before /posteffect shaders run, so this pass
// keys on those team colours (compared after normalising brightness, since the
// outline is drawn at varying intensity).
// Out: rgb = bracket colour * match, a = match. Blurred next into a halo.

uniform sampler2D InSampler;

layout(location = 0) in vec2 texCoord;

layout(std140) uniform SamplerInfo {
    vec2 OutSize;
    vec2 InSize;
};

layout(std140) uniform SignatureConfig {
    float MinBright;   // ignore pixels darker than this
    float Tolerance;   // max distance to a team colour (normalised RGB)
};

layout(location = 0) out vec4 fragColor;

// Team colours: red, gold, green, light_purple, aqua (= HP low, mid, ok, > 20 hearts, > 40 hearts).
const vec3 TEAM[5] = vec3[5](
    vec3(1.0, 0.333, 0.333),
    vec3(1.0, 0.667, 0.0),
    vec3(0.333, 1.0, 0.333),
    vec3(1.0, 0.333, 1.0),
    vec3(0.333, 1.0, 1.0)
);

void main() {
    vec3 c = texture(InSampler, texCoord).rgb;
    float m = max(c.r, max(c.g, c.b));
    vec3 n = c / max(m, 1e-4);
    float best = 1e9;
    vec3 col = vec3(0.0);
    for (int i = 0; i < 5; i++) {
        float dd = distance(n, TEAM[i]);
        if (dd < best) {
            best = dd;
            col = TEAM[i];
        }
    }
    float w = (1.0 - smoothstep(Tolerance * 0.5, Tolerance, best))
            * smoothstep(MinBright, MinBright + 0.15, m);
    fragColor = vec4(col * w, w);
}
