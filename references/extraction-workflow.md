# Client brand extraction — SOP

The goal: a registered, lint-clean DESIGN.md per client, built from **real evidence only**.

## 1. Gather evidence (real sources, in priority order)

1. A brand/style guide the client provided (PDF/Figma) — highest authority.
2. The client's live website (CSS + rendered screenshots).
3. Their logo file (vector preferred; PNG ok).
4. Their existing high-performing ads/creatives (sample with PIL).

If none exist, you cannot produce an authoritative DESIGN.md — say so and ask the client.

## 2. Auto-draft

```bash
python3 scripts/extract-brand.py --url https://client.com --client <slug> [--logo logo.png]
```

Produces `~/claude_work/brand-kits/<slug>/DESIGN.md`. The script:
- frequency-ranks hex colors from inline + linked CSS,
- pulls the dominant `font-family` stacks,
- (with `--logo`) quantizes the logo's dominant colors,
- writes confidently-detected values with a `# source:` note,
- writes everything else as `# TODO: VERIFY`.

## 3. Human verification gate (mandatory)

Walk the draft with the user. For every field:
- **Detected** → confirm it's actually the brand value (a common CSS color is not automatically the *brand* color — e.g. a framework default). Downgrade to TODO if unsure.
- **TODO: VERIFY** → get the real value from the client, or mark the brand as "unknown — needs client input". Never replace a TODO with a plausible guess.
- Fonts → confirm the family is licensed/available; record where it loads from.
- Write the `Overview`, `Layout`, `Do's and Don'ts` prose from real positioning, not invented adjectives.

A draft with any unresolved `TODO: VERIFY` is **not** usable for creative work. `lint.sh` and `sync.sh` both refuse it.

## 4. Lint (quality gate)

```bash
bash scripts/lint.sh ~/claude_work/brand-kits/<slug>/DESIGN.md
```

Fix every error and every WCAG-AA contrast failure (adjust the token, or document an approved exception in the Colors prose with the real reason — never silence it with a guess).

## 5. Register + propagate

The verified, lint-clean file is now authoritative. For each active project:

```bash
bash scripts/sync.sh <slug> <project-dir>
python3 scripts/tokens-to-css.py <project-dir>/DESIGN.md --out-dir <project-dir>
```

## Why this is strict

A fabricated brand value survives into ads and landing pages and erodes client trust. The TODO-gate + lint-gate make "I assumed" structurally impossible: the value is either evidenced, confirmed by the client, or explicitly unknown. See the `feedback_never_fabricate_brand_details` rule — this skill is its enforcement mechanism.
