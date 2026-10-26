#!/bin/bash
# Full build of an episode whose scripts are written:  bash build_ep.sh NN-slug
# voice (+ASR read-back) -> score -> mix -> 2-part parallel render -> /home/claude/outputs/NN-slug.mp4 + sheet + checks
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
STUDIO=${STUDIO:-/home/claude/studio}; S=$1; P="$STUDIO/projects/$S"; O=/home/claude/outputs/$S.mp4
cd "$P"
[ -f "$HERE/voice.env" ] && { set -a; . "$HERE/voice.env"; set +a; }
[ "$SKIP_VO" = "1" ] || python3 scripts/make_vo.py 2>&1 | grep -v -i warn | tail -3
python3 "$HERE/engine/tools/asr_check.py" "$P" 2>&1 | grep "|"
python3 "$HERE/engine/tools/voice_report.py" "$P" 2>/dev/null | tr -d '\n' | sed 's/  */ /g'; echo
python3 scripts/music.py 2>&1 | grep -v -i "warn\|mean\|ret =" | tail -1
python3 scripts/mix.py 2>&1 | grep "VO/bed"
rm -f frames/*.jpg
bash scripts/render_all.sh > work/render.log 2>&1; tail -1 work/render.log
cp work/final.mp4 "$O"
SZ=$(stat -c %s "$O")
if [ "$SZ" -gt 95000000 ]; then
  ffmpeg -v error -y -i work/final.mp4 -c:v libx264 -preset slow -crf 16 -tune animation -pix_fmt yuv420p -c:a copy -movflags +faststart "$O"
fi
ffprobe -v error -show_entries stream=codec_name,width,height -show_entries format=duration,size -of compact "$O"
ffmpeg -hide_banner -i "$O" -af ebur128=peak=true -f null - 2>&1 | grep -E "^\s+(I|Peak):"
ffmpeg -v error -y -i "$O" -vf "fps=1/2,scale=270:-1,tile=6x5" -frames:v 1 /home/claude/outputs/${S}_sheet.jpg
echo BUILD_OK "$O"
