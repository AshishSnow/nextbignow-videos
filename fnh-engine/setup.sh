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
mkdir -p /home/claude/outputs
echo "FNH ENGINE READY"
