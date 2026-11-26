#!/bin/bash
# patientget.sh <outdir> <list> — one attempt every 5 min until all files arrive (shared IP is rate-limited by Wikimedia)
OUT=$1; LIST=$2
for round in $(seq 1 24); do
  left=0
  while IFS='|' read -r n t; do
    [ -s "$OUT/$n.bin" ] && file "$OUT/$n.bin" | grep -qiE "image|TIFF|PNG|JPEG|RIFF" && continue
    left=1
    if python3 -I /home/claude/studio/tools_ref/commons.py get "$t" "$OUT/$n.bin" >> "$OUT/credits.jsonl" 2>>"$OUT/err.log"; then echo "ok $n"; sleep 20; continue; fi
    rm -f "$OUT/$n.bin"; break
  done < "$LIST"
  [ $left = 0 ] && break
  sleep 300
done
echo GET_DONE
