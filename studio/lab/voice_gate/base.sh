#!/bin/bash
# baseline make_vo on an example script, per-line UTMOS on flat (pre-PSOLA) and shipped vo.wav. Usage: base.sh <example> <slug> [env...]
S=/home/claude/nextbignow-videos/studio; ST=${STUDIO:-/home/claude/studio}
P=$(STUDIO=$ST bash $S/new_project.sh $2); cp $S/examples/$1/vo_lines.py $P/scripts/; cp $S/template/scripts/make_vo.py $P/scripts/; cd $P
shift 2; env "$@" python3 scripts/make_vo.py > work/mkvo.log 2>&1 || { tail work/mkvo.log; exit 1; }
echo "FLAT $(python3 $S/lab/voice_gate/perline.py $P work/vo_flat.wav flat)"
echo "SHIP $(python3 $S/lab/voice_gate/perline.py $P work/vo.wav)"
python3 $S/tools/tts_bakeoff.py $P score work/vo.wav | grep file
