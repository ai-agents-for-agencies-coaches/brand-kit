---
# DESIGN.md — <CLIENT NAME>  (google-labs-code/design.md · version: alpha)
# Registry: ~/claude_work/brand-kits/<client-slug>/DESIGN.md
# Any line with "TODO: VERIFY" MUST be confirmed against a real client asset
# before this file is used for creative work. Never replace a TODO with a guess.
version: alpha
name: <Client Name>
description: <one line — what the brand stands for>

colors:
  # Sampled from real assets. Hex only, sRGB. primary = core text/ink,
  # neutral = background, tertiary/accent = the single interaction color.
  primary: "#000000"      # TODO: VERIFY — core text / ink
  secondary: "#666666"    # TODO: VERIFY — borders, captions, metadata
  accent: "#0000FF"       # TODO: VERIFY — sole CTA / interaction color
  neutral: "#FFFFFF"      # TODO: VERIFY — background surface
  # add surface-* / state colors only if observed in real assets

typography:
  # fontFamily must be a real, licensed/available font. fontSize in px or rem.
  headline-lg:
    fontFamily: <Font>     # TODO: VERIFY — heading face
    fontSize: 48px
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: -0.02em
  body-md:
    fontFamily: <Font>     # TODO: VERIFY — body face
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.5
  label-caps:
    fontFamily: <Font>     # TODO: VERIFY — eyebrow / label face
    fontSize: 12px
    fontWeight: 600
    letterSpacing: 0.12em

rounded:
  sm: 4px                  # TODO: VERIFY
  md: 8px
  lg: 16px
  full: 999px

spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 32px
  xl: 64px

components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.neutral}"
    rounded: "{rounded.full}"
  button-secondary:
    # outline style: transparent fill, secondary-colored 1px border (see prose)
    backgroundColor: "transparent"
    textColor: "{colors.primary}"
    rounded: "{rounded.full}"
  caption:
    # captions / metadata / supporting text — uses the secondary color
    textColor: "{colors.secondary}"
---

## Overview

<2–3 sentences: the brand's character and the feeling creatives should evoke.
Reference real positioning, not invented adjectives. TODO: VERIFY from the
client's site/brand guide.>

## Colors

- **Primary (`{colors.primary}`):** core text / ink. Where it's used.
- **Secondary (`{colors.secondary}`):** borders, captions, supporting UI.
- **Accent (`{colors.accent}`):** the *only* color that signals action — CTAs,
  links, key emphasis. Use sparingly.
- **Neutral (`{colors.neutral}`):** background foundation.

Contrast: every text/background pair must pass WCAG AA (the linter enforces this).

## Typography

- **Headlines** use `headline-lg`. Tight letter-spacing, confident weight.
- **Body** uses `body-md`. Never set body below 16px on landing pages.
- **Labels/eyebrows** use `label-caps`, uppercase, wide tracking.
- Only the fonts named above. No system-font fallback in finished creatives —
  if a named font isn't available, stop and flag it.

## Layout

<Grid, max content width, section rhythm, edge padding. For ads: 15–25% safe
padding from frame edges minimum. TODO: VERIFY against real client pages.>

## Elevation & Depth

<Shadow language: flat? soft? hard? Realistic offsets only.>

## Shapes

<Corner radius personality (see `rounded`), use of dividers, geometric motifs.>

## Components

- **Buttons:** primary = filled `{colors.accent}`; secondary = outline —
  transparent fill with a 1px `{colors.secondary}` border (border color lives
  in prose, not a token: the spec has no `borderColor` sub-token). Variants
  for hover/pressed go under `button-primary-hover` etc. when known.
- <Add only components actually observed in the client's assets.>

## Do's and Don'ts

**Do**
- Lead with the homeowner's/customer's problem; let the brand be the guide.
- Use `accent` only for action. Keep the palette disciplined.

**Don't**
- Never invent a color, font, or claim. Unknown → `TODO: VERIFY`, then ask.
- Don't retrofit a rationale to justify a guessed value.
