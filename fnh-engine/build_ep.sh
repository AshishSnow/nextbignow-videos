#!/bin/bash
# Build one episode end to end.
# Usage: build_ep.sh <slug>      e.g. build_ep.sh 02-carmine-lipstick
# episodes/<slug>/ must contain: lines.py voice.py timeline.py render.py music.py mix.py
# Output: /home/claude/outputs/<slug>.mp4 (+ <slug>_sheet.jpg contact sheet)
set -e
R=$(cd "$(dirname "$0")" && pwd)
E=$R/episodes/$1
K=/home/claude/reel-kit/english; S=$K/scripts; W=$K/work
[ -d "$E" ] || { echo "no episode dir $E"; exit 1; }
mkdir -p $W /home/claude/outputs
cp $E/lines.py $S/vo_lines.py
cd /tmp
echo "== voice";    python3 -I $E/voice.py
echo "== align";    python3 -I $S/align_en.py $W/take.wav 1.0 | tail -16
echo "== timeline"; python3 -I $E/timeline.py
echo "== music";    python3 -I $E/music.py
echo "== mix";      python3 -I $E/mix.py
N=$(python3 -c "import json;print(int(round(json.load(open('$W/timeline.json'))['END']*30)))"); H=$((N/2))
echo "== render $N frames (2 parallel segments)"
SEG_A=0 SEG_B=$H python3 -I $E/render.py $W/seg_a.mp4 > $W/seg_a.log 2>&1 &
PA=$!
SEG_A=$H SEG_B=999999 python3 -I $E/render.py $W/seg_b.mp4 > $W/seg_b.log 2>&1
wait $PA
grep -q "^done" $W/seg_a.log && grep -q "^done" $W/seg_b.log || { echo "RENDER FAILED"; tail -20 $W/seg_a.log $W/seg_b.log; exit 1; }
printf "file '%s'\nfile '%s'\n" $W/seg_a.mp4 $W/seg_b.mp4 > $W/segs.txt
ffmpeg -v error -y -f concat -safe 0 -i $W/segs.txt -c copy $W/video.mp4
O=/home/claude/outputs/$1.mp4
ffmpeg -v error -y -i $W/video.mp4 -i $W/mix.wav -map 0:v -map 1:a -c:v libx264 -preset slow -crf 18 -maxrate 9M -bufsize 18M \
  -profile:v high -pix_fmt yuv420p -colorspace bt709 -color_primaries bt709 -color_trc bt709 -color_range tv \
  -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart $O
echo "== verify"
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate:format=duration,size -of compact $O
ffmpeg -hide_banner -i $O -af ebur128=peak=true -f null - 2>&1 | grep -E "I:|Peak:" | tail -2
python3 -I $S/contact_sheet.py $O /home/claude/outputs/$1_sheet.jpg 2.0
echo "BUILD_OK $O"
