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
N=$(python3 $R nframes 2>/dev/null | tail -n 1); Q=$(( (N + 2) / 3 )); echo "frames $N"
rm -f out/*.mp4 out/*.png work/ig.txt work/yt.txt work/*_cat.mp4
for i in 0 1 2; do a=$((i*Q)); b=$(( (i+1)*Q )); [ $b -gt $N ] && b=$N; python3 $R range $a $b > work/r$i.log 2>&1 & done
wait
for v in ig yt; do ls out/${v}_0*.mp4 | sort | sed "s#^#file '$PWD/#;s#\$#'#" > work/$v.txt
ffmpeg -nostdin -v error -y -f concat -safe 0 -i work/$v.txt -c copy work/${v}_cat.mp4; done
mkdir -p final
for v in ig yt; do
 if [ $v = yt ]; then IN="-i work/yt_cat.mp4 -loop 1 -t 0.2 -i thumbnail_$SLUG.png"; FC="[1:v]scale=1080:1920,setsar=1,fps=30[t];[0:v][t]overlay=eof_action=pass:enable='lt(t,0.2)'[v]"; AI=2; else IN="-i work/ig_cat.mp4"; FC="[0:v]null[v]"; AI=1; fi
 ffmpeg -nostdin -v error -y $IN -filter_complex "$FC" -map "[v]" -c:v libx264 -b:v 9000k -preset slow -pass 1 -passlogfile work/p_$v -an -f mp4 /dev/null
 ffmpeg -nostdin -v error -y $IN -i mix.wav -filter_complex "$FC" -map "[v]" -map $AI:a -c:v libx264 -b:v 9000k -preset slow -pass 2 -passlogfile work/p_$v -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart final/${SLUG}_$v.mp4
done
ls -la final
