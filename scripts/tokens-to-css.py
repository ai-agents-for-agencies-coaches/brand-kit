#!/usr/bin/env python3
"""DESIGN.md tokens -> CSS custom properties + a Tailwind theme snippet.

  python3 scripts/tokens-to-css.py path/to/DESIGN.md [--out-dir DIR]

Writes:
  design-tokens.css      :root{} with --color-* --font-* --radius-* --space-*
                         plus aliases the studio templates expect
                         (--accent --ink --bg --mute) so they're on-brand.
  tailwind.tokens.js     theme.extend snippet for landing pages.

Refuses to run if the file still contains TODO: VERIFY.
"""
import sys, os, re, argparse, json

def parse_front_matter(text):
    m = re.search(r'^---\s*\n(.*?)\n---\s*\n', text, re.S | re.M)
    if not m:
        sys.exit("No YAML front matter found.")
    body = m.group(1)
    try:
        import yaml
        return yaml.safe_load(re.sub(r'^\s*#.*$', '', body, flags=re.M))
    except ImportError:
        # minimal nested parser for the DESIGN.md token subset
        root, stack = {}, [(-1, {})]
        tree = stack[0][1]
        for ln in body.splitlines():
            if not ln.strip() or ln.lstrip().startswith("#"):
                continue
            ind = len(ln) - len(ln.lstrip())
            key, _, val = ln.strip().partition(":")
            val = val.strip().strip('"\'')
            while stack and stack[-1][0] >= ind:
                stack.pop()
            parent = stack[-1][1]
            if val == "":
                parent[key] = {}
                stack.append((ind, parent[key]))
            else:
                parent[key] = val
        return tree

ALIASES = {  # studio template vars <- design.md color tokens
    "--accent": ("accent", "tertiary", "primary"),
    "--ink":    ("primary", "ink"),
    "--bg":     ("neutral", "background", "surface"),
    "--mute":   ("secondary",),
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--out-dir", default=".")
    a = ap.parse_args()
    text = open(a.file).read()
    if "TODO: VERIFY" in text:
        sys.exit("✗ DESIGN.md has unresolved TODO: VERIFY — verify before generating tokens.")
    d = parse_front_matter(text) or {}
    colors = d.get("colors", {}) or {}
    typ = d.get("typography", {}) or {}
    rnd = d.get("rounded", {}) or {}
    sp = d.get("spacing", {}) or {}

    css = [":root {", "  /* generated from DESIGN.md — do not edit; regenerate */"]
    for k, val in colors.items():
        css.append(f"  --color-{k}: {val};")
    for var, names in ALIASES.items():
        for n in names:
            if n in colors:
                css.append(f"  {var}: {colors[n]};")
                break
    for k, t in typ.items():
        if isinstance(t, dict):
            if t.get("fontFamily"):
                css.append(f'  --font-{k}: "{t["fontFamily"]}";')
            if t.get("fontSize"):
                css.append(f"  --size-{k}: {t['fontSize']};")
    for k, val in rnd.items():
        css.append(f"  --radius-{k}: {val};")
    for k, val in sp.items():
        css.append(f"  --space-{k}: {val}{'' if str(val).strip()[-1:].isalpha() or str(val).endswith('%') else 'px' if str(val).replace('.','').isdigit() else ''};")
    css.append("}")
    os.makedirs(a.out_dir, exist_ok=True)
    open(os.path.join(a.out_dir, "design-tokens.css"), "w").write("\n".join(css) + "\n")

    tw = {"theme": {"extend": {
        "colors": {k: v for k, v in colors.items()},
        "borderRadius": {k: v for k, v in rnd.items()},
        "spacing": {k: (f"{v}px" if str(v).isdigit() else v) for k, v in sp.items()},
        "fontFamily": {k: [t["fontFamily"]] for k, t in typ.items()
                       if isinstance(t, dict) and t.get("fontFamily")},
    }}}
    open(os.path.join(a.out_dir, "tailwind.tokens.js"), "w").write(
        "/** generated from DESIGN.md */\nmodule.exports = "
        + json.dumps(tw, indent=2) + ";\n")

    print(f"✓ {a.out_dir}/design-tokens.css  ({len(colors)} colors, "
          f"{len(typ)} type, {len(rnd)} radius, {len(sp)} spacing)")
    print(f"✓ {a.out_dir}/tailwind.tokens.js")
    print("image-studio / fb-ad-video-studio: replace template :root values "
          "with @import of design-tokens.css (aliases --accent/--ink/--bg/--mute set).")

if __name__ == "__main__":
    main()
