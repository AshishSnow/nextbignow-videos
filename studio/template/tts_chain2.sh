#!/bin/bash
for d in "$@"; do
  cd /home/claude/studio/projects/$d; bash work/takes.sh > work/takes.log 2>&1
  echo 'import sys' > render_dummy.py; bash /home/claude/studio/pre_render.sh $PWD render_dummy.py /dev/null x > work/pre.log 2>&1; rm -f render_dummy.py thumbnail_x.png
  echo "VO_DONE $d $(grep -E 'trimmed' work/pre.log | tail -1)"
done
echo CHAIN_DONE
