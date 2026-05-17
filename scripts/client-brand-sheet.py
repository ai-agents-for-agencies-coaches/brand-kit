#!/usr/bin/env python3
"""Generate a CLIENT-FACING 'Brand Foundations' one-pager from a verified
DESIGN.md. Strips ALL internal language (provenance, corrections, lint,
agency notes) — only what's appropriate to present to the client.

  python3 scripts/client-brand-sheet.py <DESIGN.md> --client "Terzo Roofing" \
      --out <dir> [--ads-dir <dir-of-pngs>] [--agency "Volume Up Agency"]

Writes <out>/brand-foundations.html  (render to PNG/PDF with render-sheet.js).
Refuses if the DESIGN.md still has TODO: VERIFY (not client-ready).
"""
import argparse, os, re, html, glob, datetime, base64

ROLE = {  # internal token name -> client-facing label
  "accent": "Brand Gold", "accent-deep": "Gold · Deep",
  "accent-light": "Gold · Light", "primary": "Primary · Ink",
  "neutral": "Neutral · Surface", "secondary": "Supporting",
  "tertiary": "Accent",
}

def b64(path, max_w=900):
    """Downscale to a web-appropriate width before embedding (keeps the
    shareable PDF/HTML small — full-res ad PNGs are ~4MB each otherwise)."""
    try:
        import io
        from PIL import Image
        im = Image.open(path).convert("RGB")
        if im.width > max_w:
            im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=82, optimize=True)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        ext = os.path.splitext(path)[1].lstrip(".").replace("jpg", "jpeg")
        return f"data:image/{ext};base64," + base64.b64encode(open(path, "rb").read()).decode()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("design"); ap.add_argument("--client", required=True)
    ap.add_argument("--out", required=True); ap.add_argument("--ads-dir")
    ap.add_argument("--agency", default="Volume Up Agency")
    a = ap.parse_args()
    raw = open(a.design).read().replace("\r\n", "\n")
    if "TODO: VERIFY" in raw:
        raise SystemExit("✗ DESIGN.md has TODO: VERIFY — not client-ready. Verify first.")
    lines = raw.split("\n")
    fences = [i for i, l in enumerate(lines) if l.strip() == "---"]
    if len(fences) < 2:
        raise SystemExit("✗ No YAML front-matter fences (--- … ---) found in " + a.design)
    fm = "\n".join(lines[fences[0] + 1:fences[1]])
    body = "\n".join(lines[fences[1] + 1:])
    esc = html.escape

    colors = [(n, h) for n, h in
              re.findall(r'^\s{2}([a-z][\w-]*):\s*"(#[0-9A-Fa-f]{3,6})"', fm, re.M)]
    typ = []
    for blk in re.finditer(r'^\s{2}([\w-]+):\n((?:\s{4}\w+:.*\n?)+)', fm, re.M):
        if blk.group(1) in ("colors", "rounded", "spacing", "components"): continue
        p = dict(re.findall(r'(\w+):\s*(.+)', blk.group(2)))
        if "fontFamily" in p: typ.append((blk.group(1), p))
    # client-safe one-liner: Overview prose up to the first source parenthetical
    ov = re.search(r'##\s*Overview\s*\n+(.+?)(?:\n\s*\n|\(Source)', body, re.S)
    intro = re.sub(r'\s+', ' ', ov.group(1)).strip() if ov else ""
    intro = re.sub(r'\s*\([^)]*\)\s*$', '', intro)

    sw = []
    for nm, hx in colors:
        r, g, b = [int(hx[i:i+2], 16) for i in (1, 3, 5)]
        txt = "#fff" if (r*299+g*587+b*114)/1000 < 140 else "#111"
        sw.append(f'<div class="sw"><div class="chip" style="background:{hx};color:{txt}">{hx}</div>'
                  f'<div class="rl">{esc(ROLE.get(nm, nm.title()))}</div></div>')
    tw = []
    for nm, p in typ:
        fam = p.get("fontFamily", "")
        tw.append(f'<div class="ts"><div class="tl">{esc(fam)} · {esc(p.get("fontWeight","400"))}</div>'
                  f'<div style="font-family:\'{esc(fam)}\',sans-serif;font-size:34px;'
                  f'font-weight:{esc(p.get("fontWeight","700"))};letter-spacing:{esc(p.get("letterSpacing","normal"))}">'
                  f'Built to last. Built on trust.</div></div>')
    ads = ""
    if a.ads_dir and os.path.isdir(a.ads_dir):
        imgs = sorted(glob.glob(os.path.join(a.ads_dir, "*.png")))[:4]
        if imgs:
            cells = "".join(f'<img class="adc" src="{b64(p)}">' for p in imgs)
            ads = (f'<div class="sec"><div class="h2">Your brand, in action</div>'
                   f'<div class="ads">{cells}</div>'
                   f'<div class="cap">First campaign concepts — every creative is built on the palette and type above.</div></div>')

    # palette accents for the sheet's own styling = the client's brand
    cmap = dict(colors)
    GOLD = cmap.get("accent", "#111111")
    INK = cmap.get("primary", "#111111")
    today = datetime.date.today().strftime("%B %Y")
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1240px;background:#fff;color:{INK};font-family:Inter,sans-serif}}
.page{{width:1240px;min-height:1754px;padding:0 0 70px}}
.hero{{background:{GOLD};color:{INK};padding:64px 80px 56px}}
.kick{{font:800 18px Montserrat;letter-spacing:.22em;text-transform:uppercase;opacity:.7}}
.cn{{font:900 64px/1.02 Montserrat;letter-spacing:-.02em;margin:14px 0 0}}
.bf{{font:800 26px Montserrat;margin-top:6px}}
.intro{{font-size:21px;line-height:1.5;margin-top:22px;max-width:880px;font-weight:500}}
.meta{{margin-top:26px;font:700 15px Montserrat;letter-spacing:.06em;text-transform:uppercase;opacity:.8}}
.sec{{padding:52px 80px 0}}
.h2{{font:800 15px Montserrat;letter-spacing:.18em;text-transform:uppercase;color:#888;
  border-bottom:2px solid #ededed;padding-bottom:12px;margin-bottom:26px}}
.sws{{display:flex;flex-wrap:wrap;gap:22px}}
.sw{{width:172px}}
.chip{{height:108px;border-radius:12px;display:flex;align-items:flex-end;justify-content:center;
  padding-bottom:12px;font:600 15px Inter;border:1px solid rgba(0,0,0,.08)}}
.rl{{margin-top:10px;font:700 15px Montserrat;color:{INK}}}
.ts{{padding:16px 0;border-bottom:1px solid #eee}}
.tl{{font:600 12px Inter;color:#999;text-transform:uppercase;letter-spacing:.1em;margin-bottom:8px}}
.cmp{{display:flex;gap:18px;align-items:center;flex-wrap:wrap}}
.bp{{background:{INK};color:#fff;font:800 19px Montserrat;padding:18px 38px;border-radius:8px}}
.ba{{background:{GOLD};color:{INK};font:800 19px Montserrat;padding:18px 38px;border-radius:8px}}
.bs{{background:transparent;color:{INK};border:2px solid {INK};font:800 19px Montserrat;padding:16px 34px;border-radius:8px}}
.band{{background:{GOLD};color:{INK};font:800 26px Montserrat;padding:22px 30px;border-radius:10px;margin-top:18px}}
.ads{{display:grid;grid-template-columns:1fr 1fr;gap:18px}}
.adc{{width:100%;border-radius:12px;border:1px solid #eee}}
.cap{{margin-top:16px;color:#888;font-size:15px}}
.foot{{margin:56px 80px 0;padding-top:26px;border-top:2px solid #ededed;
  display:flex;justify-content:space-between;align-items:center;color:#777;font-size:15px}}
.foot b{{color:{INK};font-family:Montserrat;font-weight:800}}
</style></head><body><div class="page">
<div class="hero">
  <div class="kick">Brand Foundations</div>
  <div class="cn">{esc(a.client)}</div>
  <div class="bf">Your visual identity, locked in.</div>
  <div class="intro">{esc(intro)}</div>
  <div class="meta">Prepared by {esc(a.agency)} · {today}</div>
</div>
<div class="sec"><div class="h2">Color palette</div><div class="sws">{''.join(sw)}</div></div>
<div class="sec"><div class="h2">Typography</div>{''.join(tw)}</div>
<div class="sec"><div class="h2">Components</div>
  <div class="cmp"><span class="ba">Get a Free Inspection</span><span class="bp">Get a Free Inspection</span><span class="bs">Learn More</span></div>
  <div class="band">Signature gold band — used for key messages &amp; calls to action</div>
</div>
{ads}
<div class="foot"><span>Every creative we produce for you is held to this standard.</span><span><b>{esc(a.agency)}</b></span></div>
</div></body></html>'''
    os.makedirs(a.out, exist_ok=True)
    p = os.path.join(a.out, "brand-foundations.html")
    open(p, "w").write(doc)
    print(f"✓ {p}")
    print(f"  colors:{len(colors)} type:{len(typ)} ads:{'yes' if ads else 'no'}")
    print(f"  next: node scripts/render-sheet.js {p}  # -> PNG + PDF")

if __name__ == "__main__":
    main()
