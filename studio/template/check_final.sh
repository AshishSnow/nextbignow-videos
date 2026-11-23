#!/bin/bash
# check_final.sh <final mp4> <tag> -> scratchpad/<tag>chk.png contact sheet of 9 frames
F=$1; TAG=$2; S=/tmp/claude-0/-home-claude/1a824842-216a-5fb4-b7aa-c9d772e6909f/scratchpad
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $F); echo "dur $D"
rm -f $S/${TAG}_f_*.png
for f in 0.002 0.08 0.2 0.32 0.45 0.58 0.7 0.82 0.97; do t=$(python3 -c "print(round($D*$f,2))"); ffmpeg -v error -y -ss $t -i $F -frames:v 1 -vf scale=216:384 $S/${TAG}_f_$t.png; done
python3 -c "
from PIL import Image; import glob; S='$S'; fs=sorted(glob.glob(S+'/${TAG}_f_*.png'),key=lambda f: float(f.split('_')[-1][:-4])); o=Image.new('RGB',(226*len(fs),384),'white'); [o.paste(Image.open(f),(i*226,0)) for i,f in enumerate(fs)]; o.save(S+'/${TAG}chk.png')"
