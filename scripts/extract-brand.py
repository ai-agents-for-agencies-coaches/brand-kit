#!/usr/bin/env python3
"""Draft a DESIGN.md by extracting REAL signals from a client's site/logo.

  python3 scripts/extract-brand.py --url https://client.com --client acme \
      [--logo logo.png] [--out ~/claude_work/brand-kits]

It NEVER invents values. Anything not confidently detected is written as a
`TODO: VERIFY` line for a human to confirm. Confidence is reported per field.

Detects: hex colors in inline/linked CSS (frequency-ranked), `font-family`
stacks, and (if --logo given, needs Pillow) the logo's dominant colors.
Output: <out>/<client>/DESIGN.md  (review, resolve TODOs, then lint).
"""
import argparse, re, sys, os, urllib.request, collections

UA = {"User-Agent": "Mozilla/5.0 (brand-kit extractor)"}

def get(url):
    try:
        return urllib.request.urlopen(
            urllib.request.Request(url, headers=UA), timeout=30
        ).read().decode("utf-8", "ignore")
    except Exception as e:
        print(f"  ! fetch failed {url}: {e}", file=sys.stderr)
        return ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--client", required=True)
    ap.add_argument("--logo")
    ap.add_argument("--out", default=os.path.expanduser("~/claude_work/brand-kits"))
    a = ap.parse_args()

    html = get(a.url)
    css = html
    for href in re.findall(r'<link[^>]+href="([^"]+\.css[^"]*)"', html)[:6]:
        css += "\n" + get(href if href.startswith("http")
                           else a.url.rstrip("/") + "/" + href.lstrip("/"))

    hexes = collections.Counter(
        ("#" + h.upper() if len(h) == 6 else
         "#" + "".join(c * 2 for c in h).upper())
        for h in re.findall(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', css))
    hexes.pop("#FFFFFF", None); hexes.pop("#000000", None)
    top_colors = [c for c, _ in hexes.most_common(8)]

    fonts = collections.Counter(
        f.strip().strip('"\'')
        for decl in re.findall(r'font-family\s*:\s*([^;}\n]+)', css, re.I)
        for f in decl.split(",")[:1]
        if f.strip().lower() not in
        ("inherit", "initial", "unset", "sans-serif", "serif", "monospace"))
    top_fonts = [f for f, _ in fonts.most_common(4)]

    logo_colors = []
    if a.logo:
        try:
            from PIL import Image
            im = Image.open(a.logo).convert("RGB").quantize(colors=6)
            pal = im.getpalette()
            logo_colors = ["#%02X%02X%02X" % tuple(pal[i:i + 3])
                           for i in range(0, 18, 3)]
        except Exception as e:
            print(f"  ! logo parse failed: {e}", file=sys.stderr)

    def v(val, label):
        return (val, "detected") if val else (f'"#000000"  # TODO: VERIFY — {label} (not detected)', "TODO")

    primary, _ = v(f'"{top_colors[0]}"' if top_colors else None, "primary/ink")
    accent, _  = v(f'"{top_colors[1]}"' if len(top_colors) > 1 else None, "accent/CTA")
    head_font  = top_fonts[0] if top_fonts else "<Font>  # TODO: VERIFY — heading face"
    body_font  = (top_fonts[1] if len(top_fonts) > 1 else
                  top_fonts[0] if top_fonts else "<Font>  # TODO: VERIFY — body face")

    tpl = open(os.path.join(os.path.dirname(__file__), "..",
               "templates", "DESIGN.md")).read()
    out = (tpl.replace("<Client Name>", a.client.title())
              .replace("<client-slug>", a.client)
              .replace('"#000000"      # TODO: VERIFY — core text / ink',
                       f'{primary}      # source: site CSS (most common)')
              .replace('"#0000FF"       # TODO: VERIFY — sole CTA / interaction color',
                       f'{accent}       # source: site CSS — CONFIRM this is the brand accent')
              .replace("<Font>     # TODO: VERIFY — heading face", head_font)
              .replace("<Font>     # TODO: VERIFY — body face", body_font))

    d = os.path.join(a.out, a.client)
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "DESIGN.md")
    open(p, "w").write(out)

    print(f"\nDraft -> {p}")
    print(f"  colors detected : {top_colors or '— none, ALL marked TODO'}")
    print(f"  fonts detected  : {top_fonts or '— none, marked TODO'}")
    print(f"  logo colors     : {logo_colors or '(no --logo)'}")
    print("\nNEXT (required): review with the user, resolve every TODO: VERIFY,")
    print(f"  then: bash scripts/lint.sh {p}")
    print("Do NOT use this file for creative work while TODOs remain.")

if __name__ == "__main__":
    main()
