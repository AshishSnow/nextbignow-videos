#!/bin/bash
# render_wide.sh dir module slug [procs]  -- 16:9 long-form: render in N chunks, concat, mux mix.wav, thumbnail
d=$1; m=$2; s=$3; NP=${4:-3}; cd /home/claude/studio/projects/$d; export OMB_WIDE=1
N=$(python3 $m nframes 2>/dev/null); rm -f out/ig_*.mp4; mkdir -p out final
for k in $(seq 0 $((NP-1))); do a=$((k*N/NP)); b=$(((k+1)*N/NP)); python3 $m range $a $b 2>/dev/null & done; wait
ls out/ig_*.mp4 | sort | sed "s|^|file '$PWD/|; s|$|'|" > out/list.txt
ffmpeg -nostdin -v error -y -f concat -safe 0 -i out/list.txt -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart final/$s.mp4
python3 $m cover thumb_full.png 2>/dev/null && ffmpeg -nostdin -v error -y -i thumb_full.png -vf scale=1280:720 final/${s}_thumb.png
echo "RENDERED $s $(ffprobe -v error -show_entries format=duration -of csv=p=0 final/$s.mp4) frames=$N"
