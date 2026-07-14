#!/usr/bin/env bash
# TOPH CORTEX · SessionEnd / Stop hook.
# Fires at the end of a Claude Code session. It does NOT write to main memory —
# it runs the mechanical half (consolidation clustering + the referee) and leaves
# any distilled skill as a STAGED draft for review. The battery (a model call to
# finish a staged skill) is spent deliberately, not silently, by /consolidate.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "[toph-cortex] session end — running mechanical consolidation + referee (no writes to main)"
python bin/consolidate.py --min 2 || true
python bin/referee.py    || true
python bin/cortex.py --learn || true
echo "[toph-cortex] staged drafts (if any) in memory/_staging/ await validation before commit."
