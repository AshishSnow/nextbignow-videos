# Get better every video (owner's standing order)

The owner's words: "Don't settle. It takes time, no hurry, but with every video improve: a more natural voice, a better video.
Understand the new algorithm. Do this without being told every time."

## The loop (every run, before building)
1. **Learn from data** — refresh `PERFORMANCE.md` (Metricool analytics). Compare the last 3 posts with the best ones:
   which hooks kept people past 3 s, which held the longest average watch, which got shares/saves. Write 1–3 new insights.
2. **Learn the platforms** — if `ALGORITHM.md` is more than 7 days old, research and update it.
3. **Pick this run's upgrades** — choose at least **one voice/audio upgrade** and **one visual/story upgrade** from the
   backlog below (or a new idea the data suggests). Write them in the run log before building.
4. **Test, don't guess** —
   - Voice changes: render the script with the current defaults *and* with the change, run
     `python3 studio/tools/voice_report.py $P work/vo.wav` on both, and listen to a few lines. Keep the change only if
     UTMOS (naturalness, 1–5) is not lower by more than 0.05, ASR read-back has no new errors, and pitch range stays ≥ 15 st.
   - Visual changes: look at test frames with the safe-zone guides; keep only what reads better on a phone.
5. **Keep what works** — reusable gains go into `template/` (code) and `PLAYBOOK.md` (rules), so the next run starts higher.
6. **Log it** — add one line to the log below: date, video, upgrades tried, measured result, kept or dropped.

## Quality bar (score 1–5 before posting; any score below 4 → fix it first)
| Area | 5 looks like |
|---|---|
| Hook (0–3 s) | First frame already shows the surprising object in motion; the question names the brand and the twist |
| Clarity | A 12-year-old could retell the business secret after one watch |
| Pacing | No line rushed; the picture changes every 2–3 s; a re-hook roughly every 10 s |
| Voice | Natural, warm, energetic, clear highs and lows; no robotic words; every word read back correctly by ASR |
| Visual | Every claim drawn as a prop or diagram; vibrant set; nothing in unsafe zones; one new visual idea vs last video |
| Audio | Voice on top, music lifts reveals, SFX on beats, −11 LUFS / −1 dBTP |
| Ending | Clear payoff + a takeaway worth saving + "send this to the friend who…" |

## Backlog (pick from here; strike through what's done, add new ideas)
Voice / audio
- ~~Slower, calmer pace with longer pauses (owner request)~~ — done 26 Oct: SPD 0.88, PZ 1.6 (214 → 183 wpm).
- ~~A/B the Kokoro blend and pitch target~~ — done 26 Oct (new default blend, no pitch lift).
- ~~Per-sentence generation inside long lines~~ — done 27 Oct: `SPLIT=0.12` → UTMOS 4.23 → 4.38, range 17.7 → 18.5 st; now default.
- ~~am_puck mix in a real video~~ — 27 Oct: puck .3/michael .4/eric .3 + SPLIT = 4.42 UTMOS but narrower (16.5 st), slower (169 wpm), +3 s; within noise of the default → not adopted. Re-test on a shorter script.
- ~~Sentence-gap 0.08 vs 0.18~~ — 27 Oct gas-station script: SPLIT 0.08 / 0.12 / 0.18 = UTMOS 4.30 / 4.30 / 4.31 → gap length doesn't matter; keep 0.12, stop testing it.
- Next: a light de-esser pass check; per-word emphasis loudness (+1–2 dB) A/B; a slightly brighter blend via am_puck 0.1 on a ~75 s script.
- ~~Whisper-quiet "secret" lines and louder reveal lines~~ — done 27 Oct: `LINE_DB` per-line dB in mix.py (now in template).
- ~~Room tone between lines~~ — 27 Oct: −58 dB band-limited room tone, UTMOS 4.30 → 4.29 (within noise) → kept at −60 dB in mix (template). Still to try: real breath samples before long lines.
- Emphasis words get +1–2 dB and a slight stretch, not only pitch.
- Try a short laugh/"huh" interjection as a sound effect (not TTS) at a funny moment.

Visual / story
- First frame = the most surprising visual of the whole video (no build-up), with the hook caption already on screen.
- ~~Mid-video re-hook card~~ — done 27 Oct (envelope "wait for this number" at 47%); keep doing it, vary the prop.
- ~~Loop ending~~ — done 27 Oct: last line "…a snack shop with a giant price sign" lands on the exact frame-1 composition. Keep doing it.
- New set designs: split screen, map, receipts, factory line, courtroom, vault, game board, timeline.
- Character acting: mascot reacts (shocked, smug, counting money) on every reveal.
- Number reveals with physical objects (stacks of cash, piles of cups) instead of text.
- Custom cover frame (`videoCoverMilliseconds`) chosen deliberately: hook question + key object.
- Keep the video near 60–75 s: Duolingo 93 s → gas station 80.6 s (first draft was 87 s, trimmed 4 lines). Compare avg watch % of length next run.
- Takeaway the viewer can *use* in their own life (habit tip, money tip) — test whether it lifts saves/shares (still ~0).

## Voice benchmarks (same Starbucks test script unless noted; UTMOS 1–5, higher = more natural)
| Setting | UTMOS | F0 median | Pitch range | Speaking pace | Pauses | Note |
|---|---|---|---|---|---|---|
| Restaurant video voice (michael/onyx/fenrir/echo blend, speed ~0.94, no pitch shift) — its own script | 4.45 | 117 Hz | 15.9 st | 165 wpm | 10% | best-retaining video so far (67.6% past 3 s, 25 s avg watch) |
| Energetic default until 26 Oct (EW .75, GT 165, EXS .5, BMP .8, SPD 1.0) | 4.12 | 173 Hz | 18.1 st | 214 wpm | 8% | too fast |
| SPD .95 | 4.18 | 173 | 18.3 | 208 | 8% | |
| EW 1.0 GT 160 | 4.15 | 168 | 17.4 | 209 | 8% | |
| EW 1.0 GT 160 EXS .3 BMP .6 | 4.22 | 167 | 16.1 | 209 | 8% | |
| EW .75 GT 158 EXS .4 BMP .7 SPD .95 ("mid") | 4.28 | 166 | 17.5 | 208 | 8% | best of round 1 |
| EW .5 GT 160 | 3.82 | 168 | 18.0 | 204 | 8% | more fenrir = worse |
| Round 2–3 (all: SPD .88, PZ 1.6, PMIN .3) | | | | | | |
| eric/fenrir, own register (GT 0) | 4.20 | 158 | 19.8 | 200 | 11% | |
| eric/fenrir, GT 165 | 4.04 | 173 | 18.2 | 200 | 11% | pitch lift costs naturalness |
| restaurant blend, own register | 4.43 | 116 | 15.8 | 173 | 10% | most natural, but deep/older |
| restaurant blend, GT 135 | 4.11 | 142 | 15.3 | 173 | 10% | lift costs 0.3 |
| michael .5 / eric .3 / fenrir .2, own register, EXS .8 BMP .8 | 4.40 | 136 | 16.4 | 183 | 10% | |
| same, GT 145 | 4.14 | 152 | 16.6 | 183 | 10% | lift costs 0.26 |
| **same, EXS 1.0 BMP 1.0 → new default** | **4.37** | **137** | **17.7** | **183** | **10%** | young, warm, natural, more highs/lows |
| puck .4 / eric .4 / michael .2, own register | 4.37 | 134 | 17.5 | 182 | 10% | good alternative |
| same, EXS 1.0 BMP 1.0 | 4.34 | 136 | 18.3 | 182 | 10% | |
| puck .3 / michael .4 / eric .3, EXS .9 | 4.39 | 131 | 16.7 | 179 | 10% | good alternative |
| **Duolingo script, 27 Oct: default (A)** | 4.23 | 137 | 17.7 | 180 | 9% | 89 s |
| **A + SPLIT 0.12 (B) → new default** | **4.38** | 139 | **18.5** | 176 | 9% | 91 s |
| puck .3/michael .4/eric .3, EXS .9 (C) | 4.31 | 131 | 16.7 | 175 | 9% | 91 s |
| C + SPLIT 0.12 (D) | 4.42 | 133 | 16.5 | 169 | 9% | 94 s, flatter |
Lessons: (1) never shift the whole voice up — use the blend for brightness instead; (2) slower + longer pauses helps;
(3) more am_fenrir lowers naturalness; (4) wider per-line range costs only ~0.03.

## Log
- 2026-10-26 | system | Voice lab, 16 variants on the Starbucks script, scored with UTMOS + ASR + pitch range (table above) | new default: michael/eric/fenrir blend, own register, SPD .88, PZ 1.6, EXS 1.0 — UTMOS 4.12 → 4.36, 214 → 183 wpm | kept
- 2026-10-26 | system | voice_report.py: UTMOS now runs on onnxruntime (model on the `models` branch, no torch), ASR check ignores number/abbreviation formatting | kept
- 2026-10-27 | Duolingo streak (93 s, 21 shots) | Voice: per-sentence Kokoro generation (SPLIT 0.12) A/B vs default and vs puck blend — UTMOS 4.23 → 4.38, range 17.7 → 18.5 st, 176 wpm, ASR 0 bad lines → kept, now template default; puck+SPLIT 4.42 but flatter/slower → not adopted. Visual/story: mid-video re-hook prop (envelope 'wait for this number' at 47%), first frame = hook object + caption fully on screen, split-screen day 2 vs day 200, year heatmap, ECG revive, habit-loop diagram, takeaway the viewer can use (survive 7 days), chiptune score (new genre) → kept. Generic data-viz props (odometer, cents_grid, bars, loop_diagram, heatmap, heart_line) moved into template anim_props3. QA: 1080x1920, -11.5 LUFS / -1.3 dBTP, VO/bed 17–25 dB. Quality bar: hook 4, clarity 5, pacing 4, voice 4, visual 4, audio 4, ending 4. Lessons: shot 0 must contain the money reveal (first cut came before 'billion' — caught in test frames); tiny flame icons (<60 px) lose their fill → draw icons ≥ 60 px; 2 renders + 1 half re-render. | kept
- 2026-10-27 | Gas stations barely make money on gas (80.6 s, 20 shots) | Voice: sentence-gap A/B (SPLIT .08/.12/.18 → UTMOS 4.30/4.30/4.31, all 18.1–18.3 st, 0 ASR bad lines) → no effect, kept .12; room tone −58 dB → 4.29 (−0.01) → kept at −60 dB in the mix; per-line level automation (secret line −2.5 dB, reveals +1 dB) → kept, template. Final VO: UTMOS 4.30, 18.2 st, 170 wpm speaking, 0 ASR bad lines. Visual/story: everyday-object hook (pump + price sign in frame 1, caption on screen), loop ending back to frame 1, new forecourt prop set (pylon price sign, pump, car, store facade, pizza, fountain cup, receipt), coin-pie scoreboard (14¢ / 42¢ / 59¢), 100% stacked bars (sales vs profit), curtain re-hook, top-down store floor-plan path, usable takeaway (pay at the pump), surf-rock score (new genre) → kept; generic props moved to template anim_props3. QA: 1080x1920 h264/aac, −11.7 LUFS / −1.4 dBTP, VO/bed 14–20 dB. 1 full render + 1 half re-render (empty frames at 18 s and 29–31 s fixed by showing icons/empty coin first). Quality bar: hook 5, clarity 5, pacing 4, voice 4, visual 4, audio 4, ending 5. Lessons: tall props must start below y≈620 (caption zone); never leave a 2–3 s stretch where the main prop waits for its number — show it empty first, fill it on the word. | kept
