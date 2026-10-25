#!/bin/bash
# Create a new video project from the template.  Usage: bash studio/new_project.sh <slug>
# -> $STUDIO/projects/<slug>/{scripts,work,frames}; edit scripts/vo_lines.py, anim_shots.py, music.py (cues), mix.py (SFX).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
STUDIO=${STUDIO:-/home/claude/studio}
P="$STUDIO/projects/$1"
[ -n "$1" ] || { echo "usage: new_project.sh <slug>"; exit 1; }
mkdir -p "$P"/{scripts,work,frames}
for f in "$HERE"/template/scripts/*; do [ -e "$P/scripts/$(basename "$f")" ] || cp "$f" "$P/scripts/"; done
chmod +x "$P/scripts/render_all.sh"
echo "$P"
