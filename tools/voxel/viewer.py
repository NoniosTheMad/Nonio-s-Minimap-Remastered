"""Single-file HTML viewer: plain WebGL1 (no libraries), texture atlas PNG, greedy-meshed quads, gzip + base64 payload.

    write_viewer(scene, out_dir / "viewer.html")          python -m tools.voxel view SCENE
    python -m tools.voxel serve [--port 8765]             serves .mcdev/voxel/out/ (every scene's viewer.html)

Why v1 was hard to open: three.js r147 inlined + a WebGL2-only texture array, and every vertex attribute as base64
float/JSON (a castle was 4.7 MB of text that the browser had to atob and loop over before drawing anything; any
failure left a blank page). v2: quantised int16 vertices (16 B each), coplanar faces merged (greedy meshing, AO-aware),
one atlas PNG, the whole payload gzip'd (DecompressionStream), WebGL1 with 16-bit index chunks (works everywhere WebGL
does), and an on-page error message instead of a blank page.

Lighting (face shading x sun x AO x tint) is baked into vertex colours; cutout textures alpha-tested, translucent ones
(glass, water, ice) drawn last with blending. Controls: drag orbit, right/shift-drag pan, wheel/pinch zoom,
1-4 iso corners, T top, F frame, M markers."""
import base64, gzip, io, json
from pathlib import Path

import numpy as np
from PIL import Image

from . import mesh as meshmod
from .render import SUN

ATLAS_COLS = 32


def _shade(m):
    n = m.nrm
    face = np.where(np.abs(n[:, 1]) > 0.5, np.where(n[:, 1] > 0, 1.0, 0.5), np.where(np.abs(n[:, 2]) > 0.5, 0.8, 0.6))
    ndl = np.clip(n @ SUN, 0, None)
    light = face * (0.5 + 0.5 * (0.3 + 0.7 * ndl)) * 1.12
    return np.clip(m.col * light[:, None] * 255, 0, 255).astype(np.uint8)


def greedy(pos, uv, lay, col, tr):
    """Merge coplanar unit faces with the same texture, colour (incl. AO), uv mapping and translucency into rectangles.
    pos (Q,4,3), uv (Q,4,2), lay (Q,), col (Q,4,3) uint8, tr (Q,) bool -> same arrays, fewer quads."""
    Q = len(pos)
    if Q == 0:
        return pos, uv, lay, col, tr
    lo = pos.min(1); hi = pos.max(1); ext = hi - lo
    flat = (ext < 1e-6).sum(1) == 1
    ax = np.argmin(ext, 1)
    unit = flat & np.all(np.isclose(np.sort(ext, 1)[:, 1:], 1.0), 1) & np.isclose(lo[np.arange(Q), ax], np.round(lo[np.arange(Q), ax]))
    unit &= np.all(np.isclose(lo, np.round(lo)), 1)
    unit &= np.all(col == col[:, :1], axis=(1, 2))
    cand = np.nonzero(unit)[0]
    keep = np.ones(Q, bool)
    out_p, out_uv, out_l, out_c, out_t = [], [], [], [], []
    if len(cand):
        a = ax[cand]
        ia = np.where(a == 0, 1, 0); ja = np.where(a == 2, 1, 2)          # in-plane axes (i < j)
        r = np.arange(len(cand))
        P = pos[cand]
        pi = P[r[:, None], np.arange(4)[None], ia[:, None]] - lo[cand, ia][:, None]   # 0/1 corner coords
        pj = P[r[:, None], np.arange(4)[None], ja[:, None]] - lo[cand, ja][:, None]
        pi = np.round(pi).astype(np.int8); pj = np.round(pj).astype(np.int8)
        U = uv[cand]
        # affine uv map per quad: uv = uv0 + du*di + dv*dj  (fit from the corners)
        A = np.stack([pi, pj, np.ones_like(pi)], -1).astype(np.float64)           # (n,4,3)
        coef = np.linalg.pinv(A) @ U                                               # (n,3,2)
        resid = np.abs(A @ coef - U).max((1, 2))
        ok = (resid < 1e-4) & np.all(np.isin(np.round(coef[:, :2], 4), (-1.0, 0.0, 1.0)), (1, 2))
        coef = np.round(coef * 16) / 16
        corner = (pi * 2 + pj).astype(np.int8)                                     # winding signature
        plane = np.round(lo[cand, a]).astype(np.int32)
        ci = np.round(lo[cand, ia]).astype(np.int32); cj = np.round(lo[cand, ja]).astype(np.int32)
        # uv offset relative to the cell: shift-invariant if (uv0 - du*ci - dv*cj) mod 1 equal
        groups = {}
        for k in np.nonzero(ok)[0]:
            du = tuple(coef[k, 0]); dv = tuple(coef[k, 1])
            off = tuple(np.round(((coef[k, 2] - coef[k, 0] * ci[k] - coef[k, 1] * cj[k]) % 1.0) * 16).astype(int) % 16)
            key = (int(a[k]), int(plane[k]), int(lay[cand[k]]), bool(tr[cand[k]]), tuple(col[cand[k], 0]), du, dv, off,
                   tuple(corner[k]))
            groups.setdefault(key, {})[(int(ci[k]), int(cj[k]))] = k
        for key, cells in groups.items():
            if len(cells) < 2:
                continue
            a_, plane_ = key[0], key[1]
            ia_, ja_ = (1, 2) if a_ == 0 else ((0, 2) if a_ == 1 else (0, 1))
            left = set(cells)
            for (i0, j0) in sorted(cells):
                if (i0, j0) not in left:
                    continue
                w = 1
                while (i0 + w, j0) in left:
                    w += 1
                h = 1
                while all((i0 + t, j0 + h) in left for t in range(w)):
                    h += 1
                if w * h == 1:
                    left.discard((i0, j0))
                    continue
                for t in range(w):
                    for s in range(h):
                        left.discard((i0 + t, j0 + s))
                        keep[cand[cells[(i0 + t, j0 + s)]]] = False
                k = cells[(i0, j0)]
                q = cand[k]
                newp = pos[q].copy()
                newuv = uv[q].copy()
                for v in range(4):
                    di, dj = int(pi[k, v]), int(pj[k, v])
                    newp[v, ia_] = i0 + di * w
                    newp[v, ja_] = j0 + dj * h
                    newp[v, a_] = plane_
                    newuv[v] = coef[k, 2] + coef[k, 0] * di * w + coef[k, 1] * dj * h
                out_p.append(newp); out_uv.append(newuv); out_l.append(lay[q]); out_c.append(col[q]); out_t.append(tr[q])
    if out_p:
        pos = np.concatenate([pos[keep], np.stack(out_p)])
        uv = np.concatenate([uv[keep], np.stack(out_uv)])
        lay = np.concatenate([lay[keep], np.array(out_l)])
        col = np.concatenate([col[keep], np.stack(out_c)])
        tr = np.concatenate([tr[keep], np.array(out_t)])
    return pos, uv, lay, col, tr


def atlas_png(layers):
    L = len(layers)
    rows = (L + ATLAS_COLS - 1) // ATLAS_COLS
    H = 1
    while H < rows * 16:
        H *= 2
    img = np.zeros((H, ATLAS_COLS * 16, 4), np.uint8)
    for i, t in enumerate(layers):
        r, c = divmod(i, ATLAS_COLS)
        img[r * 16:(r + 1) * 16, c * 16:(c + 1) * 16] = t
    buf = io.BytesIO()
    Image.fromarray(img).save(buf, "PNG", optimize=True)
    return buf.getvalue(), img.shape[1], img.shape[0]


def payload(scene, vtint=None, merge=True):
    m = meshmod.build(scene, vtint=vtint)
    nq = len(m.pos) // 4
    col = _shade(m).reshape(nq, 4, 3)
    pos = m.pos.reshape(nq, 4, 3)
    uv = m.uvl[:, :2].reshape(nq, 4, 2)
    lay = m.uvl[::4, 2].astype(np.int32)
    tr = np.zeros(nq, bool)
    if len(m.tidx):
        tr[np.unique(m.tidx // 4)] = True
    q0 = nq
    if merge:
        pos, uv, lay, col, tr = greedy(pos, uv, lay, col, tr)
        nq = len(pos)
    # AO diagonal flip (merged quads have uniform colour, so never flip)
    a = col.astype(int).sum(2)
    flip = (a[:, 0] + a[:, 2]) < (a[:, 1] + a[:, 3])
    ext = max(np.abs(pos).max() if nq else 1, 1)
    ps = 16
    while ps < 256 and ext * ps * 2 < 32000:
        ps *= 2
    us = 64
    order = np.concatenate([np.nonzero(~tr)[0], np.nonzero(tr)[0]])
    pos, uv, lay, col, flip = pos[order], uv[order], lay[order], col[order], flip[order]
    V = nq * 4
    rec = np.zeros(V, np.dtype([("p", "<i2", 3), ("uv", "<i2", 2), ("l", "<u2"), ("c", "u1", 4)]))
    rec["p"] = np.round(pos.reshape(-1, 3) * ps).astype(np.int16)
    rec["uv"] = np.round(uv.reshape(-1, 2) * us).astype(np.int16)
    rec["l"] = np.repeat(lay, 4).astype(np.uint16)
    c4 = np.zeros((nq, 4, 4), np.uint8); c4[..., :3] = col; c4[:, 0, 3] = flip.astype(np.uint8) * 255
    rec["c"] = c4.reshape(-1, 4)
    png, aw, ah = atlas_png(m.tex.layers or [np.zeros((16, 16, 4), np.uint8)])
    blob = gzip.compress(rec.tobytes(), 9, mtime=0)
    return {"ps": ps, "us": us, "nq": int(nq), "nopaque": int((~tr).sum()), "quads_raw": int(q0), "atlas": base64.b64encode(png).decode(),
            "aw": aw, "ah": ah, "cols": ATLAS_COLS, "geo": base64.b64encode(blob).decode(), "size": list(scene.shape),
            "markers": {k: {"pos": v["pos"]} for k, v in scene.markers.items()}}


HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>__TITLE__</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--bg:#b9cbe8;--panel:#ffffffd9;--ink:#123}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1d2430;--panel:#000000b3;--ink:#dde6f3}}
:root[data-theme="dark"]{--bg:#1d2430;--panel:#000000b3;--ink:#dde6f3}
html,body{margin:0;height:100%;overflow:hidden;background:var(--bg);font:13px system-ui,sans-serif;color:var(--ink)}
canvas{display:block;width:100vw;height:100vh;touch-action:none}
#hud{position:fixed;left:10px;top:8px;background:var(--panel);padding:6px 9px;border-radius:6px;line-height:1.5;max-width:calc(100vw - 40px)}
#err{position:fixed;inset:0;display:none;align-items:center;justify-content:center;padding:16px;text-align:center}
#err div{background:var(--panel);padding:14px 18px;border-radius:8px;max-width:520px}
</style></head><body><canvas id="c"></canvas>
<div id="hud"><b>__TITLE__</b> &middot; __SIZE__ &middot; <span id="nq">loading&hellip;</span><br>
drag orbit &middot; right/shift-drag pan &middot; wheel/pinch zoom &middot; 1-4 iso &middot; T top &middot; F frame</div>
<div id="err"><div id="errt"></div></div>
<script>
const D = __DATA__;
function fail(msg){ const e=document.getElementById('err'); e.style.display='flex'; document.getElementById('errt').textContent=msg; }
addEventListener('error', ev => fail('Viewer error: ' + ev.message));
addEventListener('unhandledrejection', ev => fail('Viewer error: ' + (ev.reason && ev.reason.message || ev.reason)));
function b64(s){ const b=atob(s), u=new Uint8Array(b.length); for(let i=0;i<b.length;i++) u[i]=b.charCodeAt(i); return u; }
async function gunzip(u){
  if (!('DecompressionStream' in window)) throw new Error('this browser lacks DecompressionStream (needs Chrome 80+, Firefox 113+, Safari 16.4+)');
  const s = new Blob([u]).stream().pipeThrough(new DecompressionStream('gzip'));
  return new Uint8Array(await new Response(s).arrayBuffer());
}
// ---- tiny mat4 (column-major)
function persp(f,a,n,fa){const t=1/Math.tan(f/2);return [t/a,0,0,0, 0,t,0,0, 0,0,(fa+n)/(n-fa),-1, 0,0,2*fa*n/(n-fa),0];}
function lookAt(e,c,u){let z=[e[0]-c[0],e[1]-c[1],e[2]-c[2]];let l=Math.hypot(...z);z=z.map(v=>v/l);
  let x=[u[1]*z[2]-u[2]*z[1],u[2]*z[0]-u[0]*z[2],u[0]*z[1]-u[1]*z[0]];l=Math.hypot(...x)||1;x=x.map(v=>v/l);
  const y=[z[1]*x[2]-z[2]*x[1],z[2]*x[0]-z[0]*x[2],z[0]*x[1]-z[1]*x[0]];
  return [x[0],y[0],z[0],0, x[1],y[1],z[1],0, x[2],y[2],z[2],0, -(x[0]*e[0]+x[1]*e[1]+x[2]*e[2]),-(y[0]*e[0]+y[1]*e[1]+y[2]*e[2]),-(z[0]*e[0]+z[1]*e[1]+z[2]*e[2]),1];}
function mul(a,b){const o=new Array(16);for(let i=0;i<4;i++)for(let j=0;j<4;j++){let s=0;for(let k=0;k<4;k++)s+=a[k*4+j]*b[i*4+k];o[i*4+j]=s;}return o;}
(async function main(){
  const cv=document.getElementById('c');
  const gl=cv.getContext('webgl',{antialias:true,alpha:false}) || cv.getContext('experimental-webgl');
  if(!gl){ fail('WebGL is not available in this browser.'); return; }
  const raw = await gunzip(b64(D.geo));
  const img = new Image(); img.src = 'data:image/png;base64,' + D.atlas; await img.decode();
  const vs=`attribute vec3 p; attribute vec2 uv; attribute float l; attribute vec4 c; uniform mat4 M; uniform float cols; uniform float ps; uniform float us;
    varying vec2 vuv; varying vec2 vt; varying vec3 vc; varying float vd;
    void main(){ vuv=uv/us; float r=floor((l+0.5)/cols); vt=vec2(l-r*cols, r); vc=c.rgb; vec4 q=M*vec4(p/ps,1.0); vd=q.w; gl_Position=q; }`;
  const fs=`precision mediump float; uniform sampler2D T; uniform vec2 A; uniform float tr; uniform float fog; uniform vec3 bg;
    varying vec2 vuv; varying vec2 vt; varying vec3 vc; varying float vd;
    void main(){ vec2 f=clamp(fract(vuv), 0.5/16.0, 15.5/16.0); vec4 t=texture2D(T, (vt*16.0+f*16.0)/A);
      if(tr<0.5 && t.a<0.5) discard;
      vec3 col=t.rgb*vc; col=mix(col, bg, clamp((vd-fog*0.6)/(fog*0.4),0.0,1.0)*0.6);
      gl_FragColor=vec4(col, tr<0.5?1.0:max(t.a,0.55)); }`;
  function sh(t,s){const o=gl.createShader(t);gl.shaderSource(o,s);gl.compileShader(o);if(!gl.getShaderParameter(o,gl.COMPILE_STATUS))throw new Error(gl.getShaderInfoLog(o));return o;}
  const pr=gl.createProgram(); gl.attachShader(pr,sh(gl.VERTEX_SHADER,vs)); gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,fs)); gl.linkProgram(pr);
  if(!gl.getProgramParameter(pr,gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(pr));
  gl.useProgram(pr);
  const tex=gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D,tex);
  gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,img);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.NEAREST); gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.NEAREST);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
  const vb=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,vb); gl.bufferData(gl.ARRAY_BUFFER,raw,gl.STATIC_DRAW);
  const loc={p:gl.getAttribLocation(pr,'p'),uv:gl.getAttribLocation(pr,'uv'),l:gl.getAttribLocation(pr,'l'),c:gl.getAttribLocation(pr,'c')};
  for(const k in loc) gl.enableVertexAttribArray(loc[k]);
  // index chunks of <= 16384 quads (16-bit indices); the flip flag (AO diagonal) rides in the first vertex's alpha
  const CH=16384, chunks=[];
  for(let q0=0;q0<D.nq;q0+=CH){ const n=Math.min(CH,D.nq-q0), ix=new Uint16Array(n*6);
    for(let q=0;q<n;q++){ const b=q*4, o=q*6, f=raw[((q0+q)*4)*16+15]>127;
      if(f){ix[o]=b+1;ix[o+1]=b+2;ix[o+2]=b+3;ix[o+3]=b+1;ix[o+4]=b+3;ix[o+5]=b;} else {ix[o]=b;ix[o+1]=b+1;ix[o+2]=b+2;ix[o+3]=b;ix[o+4]=b+2;ix[o+5]=b+3;} }
    const ib=gl.createBuffer(); gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,ib); gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,ix,gl.STATIC_DRAW);
    chunks.push({q0,n,ib}); }
  document.getElementById('nq').textContent = D.nq.toLocaleString()+' quads (from '+D.quads_raw.toLocaleString()+')';
  const U=n=>gl.getUniformLocation(pr,n);
  gl.uniform1i(U('T'),0); gl.uniform2f(U('A'),D.aw,D.ah); gl.uniform1f(U('cols'),D.cols); gl.uniform1f(U('ps'),D.ps); gl.uniform1f(U('us'),D.us);
  const bgc=getComputedStyle(document.body).backgroundColor.match(/\d+/g).map(v=>v/255); gl.uniform3f(U('bg'),bgc[0],bgc[1],bgc[2]);
  const S=D.size, C=[S[0]/2,S[1]/3,S[2]/2], R=Math.hypot(...S)/2+1; gl.uniform1f(U('fog'),R*6);
  const cam={yaw:0.785,pitch:0.6,dist:R*1.5,t:C.slice()};
  function view(y,p){cam.yaw=y;cam.pitch=p;cam.dist=R*1.5;cam.t=C.slice();draw();}
  function draw(){
    const w=cv.clientWidth*devicePixelRatio|0,h=cv.clientHeight*devicePixelRatio|0; if(cv.width!==w||cv.height!==h){cv.width=w;cv.height=h;}
    gl.viewport(0,0,w,h); gl.clearColor(bgc[0],bgc[1],bgc[2],1); gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
    const cp=Math.cos(cam.pitch), e=[cam.t[0]+Math.sin(cam.yaw)*cp*cam.dist, cam.t[1]+Math.sin(cam.pitch)*cam.dist, cam.t[2]+Math.cos(cam.yaw)*cp*cam.dist];
    const M=mul(persp(0.87,w/h,Math.max(0.05,cam.dist/500),cam.dist+R*8), lookAt(e,cam.t,[0,1,0]));
    gl.uniformMatrix4fv(U('M'),false,new Float32Array(M));
    gl.enable(gl.DEPTH_TEST);
    for(const pass of [0,1]){
      gl.uniform1f(U('tr'),pass); if(pass){gl.enable(gl.BLEND);gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);gl.depthMask(false);} else {gl.disable(gl.BLEND);gl.depthMask(true);}
      for(const ch of chunks){
        const a=Math.max(ch.q0, pass?D.nopaque:0), b=Math.min(ch.q0+ch.n, pass?D.nq:D.nopaque); if(b<=a) continue;
        const off=ch.q0*64;
        gl.bindBuffer(gl.ARRAY_BUFFER,vb);
        gl.vertexAttribPointer(loc.p,3,gl.SHORT,false,16,off); gl.vertexAttribPointer(loc.uv,2,gl.SHORT,false,16,off+6);
        gl.vertexAttribPointer(loc.l,1,gl.UNSIGNED_SHORT,false,16,off+10); gl.vertexAttribPointer(loc.c,4,gl.UNSIGNED_BYTE,true,16,off+12);
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER,ch.ib);
        gl.drawElements(gl.TRIANGLES,(b-a)*6,gl.UNSIGNED_SHORT,(a-ch.q0)*12);
      }
    }
    gl.depthMask(true);
  }
  let drag=null, pts=new Map();
  cv.addEventListener('contextmenu',e=>e.preventDefault());
  cv.addEventListener('pointerdown',e=>{cv.setPointerCapture(e.pointerId);pts.set(e.pointerId,[e.clientX,e.clientY]);drag={b:e.button,s:e.shiftKey};});
  cv.addEventListener('pointerup',e=>{pts.delete(e.pointerId);drag=null;});
  cv.addEventListener('pointermove',e=>{ if(!pts.has(e.pointerId)) return; const [x0,y0]=pts.get(e.pointerId), dx=e.clientX-x0, dy=e.clientY-y0;
    if(pts.size===2){ const o=[...pts.entries()].find(([k])=>k!==e.pointerId)[1]; const d0=Math.hypot(x0-o[0],y0-o[1]), d1=Math.hypot(e.clientX-o[0],e.clientY-o[1]);
      if(d0>0) cam.dist*=d0/d1; }
    else if(drag && (drag.b===2||drag.s)){ const k=cam.dist/cv.clientHeight; const cy=Math.cos(cam.yaw), sy=Math.sin(cam.yaw);
      cam.t[0]-= (cy*dx)*k; cam.t[2]-= (-sy*dx)*k; cam.t[1]+= dy*k; }
    else { cam.yaw-=dx*0.008; cam.pitch=Math.max(-1.5,Math.min(1.55,cam.pitch+dy*0.008)); }
    pts.set(e.pointerId,[e.clientX,e.clientY]); draw(); });
  cv.addEventListener('wheel',e=>{e.preventDefault(); cam.dist*=Math.exp(e.deltaY*0.001); draw();},{passive:false});
  addEventListener('keydown',e=>{const k=e.key.toLowerCase();
    if(k==='1')view(0.785,0.6); if(k==='2')view(-0.785,0.6); if(k==='3')view(-2.356,0.6); if(k==='4')view(2.356,0.6);
    if(k==='t')view(0,1.55); if(k==='f')view(cam.yaw,cam.pitch);});
  addEventListener('resize',draw);
  draw(); window.__voxelReady = true;
})().catch(e=>fail('Viewer error: '+e.message));
</script></body></html>"""


def write_viewer(scene, path, vtint=None, merge=True):
    d = payload(scene, vtint, merge)
    html = (HTML.replace("__TITLE__", scene.name).replace("__SIZE__", "x".join(map(str, scene.shape)))
            .replace("__DATA__", json.dumps(d, separators=(",", ":"))))
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    mb = path.stat().st_size / 1e6
    print(f"[voxel] viewer {path} ({mb:.2f} MB, {d['nq']} quads from {d['quads_raw']})"
          + ("   WARNING: over 16 MB, too big to publish as one artifact" if mb > 16 else ""))
    return path
