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
     UTMOS (naturalness, 1–5) is not lower by more than 0.05, ASR read-back has no new errors, and pitch range stays ≥ 10 st.
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
- Slower, calmer pace with longer pauses before reveals (owner request; restaurant video held best) — tune `SPD` and per-line pauses.
- A/B the Kokoro blend (am_eric/am_fenrir weights) and pitch target against UTMOS each time a new idea comes up.
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

## Log
- 2026-10-26 | system | Voice lab A/B grid (speed, blend, pitch target, range) on a test script, scored with UTMOS + ASR + pitch range → see below | defaults updated in template/make_vo.py
