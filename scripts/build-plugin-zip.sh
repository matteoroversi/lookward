#!/usr/bin/env bash
# Build a single .zip of the WHOLE plugin for upload to claude.ai / Cowork / Desktop
# (Customize → Plugins → Upload plugin). The plugin — .claude-plugin/, skills/, hooks/,
# schedule/, the shared ontology/contract.md, README, LICENSE — is the distribution unit;
# the shared contract travels with it (skills reference it by relative path).
#
# Includes only the public/tracked set (git-ignored private docs, .cache, dist never enter).
# Usage:  ./scripts/build-plugin-zip.sh   →  dist/lookward-plugin.zip
set -euo pipefail
cd "$(dirname "$0")/.."
command -v zip >/dev/null || { echo "need 'zip' installed"; exit 1; }

DIST="dist"; mkdir -p "$DIST"
stage="$(mktemp -d)/lookward"; mkdir -p "$stage"

# the public set = tracked + untracked-non-ignored, minus dist/ itself
git ls-files --cached --others --exclude-standard | grep -v '^dist/' | while read -r f; do
  mkdir -p "$stage/$(dirname "$f")"
  cp "$f" "$stage/$f"
done

rm -f "$DIST/lookward-plugin.zip"
# reproducible: fixed mtimes + no extra attrs, so rebuilding identical content yields identical bytes
find "$stage" -exec touch -t 200001010000 {} +
( cd "$stage/.." && zip -qrX "$OLDPWD/$DIST/lookward-plugin.zip" lookward )
rm -rf "$(dirname "$stage")"
echo "✓ $DIST/lookward-plugin.zip"
echo "Upload it: claude.ai/Cowork/Desktop → Customize → Plugins → Upload plugin."
