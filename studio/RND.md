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
5. Every run also: refresh `PERFORMANCE.md` (Metricool, last 21 days) and, if `ALGORITHM.md` is > 3 days old, research it.
6. Finish within 2 h; don't push template changes near video runs (:05 past 00, 05, 10, 15, 20 UTC).

## Focus rotation
| Area | What it covers | Last worked |
|---|---|---|
| Voice | engine, narrator reference, prosody, pace, post chain | 2026-10-27 |
| Sound | music score, SFX, mix levels, loudness | never |
| Visuals | props, sets, mascot acting, transitions, safe zones, frame 1 | never |
| Story | hooks, re-hooks, structure, endings/takeaways, length | never |
| Tooling | render speed, smoke tests, QA automation | never |
| Analytics | what the numbers say, cover frames, captions, posting times | never (refreshed every run) |

## Backlog (add ideas, strike when done)
Voice
- Chatterbox hybrid: last-word pitch move on q/low lines only (full PSOLA tested: −0.23 UTMOS) — target low_fall ≤ −4 st.
- Shorter hook questions that actually rise (q_rise currently negative on long hooks, both engines).
- Second synthetic reference with more smile/energy; paralinguistic `[chuckle]` at one funny line.
- ~~Expressiveness metric: per-line final rise/fall~~ — done 27 Oct (`q_rise_st`, `low_fall_st` in tts_bakeoff.py).
- Magpie TTS (NVIDIA Open Model License) if it can run without torch.
Sound
- A/B music bed level vs avg watch; sidechain ducking depth; SFX density per 10 s.
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
