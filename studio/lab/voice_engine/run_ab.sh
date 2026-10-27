#!/bin/bash
# A/B on one project: shipped Kokoro (make_vo.py) vs Chatterbox-Turbo q4 + slow synthetic reference, both through the shipped chain.
# Usage: run_ab.sh <project_dir> <ref.wav>
P=$1; REF=$2; T=/home/claude/nextbignow-videos/studio/tools/tts_bakeoff.py; L=$(dirname "$0")/post_chain.py
cd $P && python3 scripts/make_vo.py > work/mkvo.log 2>&1 && python3 $T . score work/vo.wav | grep file
python3 $T . chatterbox --ref $REF --tag cbq4 --lm q4 | grep file
python3 $L work/bake_cbq4.wav work/bake_cbq4_chain.wav && python3 $T . score work/bake_cbq4_chain.wav | grep file
