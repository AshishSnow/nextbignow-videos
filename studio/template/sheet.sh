#!/bin/bash
# sheet.sh <dir> <module> <name> t1 t2 ...
cd $1; M=$2; N=$3; shift 3; rm -f out/*.png; python3 $M still "$@" 2>&1 | grep -v Fontc
python3 -c "
from PIL import Image; import glob
fs=sorted(glob.glob('out/ig_*.png')); ims=[Image.open(f).resize((360,640)) for f in fs]
cols=6; rows=(len(ims)+cols-1)//cols
W=Image.new('RGB',(360*cols,640*rows),'white')
for i,im in enumerate(ims): W.paste(im,((i%cols)*360,(i//cols)*640))
W.save('/tmp/claude-0/-home-claude/1a824842-216a-5fb4-b7aa-c9d772e6909f/scratchpad/$N.png')"
