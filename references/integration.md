# Integrating DESIGN.md into the ads + landing-page process

The DESIGN.md is upstream of every creative. Order of operations for any client work:

```
brand-kit (extract → verify → lint → register)
        │
        ├─ sync.sh → <ad project>/DESIGN.md ──→ image-studio / fb-ad-video-studio
        └─ sync.sh → <landing project>/DESIGN.md ──→ tokens-to-css.py → stylesheet/Tailwind
```

## Pre-flight check (all creative skills)

Before producing any client creative, the agent MUST:

1. Look for `DESIGN.md` (or `design.md`) in the project root, else in `~/claude_work/brand-kits/<slug>/`.
2. **Found + lint-clean + no TODOs** → use its tokens. Do not hardcode or sample new colors.
3. **Found with TODOs / lint errors** → stop, resolve with the user first.
4. **Not found** → run `brand-kit` extraction, get human verification, *then* proceed. Never guess. (This operationalizes the standing "never fabricate brand details" rule.)

## image-studio (statics)

- The reverse-template color-sampling step **is** `extract-brand.py` — sample into a DESIGN.md, don't bake hexes into one template.
- Generate `design-tokens.css` via `tokens-to-css.py`. In the template `<head>`, replace the literal `:root{}` with:
  `<link rel="stylesheet" href="design-tokens.css">` (it sets `--accent --ink --bg --mute` aliases the templates already use, plus `--color-*`, `--font-*`).
- Typography: load the DESIGN.md `fontFamily` values as the Google Fonts/`@font-face` faces. If a named font isn't available, stop and flag — no system fallback in finished creatives.

## fb-ad-video-studio (video)

- HyperFrames reads `design.md`/`DESIGN.md` natively from the composition project root — so `sync.sh <slug> <comp-project>` makes brand colors/fonts authoritative for the whole render with no code change.
- Also run `tokens-to-css.py` and swap the template `:root` block for the generated one so kinetic type, captions, lockup, and PIP borders inherit `--accent/--ink/--bg`.
- Keep the proven structure/pacing; only the brand layer comes from DESIGN.md.

## Landing pages

- `sync.sh` the client file in, then `tokens-to-css.py`.
- Plain CSS: `@import "design-tokens.css";` and reference `var(--color-*)`, `var(--font-*)`, `var(--radius-*)`, `var(--space-*)`.
- Tailwind: merge `tailwind.tokens.js` into `theme.extend`.
- **Gate before deploy:** `lint.sh` must pass (WCAG contrast is enforced there) — this prevents shipping low-contrast hero/CTA combinations.

## Audit / regression

To check whether an existing asset or a redesign drifted from brand:
`bash scripts/lint.sh <new>/DESIGN.md <registry>/DESIGN.md` → the `diff` reports added/removed/modified tokens and flags `regression: true`.

## Drift control

Registry (`~/claude_work/brand-kits/<slug>/DESIGN.md`) is authoritative. Project copies carry a synced-from header and must not be hand-edited. Re-running `sync.sh` shows drift and re-pulls from the registry. Edit brand only in the registry, then re-sync + re-generate tokens for every active project.
