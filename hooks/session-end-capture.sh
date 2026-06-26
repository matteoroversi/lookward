#!/usr/bin/env bash
# Lookward — Claude Code session-end capture hook (lw-capture, claude-code surface).
# Wire into settings.json as a SessionEnd/Stop hook. Receives the transcript path on stdin
# (JSON with transcript_path) or as $1. Lands an immutable capture in sources/ and commits.
# Mechanical only: it stores the raw signal; the faithful digest happens in lw-enrich.
#
# Config via env: LOOKWARD_WM_ROOT (the world-model bundle), LOOKWARD_WM_NAME.
set -euo pipefail

WM_ROOT="${LOOKWARD_WM_ROOT:?set LOOKWARD_WM_ROOT to your world-model folder}"
WM_NAME="${LOOKWARD_WM_NAME:-$(basename "$WM_ROOT")}"

# transcript_path: from $1, or parsed from stdin JSON
INPUT="${1:-$(cat)}"
TRANSCRIPT="$(printf '%s' "$INPUT" | sed -n 's/.*"transcript_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')"
[ -z "$TRANSCRIPT" ] && TRANSCRIPT="$INPUT" # allow a bare path
[ -f "$TRANSCRIPT" ] || { echo "lw-capture: no transcript at '$TRANSCRIPT'"; exit 0; }

DATE="$(date +%Y-%m-%d)"
SID="$(basename "$TRANSCRIPT" | sed 's/\.[^.]*$//')"
DEST_DIR="$WM_ROOT/sources/ai/claude-code/$DATE"
DEST="$DEST_DIR/$SID.md"

# Idempotent by source_id, across ALL date folders (not just today) — a session
# re-processed on another day must not be captured twice.
if ls "$WM_ROOT"/sources/ai/claude-code/*/"$SID.md" >/dev/null 2>&1; then
 echo "lw-capture: $SID already captured, skipping"; exit 0
fi
mkdir -p "$DEST_DIR"

# Pointer-only capture: we record metadata + a pointer to the raw transcript, NOT the
# transcript inline. Inlining would break markdown fences, bloat the node (the ingest rules),
# and risk committing secrets to permanent git history (the Connector Contract). The faithful
# digest is produced by lw-enrich, which reads `resource` on demand (locally).
{
 echo "---"
 echo "id: claude-code-$SID"
 echo "type: source"
 echo "title: Claude Code session $SID ($DATE)"
 echo "timestamp: $(date -Iseconds)"
 echo "resource: $TRANSCRIPT"
 echo "lookward:"
 echo " world_model: $WM_NAME"
 echo " purpose: \"raw capture of a Claude Code session (pointer)\""
 echo " face: self"
 echo " visibility: private"
 echo " provenance: session"
 echo " confidence: high"
 echo " capture:"
 echo " surface: claude-code"
 echo " source_kind: session-pointer"
 echo " source_id: $SID"
 echo " pull_run: $DATE"
 echo "---"
 echo "# Capture (pointer) — digested by lw-enrich"
 echo
 echo "Raw transcript at \`$TRANSCRIPT\` (not committed). \`lw-enrich\` reads it on demand to produce the faithful digest."
} > "$DEST"

# Commit if the bundle is a git repo (silent if nothing to commit)
if git -C "$WM_ROOT" rev-parse --git-dir >/dev/null 2>&1; then
 git -C "$WM_ROOT" add "$DEST"
 git -C "$WM_ROOT" commit -q -m "lw-capture: Claude Code session $SID ($DATE)" || true
fi
echo "lw-capture: wrote $DEST"
