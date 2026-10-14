"""Self-contained HTML viewer (three.js r147 inlined, orbit camera, real textures, no network needed).

    write_viewer(scene, out_dir / "viewer.html")

Lighting (face shading x sun x AO x biome tint) is baked into vertex colours; cutout textures alpha-tested,
translucent ones (glass, water, ice) drawn last. Markers (spawns, cameras) show as coloured pins.
Controls: drag = orbit, right-drag = pan, wheel = zoom, F = frame all, 1-4 = iso corners, T = top."""
import base64, json, urllib.request
from pathlib import Path

import numpy as np

from . import mesh as meshmod
from .paths import voxel_dir
from .render import SUN

THREE_VER = "0.147.0"
URLS = {
    f"three-{THREE_VER}.min.js": f"https://cdn.jsdelivr.net/npm/three@{THREE_VER}/build/three.min.js",
    f"OrbitControls-{THREE_VER}.js": f"https://cdn.jsdelivr.net/npm/three@{THREE_VER}/examples/js/controls/OrbitControls.js",
}


def _lib(name):
    f = voxel_dir() / "cache" / name
    if not f.exists():
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(urllib.request.urlopen(URLS[name], timeout=30).read())
    return f.read_text(encoding="utf-8")


def _b64(a):
    return base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()


def mesh_payload(scene, vtint=None):
    m = meshmod.build(scene, vtint=vtint)
    n = m.nrm
    face = np.where(np.abs(n[:, 1]) > 0.5, np.where(n[:, 1] > 0, 1.0, 0.5), np.where(np.abs(n[:, 2]) > 0.5, 0.8, 0.6))
    ndl = np.clip(n @ SUN, 0, None)
    light = face * (0.5 + 0.5 * (0.3 + 0.7 * ndl)) * 1.12
    col = np.clip(m.col * light[:, None] * 255, 0, 255).astype(np.uint8)
    # quads: 4 vertices each; reorder so the translucent quads come last (one draw call per pass)
    nq = len(m.pos) // 4
    trq = np.zeros(nq, bool)
    if len(m.tidx):
        trq[np.unique(m.tidx // 4)] = True
    order = np.concatenate([np.nonzero(~trq)[0], np.nonzero(trq)[0]])
    vsel = (order[:, None] * 4 + np.arange(4)).ravel()
    # keep the AO diagonal flip: quad k's first index tells which diagonal it uses
    flip = np.zeros(nq, np.uint8)
    tri = np.concatenate([m.idx, m.tidx]).reshape(-1, 6)
    flip[tri[:, 0] // 4] = (tri[:, 0] % 4 == 1)
    tex = m.tex.array()  # (L,16,16,4)
    return dict(
        nq=int(nq), nopaque=int((~trq).sum()),
        pos=_b64(m.pos[vsel].astype(np.float32)),
        uv=_b64(np.clip(np.round(m.uvl[vsel, :2] * 2048), -32768, 32767).astype(np.int16)),
        layer=_b64(m.uvl[vsel, 2].astype(np.uint16)),
        col=_b64(col[vsel]),
        flip=_b64(flip[order]),
        tex=_b64(tex), nlayers=int(len(tex)),
        size=list(scene.shape),
        markers={k: v for k, v in scene.markers.items()},
    )


HTML = r"""<!doctype html><html><head><meta charset="utf-8"><title>__TITLE__</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>html,body{margin:0;height:100%;overflow:hidden;background:#b9cbe8;font:13px system-ui,sans-serif}
#hud{position:fixed;left:10px;top:8px;color:#123;background:#fffc;padding:6px 9px;border-radius:6px;line-height:1.5}
#hud b{font-weight:600}</style></head><body><div id="hud"><b>__TITLE__</b> &middot; __SIZE__ &middot; __QUADS__ quads<br>
drag orbit &middot; right-drag pan &middot; wheel zoom &middot; 1-4 iso &middot; T top &middot; F frame</div>
<script>__THREE__</script><script>__ORBIT__</script>
<script>
const D = __DATA__;
function dec(b64, T){ const s = atob(b64), u = new Uint8Array(s.length); for (let i=0;i<s.length;i++) u[i]=s.charCodeAt(i); return new T(u.buffer); }
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(window.devicePixelRatio); renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);
const scene = new THREE.Scene(); scene.background = new THREE.Color(0xb9cbe8);
const cam = new THREE.PerspectiveCamera(50, innerWidth/innerHeight, 0.1, 5000);
const pos = dec(D.pos, Float32Array), uv16 = dec(D.uv, Int16Array), lay = dec(D.layer, Uint16Array), col = dec(D.col, Uint8Array), flip = dec(D.flip, Uint8Array);
const nv = pos.length/3, uvl = new Float32Array(nv*3);
for (let i=0;i<nv;i++){ uvl[i*3]=uv16[i*2]/2048; uvl[i*3+1]=uv16[i*2+1]/2048; uvl[i*3+2]=lay[i]; }
const idx = new Uint32Array(D.nq*6);
for (let q=0;q<D.nq;q++){ const b=q*4, o=q*6;
  if (flip[q]) { idx.set([b+1,b+2,b+3,b+1,b+3,b], o); } else { idx.set([b,b+1,b+2,b,b+2,b+3], o); } }
const g = new THREE.BufferGeometry();
g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
g.setAttribute('uvl', new THREE.BufferAttribute(uvl, 3));
g.setAttribute('col', new THREE.BufferAttribute(col, 3, true));
g.setIndex(new THREE.BufferAttribute(idx, 1));
const texdata = dec(D.tex, Uint8Array);
const tex = new THREE.DataArrayTexture(texdata, 16, 16, D.nlayers);
tex.format = THREE.RGBAFormat; tex.magFilter = THREE.NearestFilter; tex.minFilter = THREE.NearestFilter; tex.needsUpdate = true;
const vs = `in vec3 uvl; in vec3 col; out vec3 vuvl; out vec3 vcol; out float vd;
void main(){ vuvl=uvl; vcol=col; vec4 mv = modelViewMatrix*vec4(position,1.0); vd=-mv.z; gl_Position = projectionMatrix*mv; }`;
const fs = (tr) => `precision highp sampler2DArray; uniform sampler2DArray tex; uniform float fogfar; in vec3 vuvl; in vec3 vcol; in float vd;
void main(){ vec4 t = texture(tex, vuvl); ${tr ? '' : 'if (t.a < 0.5) discard;'}
  vec3 c = t.rgb*vcol; c = mix(c, vec3(0.725,0.796,0.91), clamp((vd-fogfar*0.6)/(fogfar*0.4),0.0,1.0)*0.6);
  gl_FragColor = vec4(c, ${tr ? 'max(t.a,0.55)' : '1.0'}); }`;
const uni = {tex:{value:tex}, fogfar:{value:1000}};
const mOpaque = new THREE.ShaderMaterial({glslVersion:THREE.GLSL3, vertexShader:vs, fragmentShader:fs(false), uniforms:uni, side:THREE.DoubleSide});
const mTrans = new THREE.ShaderMaterial({glslVersion:THREE.GLSL3, vertexShader:vs, fragmentShader:fs(true), uniforms:uni, side:THREE.DoubleSide, transparent:true, depthWrite:false});
g.addGroup(0, D.nopaque*6, 0); g.addGroup(D.nopaque*6, (D.nq-D.nopaque)*6, 1);
scene.add(new THREE.Mesh(g, [mOpaque, mTrans]));
g.computeBoundingBox(); const bb = g.boundingBox, c = bb.getCenter(new THREE.Vector3()), r = bb.getSize(new THREE.Vector3()).length()/2+1;
uni.fogfar.value = r*6;
const pinCol = n => n.startsWith('spawn') ? (n.includes('black') ? 0x222222 : n.includes('white') ? 0xffffff : 0x33aaff) : 0xffaa22;
for (const [n, m] of Object.entries(D.markers)) {
  const p = new THREE.Mesh(new THREE.ConeGeometry(0.45, 1.6, 10), new THREE.MeshBasicMaterial({color:pinCol(n)}));
  p.rotation.x = Math.PI; p.position.set(m.pos[0]+0.5, m.pos[1]+0.8, m.pos[2]+0.5); scene.add(p);
}
const ctl = new THREE.OrbitControls(cam, renderer.domElement);
function view(dx, dy, dz){ cam.position.set(c.x+dx*r*1.6, c.y+dy*r*1.6, c.z+dz*r*1.6); ctl.target.copy(c); ctl.update(); }
view(0.6, 0.55, 0.6);
addEventListener('keydown', e => { const k = e.key.toLowerCase();
  if (k==='1') view(0.6,0.55,0.6); if (k==='2') view(-0.6,0.55,0.6); if (k==='3') view(-0.6,0.55,-0.6); if (k==='4') view(0.6,0.55,-0.6);
  if (k==='t') view(0,1,0.001); if (k==='f') view(0.6,0.55,0.6); });
addEventListener('resize', () => { cam.aspect = innerWidth/innerHeight; cam.updateProjectionMatrix(); renderer.setSize(innerWidth, innerHeight); });
(function loop(){ requestAnimationFrame(loop); renderer.render(scene, cam); })();
</script></body></html>"""


def write_viewer(scene, path, vtint=None):
    d = mesh_payload(scene, vtint)
    html = (HTML.replace("__THREE__", _lib(f"three-{THREE_VER}.min.js"))
            .replace("__ORBIT__", _lib(f"OrbitControls-{THREE_VER}.js"))
            .replace("__TITLE__", scene.name).replace("__SIZE__", "x".join(map(str, scene.shape)))
            .replace("__QUADS__", str(d["nq"])).replace("__DATA__", json.dumps(d)))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print(f"[voxel] viewer {path} ({path.stat().st_size / 1e6:.1f} MB)")
    return path
