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
- ~~A/B the Kokoro blend and pitch target~~ — done 26 Oct (new default blend, no pitch lift). Next: try am_puck mixes in a real video, per-sentence generation inside long lines, and a light de-esser.
- Whisper-quiet "secret" lines and louder reveal lines (volume automation per line in mix.py).
- Breath/room tone between lines so it doesn't sound stitched; tiny 40–80 ms crossfades.
- Emphasis words get +1–2 dB and a slight stretch, not only pitch.
- Try a short laugh/"huh" interjection as a sound effect (not TTS) at a funny moment.

Visual / story
- First frame = the most surprising visual of the whole video (no build-up), with the hook caption already on screen.
- Mid-video re-hook card ("and the third trick is the sneakiest") around 45–55% of the runtime.
- Loop ending: last line leads back into the first frame.
- New set designs: split screen, map, receipts, factory line, courtroom, vault, game board, timeline.
- Character acting: mascot reacts (shocked, smug, counting money) on every reveal.
- Number reveals with physical objects (stacks of cash, piles of cups) instead of text.
- Custom cover frame (`videoCoverMilliseconds`) chosen deliberately: hook question + key object.

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
Lessons: (1) never shift the whole voice up — use the blend for brightness instead; (2) slower + longer pauses helps;
(3) more am_fenrir lowers naturalness; (4) wider per-line range costs only ~0.03.

## Log
- 2026-10-26 | system | Voice lab, 16 variants on the Starbucks script, scored with UTMOS + ASR + pitch range (table above) | new default: michael/eric/fenrir blend, own register, SPD .88, PZ 1.6, EXS 1.0 — UTMOS 4.12 → 4.36, 214 → 183 wpm | kept
- 2026-10-26 | system | voice_report.py: UTMOS now runs on onnxruntime (model on the `models` branch, no torch), ASR check ignores number/abbreviation formatting | kept
