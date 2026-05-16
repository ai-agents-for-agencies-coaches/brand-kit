# DESIGN.md spec — condensed (offline copy)

Source: `github.com/google-labs-code/design.md` (`docs/spec.md`, version `alpha`). Read this instead of hitting the network.

## Structure

Two layers in one file:

1. **YAML front matter** (between `---` fences) — machine-readable tokens. Normative.
2. **Markdown body** (`##` sections) — human rationale for *how* to apply tokens.

Prose may use descriptive names ("Boston Clay"); tokens use systematic names (`tertiary`). Tokens win.

## Token schema

```yaml
version: alpha            # optional
name: <string>            # required
description: <string>     # optional
colors:
  <token>: "#RRGGBB"      # hex, sRGB, must start with #
typography:
  <token>:
    fontFamily: <string>
    fontSize: <dimension>           # px or rem
    fontWeight: <number>            # 400, 700…
    lineHeight: <dimension|number>
    letterSpacing: <dimension>
rounded:
  <level>: <dimension>    # xs|sm|md|lg|xl|full or any string key
spacing:
  <level>: <dimension|number>
components:
  <name>:
    <prop>: <string | token reference>
```

**Token references:** `{path.to.token}` → must point at a primitive (e.g. `{colors.primary}`), except inside `components` where composite refs are allowed (e.g. `{typography.label-md}`).

**Conventional names:** typography — `headline-display`, `headline-lg`, `headline-md`, `body-lg`, `body-md`, `body-sm`, `label-lg`, `label-md`, `label-sm`. Any descriptive key is still valid.

**Component variants:** suffix the state — `button-primary`, `button-primary-hover`, `button-primary-active`. Common components: Buttons, Chips, Lists, Tooltips, Checkboxes, Radio buttons, Input fields. (Component spec is evolving — flexible by design.)

## Recommended body sections

`Overview` (a.k.a. Brand & Style) · `Colors` · `Typography` · `Layout` (a.k.a. Layout & Spacing) · `Elevation & Depth` · `Shapes` · `Components` · `Do's and Don'ts`.

## Validation behavior

| Scenario | Behavior |
|---|---|
| Unknown section heading | preserve, no error |
| Unknown color/typography token name | accept if value valid |
| Unknown spacing value | accept (stored as string) |
| Unknown component property | accept **with warning** |
| Duplicate section heading | **error — file rejected** |

## CLI

```bash
npx @google/design.md lint DESIGN.md            # refs + WCAG contrast → JSON findings
npx @google/design.md diff DESIGN.md DESIGN-v2.md   # token + prose regression
```

`lint` emits `{ findings:[{severity,path,message}], summary:{errors,warnings,info} }`. Treat `errors > 0` or any failing contrast as a hard gate.
