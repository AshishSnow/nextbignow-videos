#!/bin/bash
# Hybrid endings A/B on one example script: Kokoro shipped (make_vo) vs Chatterbox q4 shipped vs Chatterbox + end_contour (2 depths).
# Usage: run.sh <example_name> <lab_slug>
set -e
S=/home/claude/nextbignow-videos/studio; ST=${STUDIO:-/home/claude/studio}; T=$S/tools/tts_bakeoff.py; PC=$S/lab/voice_engine/post_chain.py
P=$(STUDIO=$ST bash $S/new_project.sh $2); cp $S/examples/$1/vo_lines.py $P/scripts/; cd $P
python3 scripts/make_vo.py > work/mkvo.log 2>&1 && python3 $T . score work/vo.wav | grep file
python3 $T . chatterbox --ref $ST/voices/narrator_slow_ref24k.wav --tag cbq4 --lm q4 > work/cb.log 2>&1
python3 $PC work/bake_cbq4.wav work/bake_cbq4_chain.wav && python3 $T . score work/bake_cbq4_chain.wav | grep file
for v in "-4 0"; do set -- $v; tag=v5end${1}_${2}
  python3 $S/lib/end_contour.py work/bake_cbq4.wav work/bake_$tag.wav scripts/vo_lines.py $1 $2 | grep gate
  python3 $PC work/bake_$tag.wav work/bake_${tag}_chain.wav && python3 $T . score work/bake_${tag}_chain.wav | grep file
done
