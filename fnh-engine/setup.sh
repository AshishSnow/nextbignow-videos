#!/bin/bash
# FreshNestHub engine v4 setup (fresh workspace, idempotent, ~3-5 min):
# installs the animation/voice studio (vendored copy in engine/) into $STUDIO (default /home/claude/studio).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
export STUDIO=${STUDIO:-/home/claude/studio}
bash "$HERE/engine/setup.sh"
if [ ! -f /usr/share/fonts/opentype/inter/InterDisplay-Black.otf ]; then
  (apt-get install -y -q fonts-inter >/dev/null 2>&1) || echo "WARNING: fonts-inter could not be installed"
fi
# ep 27: hand-lettering font for the draw-on board kit (Architects Daughter, SIL OFL 1.1, Google Fonts)
mkdir -p "$STUDIO/fonts/hand"
[ -f "$STUDIO/fonts/hand/ArchitectsDaughter-Regular.ttf" ] || curl -sSfL -o "$STUDIO/fonts/hand/ArchitectsDaughter-Regular.ttf" "https://raw.githubusercontent.com/google/fonts/main/ofl/architectsdaughter/ArchitectsDaughter-Regular.ttf" || echo "WARNING: hand font missing (board text falls back to the bold sans)"
mkdir -p /home/claude/outputs
echo "FNH ENGINE READY"
