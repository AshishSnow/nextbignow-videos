#!/bin/bash
# slowget.sh <outdir> <listfile: name|title>  — polite Commons downloader (60 s gaps, retries)
OUT=$1; LIST=$2
while IFS='|' read -r n t; do
  [ -s "$OUT/$n.bin" ] && continue
  for k in 1 2 3; do
    if python3 -I /home/claude/studio/tools_ref/commons.py get "$t" "$OUT/$n.bin" >> "$OUT/credits.jsonl" 2>>"$OUT/err.log"; then echo "ok $n"; break; fi
    rm -f "$OUT/$n.bin"; echo "retry $n"; sleep 90
  done
  sleep 75
done < "$LIST"
echo GET_DONE
