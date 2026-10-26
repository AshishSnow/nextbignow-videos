#!/bin/bash
# Render the project in two parallel halves, then join + mux with work/mix.wav -> work/final.mp4
O=$(cd "$(dirname "$0")/.." && pwd)
N=$(python3 -c "import json;print(round((json.load(open('$O/work/align.json'))['dur']+1.5)*24))"); H=$((N/2))
python3 -I $O/scripts/anim.py $O/work/part1.mp4 0:$H > $O/work/r1.log 2>&1 &
python3 -I $O/scripts/anim.py $O/work/part2.mp4 $H:$N > $O/work/r2.log 2>&1 &
wait
printf "file '%s'\nfile '%s'\n" $O/work/part1.mp4 $O/work/part2.mp4 > $O/work/parts.txt
ffmpeg -v error -y -f concat -safe 0 -i $O/work/parts.txt -i $O/work/mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 320k -ar 48000 -shortest -movflags +faststart $O/work/final.mp4
echo ALLDONE $N
