#!/bin/bash
P=/home/claude/studio/projects/crocs-comeback; T=/home/claude/nextbignow-videos/studio/tools
cd $P
for n in 1 2; do
  rm -f work/flat_*.npz
  CBV=usa_narr python3 scripts/make_vo.py > work/mv_$n.log 2>&1 || CBV=usa_narr python3 scripts/make_vo.py >> work/mv_$n.log 2>&1
  cp work/vo.wav work/vo_n$n.wav; cp work/align.json work/align_n$n.json
  python3 $T/voice_report.py $P work/vo.wav > work/vr_n$n.log 2>&1
  cp work/voice_report.json work/voice_report_n$n.json 2>/dev/null
  echo TAKE $n DONE
done
echo ALLTAKES
