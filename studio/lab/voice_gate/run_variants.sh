#!/bin/bash
# wait for A loop, then PG variants reusing the flat cache
while pgrep -f "runB.sh PG15" >/dev/null; do sleep 10; done
S=/home/claude/nextbignow-videos/studio; PR=/home/claude/studio/projects
for tag in "$@"; do
 for s in gasstation duolingostreak airlinemiles; do
  mkdir -p $PR/lab_1027r3_${s}_$tag/work; cp $PR/lab_1027r3_${s}_A/work/flat_*.npz $PR/lab_1027r3_${s}_$tag/work/
  case $tag in PG15) E="PGATE=0.15";; PG10) E="PGATE=0.10";; PG20) E="PGATE=0.20";; PUCK) E="PGATE=0.15 VMIX=am_michael:0.45,am_eric:0.3,am_fenrir:0.15,am_puck:0.1";; CL) E="CLIPLO=-7 CLIPHI=8";; CLPG) E="CLIPLO=-7 CLIPHI=8 PGATE=0.15";; esac
  MV=$S/lab/voice_gate/make_vo_pg.py bash $S/lab/voice_gate/base2.sh $s lab_1027r3_${s}_$tag $E > /home/claude/rr/${s}_$tag.log 2>&1
  grep "prosody gate" $PR/lab_1027r3_${s}_$tag/work/mkvo.log >> /home/claude/rr/${s}_$tag.log
 done
done
