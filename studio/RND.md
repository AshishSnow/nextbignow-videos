# R&D — how the studio gets better between videos

A separate scheduled R&D run (no posting) improves the studio one focus area at a time. The video runs read
`PLAYBOOK.md`/`VOICE.md`; this file holds the rules, the rotation, the backlog and the log of experiments.

## Rules
1. One focus area per run. Pick the one with the oldest "last worked" date, unless something is broken or the data
   clearly says otherwise. **Voice has priority until the narrator clearly meets `VOICE.md`'s spec.**
2. Write the hypothesis before building. Research first (primary sources, dated), then experiment in
   `$STUDIO/projects/lab_<date>`; measure before and after **on the same material** (≥ 2 different scripts for voice).
3. Keep only what measures better, or equal and simpler. Template changes must pass `bash studio/tools/smoke_test.sh`.
   Reusable code → `template/` or `lib/`; rules → `PLAYBOOK.md`/`VOICE.md`; numbers → the log below; anything not
   adopted → `studio/lab/<topic>/` with notes.
4. Never post, never touch Metricool beyond read-only analytics, never touch other brands or `fnh-engine/`, only change
   `studio/`. No MP4s or big media in git (narrator reference clips < 1 MB in `studio/voices/` only).
   Open-weight, commercial-use models only; never clone a real person; never ElevenLabs.
5. Every run also: refresh `PERFORMANCE.md` (Metricool, last 21 days); if `ALGORITHM.md` is > 3 days old, research it; if
   `topic_bank.md` has fewer than 10 Ready topics, add verified ones first (owner, 27 Oct: "topics need to improve — something interesting").
   Voice has had 3 runs in a row — give the other areas (Topics, Story, Visuals, Sound) their turn unless voice is broken.
6. Finish within 2 h; don't push template changes near video runs (:05 past 00, 05, 10, 15, 20 UTC).

## Focus rotation
| Area | What it covers | Last worked |
|---|---|---|
| Voice | engine, narrator reference, prosody, pace, post chain | 2026-10-27 (3×) |
| Sound | music score, SFX, mix levels, loudness | never |
| Visuals | props, sets, mascot acting, transitions, safe zones, frame 1 | never |
| Story | hooks, re-hooks, structure, endings/takeaways, length | never |
| Tooling | render speed, smoke tests, QA automation | never |
| Analytics | what the numbers say, cover frames, captions, posting times | never (refreshed every run; YouTube numbers flowing since 27 Oct) |
| Topics | keep `topic_bank.md` interesting and verified: research what makes business stories fascinating, verify 3–5 new topics per run (primary sources), score them with PLAYBOOK §2's interest test, retire weak ones | 2026-10-27 |

## Backlog (add ideas, strike when done)
Voice
- ~~Kokoro weak lines~~ — done 27 Oct run 3: they come from our PSOLA; per-line prosody gate (`PGATE` 0.15, template) → worst line 3.98/4.05 → 4.25.
- Chain drops on short lines: airline a3 raw 4.263 → +EQ 4.259 → +voice_clean 4.217 → +room 4.149; t3 4.327 → 4.263 at voice_clean
  (de-ess cut up to −10.8 dB). EQ is neutral → A/B a lighter de-esser and a drier room (−24 dB vs −21) per line on 3 scripts.
- ~~Chatterbox hybrid: last-word pitch move on low lines~~ — done 27 Oct run 2: `lib/end_contour.py`, low_fall −1.3 → −4.0 (gas), −1.0 → −3.5 (Costco) at ≤ 0.01 per-line UTMOS.
- Chatterbox retakes for *weak* lines too (per-line UTMOS < 4.3, e.g. Duolingo a2 = 3.91 with uptalk): extend `lab/voice_engine/take_picker.py`
  (sampled takes) to also pick by per-line UTMOS and low_fall, then run end_contour on the winner; punctuation variants as a fallback.
- Second scorer that hears intonation: UTMOSv2 or Audiobox-Aesthetics CE/PQ (arXiv 2608.09930) — licence, onnx, RAM on 2 CPUs.
- Shorter hook questions that actually rise (q_rise currently negative on long hooks, both engines; PSOLA rises on Chatterbox made it worse, 27 Oct).
- Second synthetic reference with more smile/energy; paralinguistic `[chuckle]` at one funny line.
- ~~Expressiveness metric: per-line final rise/fall~~ — done 27 Oct (`q_rise_st`, `low_fall_st` in tts_bakeoff.py).
- Magpie TTS (NVIDIA Open Model License) if it can run without torch.
- Ming-3.0-tts-0.5B (MIT; top open-licence arena score; free-text delivery instructions) — first CPU test. NeuTTS **Air** (Apache) as a
  CPU fallback (not 2E/Nano: revenue-capped licence).
- Misread lines with Chatterbox: instead of rephrasing, sample 2 extra takes (temp ~0.7) and keep the one that reads back exactly —
  code ready in `lab/voice_engine/take_picker.py` (ASR exactness first, then UTMOS).
Sound
- A/B music bed level vs avg watch; sidechain ducking depth; SFX density per 10 s.
Analytics
- YouTube vs Instagram per topic: YT winners differ (Compaq 1,332 YT vs 130 IG) — pull YTVP06/08 every run and compare after 10 posts.
Visuals / Story / Tooling
- First-frame test sheet: render frame 0 of the last 5 videos side by side with safe-zone guides.
- Smoke test that renders 2 s of video (not only VO) to catch empty-frame regressions.

## Log
- 2026-10-27 | Voice | Hypothesis: an LLM-style open TTS (Chatterbox-Turbo, MIT) conditioned on our own synthetic narrator gives more
  natural delivery than Kokoro + PSOLA, at ≥ equal intelligibility and acceptable CPU cost. Built `tools/tts_bakeoff.py`
  (engine A/B with whole + per-line UTMOS, range, wpm, ASR, RTF) and `lib/cb_turbo.py`. Results (Kokoro shipped → Chatterbox q4
  slow-ref shipped, UTMOS whole/per-line): gas i1–b2 4.474/4.43 → 4.544/4.494; gas b3–e2 4.257/4.38 → 4.336/4.459; more rows below.
  Range 18.1–18.3 → 17.0–17.2 st (still ≥ 15), ASR 0 bad lines on both. q8 LM RTF 12.7 → q4 LM RTF 1.8 at equal score.
  Reference sets pace: flat ref 186 wpm/13.2 st, slow PSOLA ref 165 wpm/16.4 st. → see "Decision" line below.
  Duolingo 91 s 4.375/4.424 → 4.519/4.484; Costco 83 s 4.340/4.405 → 4.471/4.468. New line-end metric: Chatterbox's reveal
  lines fall only −0.2…−2.5 st vs Kokoro+PSOLA −4.2…−7.2 st; PSOLA on top of Chatterbox costs −0.23 UTMOS.
  **Decision: not adopted as default** (gains are acoustic; it loses the landed endings our format needs). Kept as opt-in
  `ENGINE=chatterbox` in make_vo.py (+ `PROSODY` switch), lib/cb_turbo.py, voices/narrator_slow.*, setup downloads (q4).
  Smoke test (new tools/smoke_test.sh) passed on both engines. Next voice run: hybrid endings (see VOICE.md "Next").
- 2026-10-27 | Voice (interactive session with the owner, in parallel with the R&D run) | Deep research → narrator spec with sources
  (VOICE.md "Research basis"); 16-variant Kokoro lab (26 Oct: no global pitch lift, SPD .88/PZ 1.6 → the current default);
  Chatterbox fp32/q8 bake-off with 5 references; Qwen3-TTS 0.6B as engine (3.95) and 1.7B VoiceDesign as reference maker (too
  high-pitched); **hybrid lead:** Chatterbox with a *flat* Kokoro reference (`voices/narrator_flat_ref24k.wav`) + half-strength
  PSOLA cost only −0.005 UTMOS (4.471 → 4.466) and raised range 13.6 → 16.2 st on the Starbucks script (full PSOLA: −0.10);
  line-end melody (main's scorer, Starbucks script): Kokoro main default 4.345 / low_fall −4.3 / q_rise +0.9 / 18.2 st;
  Chatterbox flat ref 4.471 / −0.6 / −1.3 / 13.6 st; + half PSOLA 4.466 / **−0.2** / −1.2 / 16.2 st; + full PSOLA 4.368 / −0.2 / 19.2 st;
  best-of-3 takes 4.478 / +0.1. → **Half/full-strength PSOLA adds range but does NOT land the endings** (Chatterbox's last words
  resist the generic ending curve). Confirms the R&D decision: Kokoro stays default. Endings need a targeted last-word move
  (bigger, on the final stressed syllable only) or a reference whose sentences end low. | confirms Kokoro default; lead for hybrid
- 2026-10-27 (run 2) | Voice | Hypothesis: moving pitch only on the last word of `low` lines in a Chatterbox take (PSOLA on that slice,
  cross-faded in) lands reveal lines at ≤ −4 st without global PSOLA's −0.23 UTMOS. 6 versions on gas/Costco/Duolingo (lab/voice_endings/).
  Final (−4 st, start ≥ 0.5 s before last voiced frame, cap uptalk at line median, floor 85 Hz, per-line UTMOS gate 0.05):
  gas low_fall −1.3 → **−4.0**, UTMOS 4.522/4.480 → 4.513/4.476; Costco −1.0 → **−3.5**, per-line 4.474 → 4.468 (whole 4.501 → 4.380,
  whole-file score noise — per-line min 4.43 → 4.41); Duolingo −0.2 → −1.7 (moved lines −2…−3.5 each; its a2 line is a 3.91 uptalk
  line the gate skipped). Kokoro shipped on the same scripts: 4.317/4.399, 4.321/4.402, 4.382/4.428; low_fall −4.8/−4.9/−7.1.
  Question rises (+3…+4.5 st) on Chatterbox: q_rise worse (−1.8 → −2.1) → off. **Decision:** endings ON by default inside
  `ENGINE=chatterbox` (`ENDS=0` to disable); Kokoro stays the default engine (Chatterbox still: falling questions, one weak line on
  Duolingo). Also: ASR scorer now reads "$1.50" == "a dollar fifty" (Costco's 2 false "bad lines"); smoke test exercises a low line.
  Analytics: Metricool IG reel stats frozen since ~26 Oct evening IST (identical 3 pulls); YouTube numbers arrive for the first time.
- 2026-10-27 (run 3) | Voice | Hypothesis: Kokoro's weak lines (worst 3.98 gas, 4.05 airline) can be lifted to ≥ 4.2 without losing melody.
  Diagnosis first: flat Kokoro lines all score 4.43–4.52; our PSOLA prosody makes the weak ones (gas c1 4.45 → 3.93) → the planned
  Kokoro retakes were dropped unbuilt. Built a per-line prosody gate (re-render a line at 0.6/0.3 strength if PSOLA costs it > 0.15).
  Same 3 scripts, shipped chain, UTMOS whole / per-line (min): gas 4.234/4.379 (3.98) → 4.373/4.411 (4.25), range 18.1 → 17.8;
  Duolingo 4.386/4.423 (4.37) → 4.421/4.421 (4.33), 18.4 → 18.3; airline 4.394/4.390 (4.05) → 4.402/4.406 (4.25), 18.4 → 18.2;
  low_fall unchanged (−4.8/−6.6/−5.0), ASR 0 bad lines. Not adopted: global clip −7/+8 st (range 15.0), puck .1 blend default (equal).
  **Decision: `PGATE=0.15` is the template default** (`PGATE=0` disables); smoke test checks it runs; passed. lab/voice_gate/.
  Analytics: Metricool Instagram reel stats identical for the 5th pull (frozen since 26 Oct); YouTube still updates.
