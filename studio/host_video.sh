#!/bin/bash
# Host an MP4 at a public raw GitHub URL on a throwaway branch (keeps main small).
# Usage: host_video.sh push <file.mp4> <slug>  -> prints RAW_URL=...
#        host_video.sh delete <slug>            -> deletes the branch (only AFTER Metricool returned a static.metricool.com media URL)
set -e
ACT=$1; REMOTE=https://github.com/AshishSnow/nextbignow-videos
if [ "$ACT" = "push" ]; then
  F=$2; SLUG=$3; BR=omb-$SLUG
  T=$(mktemp -d); cd "$T"
  git init -q; git checkout -q -b "$BR"
  cp "$F" "$SLUG.mp4"; git add "$SLUG.mp4"
  git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "media: $SLUG"
  git push -q "$REMOTE" "$BR"
  U=https://raw.githubusercontent.com/AshishSnow/nextbignow-videos/$BR/$SLUG.mp4
  for i in 1 2 3 4 5 6; do curl -sSI "$U" | grep -qE "^HTTP/2 200" && break; sleep 10; done
  echo "RAW_URL=$U"; rm -rf "$T"
elif [ "$ACT" = "delete" ]; then
  git push -q "$REMOTE" --delete "omb-$2" && echo "deleted omb-$2"
else
  echo "usage: host_video.sh push <file.mp4> <slug> | delete <slug>"; exit 1
fi
