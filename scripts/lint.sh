#!/usr/bin/env bash
# Validate a DESIGN.md against the spec: broken token refs + WCAG contrast.
# This is the QUALITY GATE — a file with errors, or unresolved TODO: VERIFY,
# must not be used for creative work.
#
# Usage:  bash scripts/lint.sh path/to/DESIGN.md [path/to/OTHER.md]   # 2nd = diff
set -euo pipefail
F="${1:?path to DESIGN.md}"

if grep -nq "TODO: VERIFY" "$F"; then
  echo "✗ Unresolved TODO: VERIFY lines — resolve with the client before use:"
  grep -n "TODO: VERIFY" "$F"
  echo
fi

echo "→ npx @google/design.md lint $F"
npx --yes @google/design.md lint "$F"

if [[ -n "${2:-}" ]]; then
  echo
  echo "→ diff vs $2 (brand regression check)"
  npx --yes @google/design.md diff "$F" "$2"
fi
