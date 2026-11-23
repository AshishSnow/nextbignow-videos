#!/bin/bash
# host_file.sh <file> <slug>  -> RAW_URL for any file type (keeps extension)
set -e
F=$1; SLUG=$2; EXT=${F##*.}; BR=omb-$SLUG; REMOTE=https://github.com/AshishSnow/nextbignow-videos
T=$(mktemp -d); cd "$T"; git init -q; git checkout -q -b "$BR"
cp "$F" "$SLUG.$EXT"; git add "$SLUG.$EXT"
git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "media: $SLUG"
git push -q -f "$REMOTE" "$BR"
U=https://raw.githubusercontent.com/AshishSnow/nextbignow-videos/$BR/$SLUG.$EXT
for i in 1 2 3 4 5 6; do curl -sSI "$U" | grep -qE "^HTTP/2 200" && break; sleep 10; done
echo "RAW_URL=$U"; rm -rf "$T"
