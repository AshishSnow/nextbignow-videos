#!/bin/bash
# usage: finalize_essay.sh <project dir> <module.py> <slug>
set -e; cd "$1"; M=$2; S=$3
python3 $M cover cover_$S.png 2>/dev/null
ls out/ig_*.mp4 | sort | sed "s/^/file '$(pwd | sed 's/\//\\\//g')\//;s/$/'/" > work/ig.txt
ffmpeg -nostdin -v error -y -f concat -safe 0 -i work/ig.txt -c copy work/ig_cat.mp4
for V in ig yt; do
  if [ $V = yt ]; then VF="-filter_complex [0:v][2:v]overlay=0:0:enable='lt(t,0.25)'[v] -map [v]"; EXTRA="-loop 1 -t 1 -i cover_$S.png"; else VF="-map 0:v"; EXTRA=""; fi
  ffmpeg -nostdin -v error -y -i work/ig_cat.mp4 -i mix.wav $EXTRA $VF -c:v libx264 -preset slow -b:v 9000k -pass 1 -passlogfile work/p_$V -an -f mp4 /dev/null
  ffmpeg -nostdin -v error -y -i work/ig_cat.mp4 -i mix.wav $EXTRA $VF -map 1:a -c:v libx264 -preset slow -b:v 9000k -pass 2 -passlogfile work/p_$V -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart final/${S}_$V.mp4
done
ls -la final/
