"""Concept images via Gemini (inspiration for shaders and builds, never shipped).

  python tools/imagegen.py "prompt" [-o out.png] [-n 2] [--model gemini-3-pro-image] [--ref img.png ...]

Key: GEMINI_API_KEY or GOOGLE_API_KEY. Outputs default to .mcdev/imagegen/.
"""
import argparse, os, pathlib, sys, time

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "gemini-3-pro-image"


def generate(prompt, out=None, n=1, model=DEFAULT_MODEL, refs=()):
    from google import genai
    from google.genai import types
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        sys.exit("no GEMINI_API_KEY / GOOGLE_API_KEY")
    client = genai.Client(api_key=key)
    contents = [types.Part.from_bytes(data=pathlib.Path(r).read_bytes(),
                                      mime_type="image/png" if r.lower().endswith(".png") else "image/jpeg")
                for r in refs] + [prompt]
    outdir = ROOT / ".mcdev" / "imagegen"
    outdir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i in range(n):
        r = client.models.generate_content(model=model, contents=contents)
        for p in r.candidates[0].content.parts:
            if p.inline_data:
                path = pathlib.Path(out) if out and n == 1 else outdir / f"{int(time.time())}_{i}.png"
                path.write_bytes(p.inline_data.data)
                paths.append(path)
                print(path)
    if not paths:
        sys.exit("no image returned")
    return paths


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("prompt")
    ap.add_argument("-o", "--out")
    ap.add_argument("-n", type=int, default=1)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--ref", nargs="*", default=[])
    a = ap.parse_args()
    generate(a.prompt, a.out, a.n, a.model, a.ref)
