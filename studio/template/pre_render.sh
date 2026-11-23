#!/bin/bash
# usage: pipeline_post_voice.sh <project dir> <render_x.py> <scenes_x.py> <slug>
# after work/takes.sh: comp (n2 base + n1 alt), trim, align convert, rebuild sketch renderer, mix, thumbnail from frame 1.8, render 3 workers, encode.
set -e
P=$1; R=$2; SC=$3; SLUG=$4; T=/home/claude/nextbignow-videos/studio/tools
cd $P
cp work/vo_n2.wav work/vo.wav; cp work/align_n2.json work/align.json; cp work/voice_report_n2.json work/voice_report.json
python3 $T/comp_takes.py $PWD n1 | tail -n 1
python3 $T/trim_gaps.py $PWD | tail -n 1
python3 - <<'EOF'
import json,re,sys
sys.path.insert(0,'scripts'); from vo_lines import LINES
a=json.load(open('work/align.json')); W=a['words']; Ls=a['lines']
Lend={l['id']:l['end'] for l in Ls} if isinstance(Ls,list) else {k:v['end'] for k,v in Ls.items()}
out=[]
for i,w in enumerate(W):
    nxt=W[i+1]['t'] if i+1<len(W) and W[i+1]['line']==w['line'] else Lend[w['line']]
    end=min(nxt, w['t']+1.2); toks=re.findall(r"[A-Za-z0-9'%]+", w['w'])
    for j,tk in enumerate(toks):
        d=(end-w['t'])/len(toks); out.append([tk,w['t']+j*d,w['t']+(j+1)*d])
json.dump(out,open('comic/cd/align.json','w')); open('comic/cd/script.txt','w').write(' '.join(L[1] for L in LINES)); print('align', out[-1])
EOF
G=/home/claude/studio/projects/grocery-ads/render_grocery.py; M=$(grep -n "^if __name__" $G | cut -d: -f1)
(sed -n 1,322p $G; cat $SC; echo; sed -n "467,$((M-1))p" $G; cat /home/claude/studio/sketch_mode.py; echo; sed -n "$M,\$p" $G) > $R
python3 mix_sfx.py work/vo.wav mix.wav 2>&1 | grep -v Fontconfig || true
MOD=${R%.py}
python3 - <<EOF 2>&1 | grep -v Fontconfig
import numpy as np, skia, $MOD as R
raw=R.frame(1.8).makeImageSnapshot(); arr=raw.toarray(colorType=skia.kRGBA_8888_ColorType)[:,:,:3]
from PIL import Image; Image.fromarray(R._ink(np.ascontiguousarray(arr))).save('thumbnail_$SLUG.png'); print('thumb ok')
EOF
if [ -f cover_spec.txt ]; then python3 /home/claude/studio/cover.py $PWD ${R%.py} "$(sed -n 1p cover_spec.txt)" "$(sed -n 2p cover_spec.txt)" "$(sed -n 3p cover_spec.txt)" $PWD/cover_$SLUG.png 2>&1 | grep -v Fontconfig; fi
[ -f cover_$SLUG.png ] && cp cover_$SLUG.png thumbnail_$SLUG.png && echo 'using cover v3'
