#!/bin/bash
# render_all.sh dir:module:slug ...
for spec in "$@"; do
  IFS=: read d m s <<< "$spec"; cd /home/claude/studio/projects/$d
  N=$(python3 $m nframes 2>/dev/null); rm -f out/ig_*.mp4; a=$((N/3)); b=$((2*N/3))
  python3 $m range 0 $a 2>/dev/null & python3 $m range $a $b 2>/dev/null & python3 $m range $b $N 2>/dev/null & wait
  bash /home/claude/studio/finalize_essay.sh $PWD $m $s > /dev/null 2>&1 && /home/claude/studio/check_final.sh $PWD/final/${s}_yt.mp4 $s > /dev/null 2>&1
  echo "RENDERED $d $(ls -la final/${s}_ig.mp4 | awk '{print $5}')"
done
echo RENDER_ALL_DONE
