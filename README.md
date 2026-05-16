# brand-kit

**One verified source of truth for every client's brand — so every ad and landing page is on-brand, and nothing is ever guessed.**

Built on the open [**DESIGN.md**](https://github.com/google-labs-code/design.md) standard (`@google/design.md`). A Claude Code skill that auto-extracts a client's visual identity into a validated `DESIGN.md`, keeps a central registry, and feeds the tokens into [`image-studio`](https://github.com/ai-agents-for-agencies-coaches/image-studio), [`fb-ad-video-studio`](https://github.com/ai-agents-for-agencies-coaches/fb-ad-video-studio), and landing pages.

## Why

Brand drift and invented colors erode client trust. This skill makes "I assumed the brand color" structurally impossible: every value is either evidenced from a real asset, confirmed by the client, or explicitly marked unknown. The linter additionally enforces WCAG AA contrast before anything ships.

## What DESIGN.md is

YAML front-matter **tokens** (`colors`, `typography`, `rounded`, `spacing`, `components`) + a markdown **body** (Overview, Colors, Typography, Layout, Components, Do's and Don'ts). Tokens are normative; prose says how to apply them. Validated by `npx @google/design.md lint` (broken refs + contrast) and `diff` (brand regression). Offline spec: [`references/spec-summary.md`](references/spec-summary.md).

## Install

```bash
git clone https://github.com/ai-agents-for-agencies-coaches/brand-kit.git \
  ~/.claude/skills/brand-kit
cd ~/.claude/skills/brand-kit && npm install
```

Claude auto-discovers it via `SKILL.md`. Then: *"set up the brand kit for <client>"* or *"is there a DESIGN.md for this client?"*

## Per-client workflow

```
extract  → python3 scripts/extract-brand.py --url <site> --client <slug> [--logo logo.png]
verify   → resolve every "TODO: VERIFY" with the user           (mandatory gate)
lint     → bash scripts/lint.sh ~/claude_work/brand-kits/<slug>/DESIGN.md   (WCAG gate)
register → the verified, lint-clean file is authoritative
propagate→ bash scripts/sync.sh <slug> <project-dir>
consume  → python3 scripts/tokens-to-css.py <project-dir>/DESIGN.md
```

| Script | Does |
|--------|------|
| `extract-brand.py` | Drafts DESIGN.md from real site CSS / logo; flags unknowns as `TODO: VERIFY` (never guesses) |
| `lint.sh` | `@google/design.md lint` + TODO check; optional `diff` for regression |
| `sync.sh` | Copies registry → project with a synced-from header; detects drift |
| `tokens-to-css.py` | Emits `:root{}` CSS (incl. `--accent/--ink/--bg/--mute` aliases) + Tailwind theme |

## Where files live

- **Registry (authoritative):** `~/claude_work/brand-kits/<client-slug>/DESIGN.md`
- **Per project (synced copy, do not hand-edit):** `<project>/DESIGN.md`

## Integration

`image-studio`, `fb-ad-video-studio`, and landing pages all run a pre-flight check: a project DESIGN.md → use its tokens; missing/with-TODOs → extract + verify first, never hardcode. HyperFrames reads `DESIGN.md` natively, so syncing it into a video composition is zero-config. Full wiring in [`references/integration.md`](references/integration.md); extraction SOP in [`references/extraction-workflow.md`](references/extraction-workflow.md).

## License

MIT — see [LICENSE](LICENSE). The DESIGN.md format is by Google Labs (`google-labs-code/design.md`).
