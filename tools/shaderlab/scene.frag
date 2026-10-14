#version 330
#include <minecraft:nonios_mark.glsl>
// shaderlab test scene: a small Minecraft-like voxel world, ray-marched (DDA).
// Outputs colour (with the demo overlay's invisible low-bit markers, like the real game) and a
// reversed-Z depth (d = Near / viewZ, sky = 0), the same format the pack's post shaders read.

uniform vec2 Res;
uniform vec3 CamPos;
uniform vec2 CamRot;      // yaw, pitch (radians)
uniform float TanHalfFov; // vertical
uniform float DayTime;    // 0 noon .. 0.5 midnight
uniform float Time;       // seconds (torch flicker)
uniform float Near;
uniform float RenderDist;

layout(location = 0) out vec4 outColor;
layout(location = 1) out vec4 outDepth;

float hash13(vec3 p3) {
    p3 = fract(p3 * 0.1031);
    p3 += dot(p3, p3.zyx + 31.32);
    return fract((p3.x + p3.y) * p3.z);
}
float hash12(vec2 p) { return hash13(vec3(p, 17.0)); }
float vnoise(vec2 p) {
    vec2 i = floor(p), f = fract(p);
    f = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash12(i), hash12(i + vec2(1, 0)), f.x), mix(hash12(i + vec2(0, 1)), hash12(i + vec2(1, 1)), f.x), f.y);
}
float height(vec2 xz) {
    float h = 64.0 + 9.0 * vnoise(xz / 48.0) + 4.0 * vnoise(xz / 17.0) + 18.0 * smoothstep(0.55, 0.9, vnoise(xz / 140.0 + 3.1));
    return floor(h);
}
// tree at a 9x9 cell: trunk position
bool treeAt(vec2 cell, out vec3 base) {
    float h = hash12(cell * 1.31 + 5.0);
    vec2 o = floor(vec2(hash12(cell + 2.3), hash12(cell + 7.9)) * 5.0) + 2.0;
    vec2 xz = cell * 9.0 + o;
    base = vec3(xz.x, height(xz) + 1.0, xz.y);
    return h < 0.55;
}
// block ids: 0 air, 1 grass, 2 dirt, 3 stone, 4 log, 5 leaves, 6 glowstone (light), 7 lantern post, 8 flower
int block(vec3 p) {
    float h = height(p.xz);
    if (p.y < h - 3.0) return 3;
    if (p.y < h) return 2;
    if (p.y < h + 1.0) return 1;
    // trees
    vec2 c = floor(p.xz / 9.0);
    for (int dx = -1; dx <= 1; dx++)
    for (int dz = -1; dz <= 1; dz++) {
        vec3 b;
        vec2 cc = c + vec2(dx, dz);
        if (!treeAt(cc, b)) continue;
        vec3 q = p - b;
        float th = 4.0 + floor(hash12(cc + 9.1) * 3.0);
        if (q.x == 0.0 && q.z == 0.0 && q.y >= 0.0 && q.y < th) return 4;
        float ly = q.y - (th - 2.0);
        if (ly >= 0.0 && ly <= 3.0) {
            float r = ly >= 2.0 ? 1.0 : 2.0;
            if (abs(q.x) <= r && abs(q.z) <= r) {
                bool corner = abs(q.x) == r && abs(q.z) == r;
                if (!corner || hash13(p) < 0.4) return 5;
            }
        }
    }
    // a few light posts and flowers on the grass
    if (p.y == h + 1.0) {
        vec2 lc = floor(p.xz / 13.0);
        vec2 lo = lc * 13.0 + floor(vec2(hash12(lc + 1.1), hash12(lc + 3.3)) * 9.0) + 2.0;
        if (p.x == lo.x && p.z == lo.y && hash12(lc + 0.7) < 0.35) return 6;
        if (hash13(p) < 0.03) return 8;
    }
    return 0;
}
vec3 baseColor(int id, vec3 n) {
    if (id == 1) return n.y > 0.5 ? vec3(0.36, 0.6, 0.22) : vec3(0.45, 0.33, 0.22);
    if (id == 2) return vec3(0.45, 0.33, 0.22);
    if (id == 3) return vec3(0.5);
    if (id == 4) return n.y != 0.0 ? vec3(0.6, 0.48, 0.3) : vec3(0.38, 0.29, 0.17);
    if (id == 5) return vec3(0.22, 0.45, 0.14);
    if (id == 6) return vec3(1.0, 0.86, 0.5);
    if (id == 8) return vec3(0.95, 0.85, 0.2);
    return vec3(1.0, 0.0, 1.0);
}
vec3 sunDir() {
    float a = DayTime * 6.2831853;
    return normalize(vec3(sin(a) * 0.9, cos(a), 0.25));
}
float nightF() { return smoothstep(-0.05, -0.25, sunDir().y) ; }

// sky code (copy of the overlay's core/sky.fsh logic, keyed on the view direction)
float fbm3(vec3 p) {
    float s = 0.0, a = 0.5;
    for (int i = 0; i < 4; i++) {
        vec3 i3 = floor(p), f = fract(p);
        f = f * f * (3.0 - 2.0 * f);
        float x = mix(mix(mix(hash13(i3), hash13(i3 + vec3(1, 0, 0)), f.x), mix(hash13(i3 + vec3(0, 1, 0)), hash13(i3 + vec3(1, 1, 0)), f.x), f.y),
                      mix(mix(hash13(i3 + vec3(0, 0, 1)), hash13(i3 + vec3(1, 0, 1)), f.x), mix(hash13(i3 + vec3(0, 1, 1)), hash13(i3 + vec3(1, 1, 1)), f.x), f.y), f.z);
        s += x * a; a *= 0.5; p *= 2.02;
    }
    return s / 0.9375;
}
vec3 skyCode(vec3 dir) {
    float up = smoothstep(-0.02, 0.12, dir.y);
    float band = exp(-pow(dot(dir, normalize(vec3(0.42, 0.30, 0.86))) / 0.38, 2.0));
    float a = clamp((fbm3(dir * 2.6 + vec3(3.1, 0.0, 1.7)) - 0.38) * 2.4, 0.0, 1.0) * (0.3 + 0.7 * band) * up;
    float b = clamp((fbm3(dir * 4.2 + vec3(0.0, 7.7, 2.3)) - 0.46) * 2.8, 0.0, 1.0) * (0.2 + 0.8 * band) * up;
    vec3 g = dir * 260.0;
    vec3 cell = floor(g);
    float star = 0.0;
    if (hash13(cell) < 0.012 + 0.05 * band) {
        vec3 p = cell + 0.5 + (vec3(hash13(cell + 1.7), hash13(cell + 4.3), hash13(cell + 8.9)) - 0.5) * 0.5;
        float lvl = 1.0 + floor(hash13(cell + 12.1) * 2.99);
        star = (length(g - p) < 0.42 ? lvl : 0.0) * up;
    }
    return nonios_sky_code(a, b, star, ivec2(gl_FragCoord.xy));
}
vec3 mark(vec3 c, vec3 code) {
    vec3 q = floor(clamp(c, 0.0, 1.0) * 255.0 + 0.5);
    return (q - mod(q, 4.0) + code) / 255.0;
}

vec3 skyColor(vec3 dir, out vec3 addLater) {
    float nf = nightF();
    vec3 day = mix(vec3(0.62, 0.75, 1.0), vec3(0.47, 0.62, 1.0), clamp(dir.y, 0.0, 1.0));
    vec3 night = vec3(0.0, 0.0, 0.01) + vec3(0.01, 0.015, 0.03) * (1.0 - clamp(dir.y, 0.0, 1.0));
    vec3 c = mix(day, night, nf);
    if (dir.y < -0.03) c *= 0.2;  // dark lower disc
    // celestial bodies are blended on top of the coded sky (like the game: additive, after the sky)
    addLater = vec3(0.0);
    vec3 s = sunDir();
    vec3 m = -s;
    // square sun / moon (tangent-space test)
    vec3 tu = normalize(cross(s, vec3(0, 0, 1)));
    vec3 tv = cross(s, tu);
    float ds = dot(dir, s);
    if (ds > 0.0) {
        vec2 q = vec2(dot(dir, tu), dot(dir, tv)) / ds;
        if (max(abs(q.x), abs(q.y)) < 0.09) addLater += vec3(1.0, 0.95, 0.7) * (1.0 - nf);
    }
    float dm = dot(dir, m);
    if (dm > 0.0) {
        vec2 q = vec2(dot(dir, tu), dot(dir, tv)) / dm;
        if (max(abs(q.x), abs(q.y)) < 0.06) {
            vec2 t = floor((q / 0.12 + 0.5) * 16.0);
            float crater = hash12(t) < 0.25 ? 0.75 : 1.0;
            addLater += vec3(0.85, 0.88, 0.95) * crater * nf;
        }
    }
    // vanilla stars (additive)
    vec3 g = dir * 180.0;
    vec3 cell = floor(g);
    if (hash13(cell + 50.0) < 0.02 && length(fract(g) - 0.5) < 0.25 && dir.y > -0.1) addLater += vec3(0.6) * nf;
    return c;
}

void main() {
    vec2 uv = (gl_FragCoord.xy / Res) * 2.0 - 1.0;
    float aspect = Res.x / Res.y;
    vec3 fw = vec3(sin(CamRot.x) * cos(CamRot.y), sin(CamRot.y), cos(CamRot.x) * cos(CamRot.y));
    vec3 rt = normalize(cross(fw, vec3(0, 1, 0)));
    vec3 up = cross(rt, fw);
    vec3 rd = normalize(fw + (uv.x * aspect * TanHalfFov) * rt + (uv.y * TanHalfFov) * up);

    // DDA
    vec3 ro = CamPos;
    vec3 p = floor(ro);
    vec3 st = sign(rd);
    vec3 tD = abs(1.0 / rd);
    vec3 tM = (st * (p - ro) + st * 0.5 + 0.5) * tD;
    vec3 n = vec3(0.0);
    int id = 0;
    float t = 0.0;
    for (int i = 0; i < 420; i++) {
        id = block(p);
        if (id != 0) break;
        if (tM.x < tM.y && tM.x < tM.z) { t = tM.x; tM.x += tD.x; p.x += st.x; n = vec3(-st.x, 0, 0); }
        else if (tM.y < tM.z) { t = tM.y; tM.y += tD.y; p.y += st.y; n = vec3(0, -st.y, 0); }
        else { t = tM.z; tM.z += tD.z; p.z += st.z; n = vec3(0, 0, -st.z); }
        if (t > RenderDist) { id = 0; break; }
    }
    float nf = nightF();
    if (id == 0) {
        vec3 add;
        vec3 sky = skyColor(rd, add);
        // below the horizon the game shows the uncoded clear colour (arbitrary low bits, here 3,2,3)
        vec3 col = (rd.y < -0.03 ? vec3(7.0, 6.0, 15.0) / 255.0 : mark(sky, skyCode(rd))) + add;
        outColor = vec4(clamp(col, 0.0, 1.0), 1.0);
        outDepth = vec4(0.0);
        return;
    }
    vec3 hit = ro + rd * t;
    // texel noise (16x16 per face)
    vec3 lp = hit - p;
    vec2 fuv = abs(n.x) > 0.5 ? lp.zy : abs(n.y) > 0.5 ? lp.xz : lp.xy;
    vec2 tex = floor(fuv * 16.0);
    float tn = hash13(vec3(tex, dot(p, vec3(1.0, 57.0, 113.0)) * 0.0 + float(id) * 7.0 + (abs(n.y) > 0.5 ? 1.0 : 0.0)));
    vec3 base = baseColor(id, n) * (0.78 + 0.4 * tn);
    if (id == 5 && tn < 0.12) base *= 0.5;
    // lighting: Minecraft face shade + sky light + block light from nearby glowstone
    float shade = n.y > 0.5 ? 1.0 : n.y < -0.5 ? 0.5 : abs(n.x) > 0.5 ? 0.6 : 0.8;
    vec3 skyl = mix(vec3(1.0), vec3(0.11, 0.12, 0.2), nf);
    float bl = 0.0;
    vec2 lc0 = floor(p.xz / 13.0);
    for (int dx = -1; dx <= 1; dx++)
    for (int dz = -1; dz <= 1; dz++) {
        vec2 lc = lc0 + vec2(dx, dz);
        if (hash12(lc + 0.7) >= 0.35) continue;
        vec2 lo = lc * 13.0 + floor(vec2(hash12(lc + 1.1), hash12(lc + 3.3)) * 9.0) + 2.0;
        vec3 lpos = vec3(lo.x + 0.5, height(lo) + 1.5, lo.y + 0.5);
        float d = abs(hit.x - lpos.x) + abs(hit.y - lpos.y) + abs(hit.z - lpos.z);
        bl = max(bl, clamp((15.0 - d) / 15.0, 0.0, 1.0));
    }
    vec3 blockl = vec3(1.0, 0.85, 0.6) * pow(bl, 1.6) * (0.95 + 0.05 * sin(Time * 9.0));
    vec3 light = max(skyl, blockl) * shade;
    float heat = 0.0;
    vec3 col = base * light;
    if (id == 6) { col = base * (0.85 + 0.3 * tn); heat = 1.0; }
    // fog
    vec3 add;
    vec3 fogc = skyColor(normalize(vec3(rd.x, 0.0, rd.z)), add);
    float fog = smoothstep(RenderDist * 0.75, RenderDist, t);
    col = mix(col, fogc, fog);
    float l = floor(heat * 7.0 + 0.5);
    vec3 code = vec3(0, 1, 0) + 2.0 * vec3(mod(l, 2.0), mod(floor(l / 2.0), 2.0), floor(l / 4.0));
    outColor = vec4(mark(col, code), 1.0);
    // reversed Z: view-space depth along the camera axis
    float z = t * dot(rd, fw);
    outDepth = vec4(Near / z, 0.0, 0.0, 1.0);
}
