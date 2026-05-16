#!/usr/bin/env bash
# Copy the authoritative registry DESIGN.md into a client project, with a
# header pointing back to the registry. Re-running diffs to detect drift.
#
# Usage:  bash scripts/sync.sh <client-slug> <project-dir> [registry-root]
set -euo pipefail
SLUG="${1:?client slug}"
PROJ="${2:?project dir}"
REG="${3:-$HOME/claude_work/brand-kits}"
SRC="$REG/$SLUG/DESIGN.md"
DST="$PROJ/DESIGN.md"

[[ -f "$SRC" ]] || { echo "✗ no registry file: $SRC (run extract-brand.py first)"; exit 1; }
if grep -q "TODO: VERIFY" "$SRC"; then
  echo "✗ registry file still has TODO: VERIFY — verify + lint before syncing."; exit 1
fi

if [[ -f "$DST" ]]; then
  if diff -q "$SRC" <(tail -n +3 "$DST" 2>/dev/null || cat "$DST") >/dev/null 2>&1; then
    echo "✓ $DST already in sync with registry"; exit 0
  fi
  echo "⚠ project copy differs from registry — showing drift:"
  diff "$DST" "$SRC" || true
  echo "Overwriting project copy with registry (registry is authoritative)…"
fi

{
  echo "<!-- SYNCED from registry: $SRC — do not edit here; edit the registry then re-run sync.sh -->"
  echo
  cat "$SRC"
} > "$DST"
echo "✓ $SLUG → $DST"
echo "Next: python3 scripts/tokens-to-css.py $DST  (emit CSS/Tailwind tokens)"
