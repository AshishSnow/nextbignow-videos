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
# video path (R&D Visuals run, 28 Oct): template + the Hoover example's shots with fake timings -> layout_check renders frames
# (captions inside the UI safe area, frame 0 not empty) and anim.py encodes 1 s of real video. ~2 min.
PV="$STUDIO/projects/_smoke_video"; rm -rf "$PV"; mkdir -p "$PV"/{scripts,work,frames}
cp "$HERE"/template/scripts/* "$PV/scripts/"; cp "$HERE"/examples/hoover/* "$PV/scripts/"
if python3 "$HERE/tools/layout_check.py" "$PV" --fake-align --step 30 --no-sheet --json "$PV/work/layout.json" > "$PV/work/layout.txt" 2>&1 \
   && (cd "$PV" && python3 scripts/anim.py work/smoke.mp4 0:24 > work/anim.log 2>&1) && python3 - "$PV" <<'EOF'
import json, subprocess, sys
P = sys.argv[1]; r = json.load(open(f"{P}/work/layout.json")); s = r["summary"]
early = [x for x in r["rows"] if x["t"] <= 3 and x["bad_px"] > 150]
n = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames,width,height",
                    "-of", "csv=p=0", f"{P}/work/smoke.mp4"], capture_output=True, text=True).stdout.strip()
ok = not early and s["f0_core_detail"] >= 0.005 and s["caption_frames"] > 0 and n == "1080,1920,24"
print(("ok  " if ok else "FAIL"), "video: layout first 3 s violations", len(early), "| frame-0 detail", s["f0_core_detail"],
      "| caption frames", s["caption_frames"], "| encoded", n)
sys.exit(0 if ok else 1)
EOF
then :; else echo "FAIL video path (layout_check / anim.py)"; tail -5 "$PV/work/layout.txt" "$PV/work/anim.log" 2>/dev/null; fail=1; fi
rm -rf "$PV"
python3 "$HERE/tools/story_check.py" --all "$HERE/examples" > /dev/null && python3 "$HERE/tools/story_check.py" "$P" > /dev/null \
  && echo "ok   story_check" || { echo "FAIL story_check.py crashed"; fail=1; }
# writers' room pre-flight (R&D Tooling run, 31 Oct): every queued board parses; the pilot's story-kit assets all exist (--strict)
python3 "$HERE/tools/board_check.py" --all "$HERE/episodes/queue" --no-brief > "$STUDIO/projects/_board.txt" 2>&1 \
  && python3 "$HERE/tools/board_check.py" "$HERE/episodes/queue/01-pepsi-jet-p1" --strict --no-brief > /dev/null 2>&1 \
  && echo "ok   board_check $(tail -1 "$STUDIO/projects/_board.txt")" || { echo "FAIL board_check (queue boards or the pilot's assets)"; tail -3 "$STUDIO/projects/_board.txt"; fail=1; }
rm -f "$STUDIO/projects/_board.txt"
for eng in kokoro chatterbox; do
  rm -f "$P"/work/*
  (cd "$P" && ENGINE=$eng python3 scripts/make_vo.py > work/make_vo.log 2>&1) || { echo "FAIL $eng: make_vo.py crashed"; tail -5 "$P/work/make_vo.log"; fail=1; continue; }
  if [ $eng = kokoro ]; then grep -q "prosody gate" "$P/work/make_vo.log" || { echo "FAIL kokoro: prosody gate (PGATE) did not run"; fail=1; }; grep "prosody gate" "$P/work/make_vo.log"; fi
  if [ $eng = chatterbox ]; then grep -q "ending moves" "$P/work/make_vo.log" || { echo "FAIL chatterbox: end_contour (ENDS) did not run"; fail=1; }; grep "ending moves" "$P/work/make_vo.log"; fi
  for f in vo.wav align.json; do [ -s "$P/work/$f" ] || { echo "FAIL $eng: missing $f"; fail=1; }; done
  if [ $eng = kokoro ]; then  # mix word guard + mix_check on the real VO over a loud synthetic bed (music-like tones + SFX clicks)
    python3 - "$P" "$HERE/lib" <<'EOF' && python3 "$HERE/tools/mix_check.py" "$P" > "$P/work/mix_check.txt" 2>&1 && python3 - "$P" <<'EOF2' || { echo "FAIL mix guard / mix_check"; fail=1; }
import sys, numpy as np, soundfile as sf; sys.path.insert(0, sys.argv[2]); import bed_carve
P = sys.argv[1]; v, sr = sf.read(f"{P}/work/vo.wav", dtype="float32"); v = v if v.ndim == 1 else v.mean(1); n = len(v); t = np.arange(n) / sr
bed = 0.012 * (np.sin(2 * np.pi * 220 * t) + np.sin(2 * np.pi * 1760 * t) + np.sin(2 * np.pi * 3300 * t))
for k in range(0, n, sr // 2): bed[k:k + 2400] += 0.06 * np.random.default_rng(k).standard_normal(min(2400, n - k))
bed = np.stack([bed, bed], 1).astype(np.float32)
g = bed_carve.guard(bed_carve.carve(bed, v), v)
sf.write(f"{P}/work/stem_vo.wav", v, sr, subtype="FLOAT"); sf.write(f"{P}/work/stem_bed.wav", g, sr, subtype="FLOAT")
EOF
import json, sys; r = json.load(open(f"{sys.argv[1]}/work/mix_check.json"))
ok = r["ld_m_p5"] >= 9.0; print(("ok  " if ok else "FAIL"), "mix guard: momentary LD p5", r["ld_m_p5"], "ESTOI phone", r["estoi"]); sys.exit(0 if ok else 1)
EOF2
  fi
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
