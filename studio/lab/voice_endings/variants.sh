#!/bin/bash
# re-run only the end_contour variants on an existing lab project: variants.sh <project> "<low> <q>" ...
S=/home/claude/nextbignow-videos/studio; T=$S/tools/tts_bakeoff.py; PC=$S/lab/voice_engine/post_chain.py; cd $1; shift
for v in "$@"; do set -- $v; tag=v6end${1}_${2}
  python3 $S/lib/end_contour.py work/bake_cbq4.wav work/bake_$tag.wav scripts/vo_lines.py $1 $2 | grep gate
  python3 $PC work/bake_$tag.wav work/bake_${tag}_chain.wav && python3 $T . score work/bake_${tag}_chain.wav | grep file
done
