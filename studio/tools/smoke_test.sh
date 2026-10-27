#!/bin/bash
# Smoke test for template changes: builds a 3-line project (question, low ending, CTA) from the template and runs the voice pipeline with both
# engines, then voice_report. Fails (exit 1) on any error, missing output, ASR bad line or UTMOS < 4.0. ~3 min on 2 CPUs.
# Usage: bash studio/tools/smoke_test.sh
set -e
HERE=$(cd "$(dirname "$0")/.." && pwd); STUDIO=${STUDIO:-/home/claude/studio}
P="$STUDIO/projects/_smoke"; rm -rf "$P"
cp -f "$HERE"/lib/*.py "$STUDIO/lib/"; mkdir -p "$STUDIO/voices"; cp -f "$HERE"/voices/*.npz "$STUDIO/voices/" 2>/dev/null || true
mkdir -p "$P"/{scripts,work,frames}; cp "$HERE"/template/scripts/* "$P/scripts/"
cat > "$P/scripts/vo_lines.py" <<'EOF'
LINES = [
    ("i1", "Do you know your coffee shop is secretly a bank?", 1.04, 0.35, +1.0, 1.45, ["secretly", "bank?"], "q"),
    ("a1", "It keeps about forty cents of every dollar.", 1.04, 0.30, +0.8, 1.45, ["forty", "dollar.:dn"], "low"),
    ("e2", "Send this to the friend who lives at the coffee shop!", 1.06, 0.0, +1.0, 1.45, ["friend", "lives"], None),
]
EOF
fail=0
for eng in kokoro chatterbox; do
  rm -f "$P"/work/*
  (cd "$P" && ENGINE=$eng python3 scripts/make_vo.py > work/make_vo.log 2>&1) || { echo "FAIL $eng: make_vo.py crashed"; tail -5 "$P/work/make_vo.log"; fail=1; continue; }
  if [ $eng = kokoro ]; then grep -q "prosody gate" "$P/work/make_vo.log" || { echo "FAIL kokoro: prosody gate (PGATE) did not run"; fail=1; }; grep "prosody gate" "$P/work/make_vo.log"; fi
  if [ $eng = chatterbox ]; then grep -q "ending moves" "$P/work/make_vo.log" || { echo "FAIL chatterbox: end_contour (ENDS) did not run"; fail=1; }; grep "ending moves" "$P/work/make_vo.log"; fi
  for f in vo.wav align.json; do [ -s "$P/work/$f" ] || { echo "FAIL $eng: missing $f"; fail=1; }; done
  python3 "$HERE/tools/voice_report.py" "$P" > "$P/work/report_$eng.txt" 2>&1 || { echo "FAIL $eng: voice_report"; fail=1; continue; }
  python3 - "$P/work/voice_report.json" "$eng" <<'EOF' || fail=1
import json, sys
r = json.load(open(sys.argv[1])); e = sys.argv[2]
ok = (r.get("utmos") is None or r["utmos"] >= 4.0) and not r.get("asr_bad_lines")
print(("ok  " if ok else "FAIL"), e, "utmos", r.get("utmos"), "range", r.get("f0_range_st"), "wpm", r.get("wpm_speaking"), "asr_bad", r.get("asr_bad_lines"))
sys.exit(0 if ok else 1)
EOF
done
rm -rf "$P"
[ $fail = 0 ] && echo "SMOKE TEST PASSED" || { echo "SMOKE TEST FAILED"; exit 1; }
