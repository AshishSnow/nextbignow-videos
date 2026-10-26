#!/bin/bash
# Create an episode project:  bash new_ep.sh NN-slug   -> prints the project dir ($STUDIO/projects/NN-slug)
# scripts = studio template + FreshNestHub template (Chubby mascot, props, last approved episode as the example).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
STUDIO=${STUDIO:-/home/claude/studio}
[ -n "$1" ] || { echo "usage: new_ep.sh NN-slug"; exit 1; }
P="$STUDIO/projects/$1"
mkdir -p "$P"/{scripts,work,frames}
cp "$HERE"/engine/template/* "$P/scripts/"
cp "$HERE"/template/* "$P/scripts/"
chmod +x "$P/scripts/render_all.sh"
echo "$P"
