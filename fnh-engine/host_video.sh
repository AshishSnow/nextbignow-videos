#!/bin/bash
# Publish an MP4 at a public raw GitHub URL on a throwaway branch (keeps main small).
# Usage: host_video.sh <slug> push   -> prints RAW_URL=...
#        host_video.sh <slug> delete -> deletes the branch (run AFTER Metricool returns a static.metricool.com media URL)
set -e
SLUG=$1; ACT=$2; BR=v-$SLUG
REMOTE=https://github.com/AshishSnow/nextbignow-videos
if [ "$ACT" = "push" ]; then
  T=$(mktemp -d); cd $T
  git init -q; git checkout -q -b $BR
  cp /home/claude/outputs/$SLUG.mp4 $SLUG.mp4
  git add $SLUG.mp4
  git -c user.name="Claude" -c user.email="noreply@anthropic.com" commit -q -m "media: $SLUG"
  git push -q $REMOTE $BR
  U=https://raw.githubusercontent.com/AshishSnow/nextbignow-videos/$BR/$SLUG.mp4
  curl -sSI $U | grep -qE "^HTTP/2 200" || { sleep 10; curl -sSI $U | grep -qE "^HTTP/2 200"; }
  echo "RAW_URL=$U"
elif [ "$ACT" = "delete" ]; then
  git push -q $REMOTE --delete $BR && echo "deleted $BR"
fi
