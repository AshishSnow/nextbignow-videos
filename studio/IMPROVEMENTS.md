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
- am_puck 0.1 brighter blend (michael .45 / eric .3 / fenrir .15 / puck .1) — 27 Oct airline script: UTMOS 4.395 → 4.409, per-line 4.39 → 4.41, **worst line 4.07 → 4.17**, range 18.4 → 17.9 st, low endings −5.4 → −5.1 st → used for this video; R&D should confirm on a 2nd script before it becomes the template default. R&D run 3 (27 Oct, with the prosody gate): per-line mean equal to the default on gas/Duolingo/airline (±0.005) → stays a per-video option, not the default.
- ~~Light de-esser / chain drop on short lines~~ — done 27 Oct (De Beers): chain-only A/B on one fixed raw take → de-ess −8, room −27 dB, compressor 1.5:1 = per-line 4.396 → 4.425, worst 3.996 → 4.063; template default. R&D: confirm on gas + airline scripts.
- Next: per-word emphasis loudness (+1–2 dB) A/B.
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
- Number reveals with physical objects (stacks of cash, piles of cups) instead of text. 27 Oct De Beers: icon arrays (10 brides, 1 → 8 lit), a mine cart of gems, a cracking gem — keep going.
- Typewriter-in-sync typography (the key quote typed word by word as the VO says it) — first used 27 Oct (De Beers); reuse for any famous slogan/quote.
- Test a 2-minute explainer vs the 75–100 s ones on avg view % (De Beers is 117.7 s with re-hooks at ~10, 31, 58 and 71 s).
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
- 2026-10-27 | R&D (no video) | Voice engine bake-off: Chatterbox-Turbo q4 (MIT) in our synthetic narrator's voice vs Kokoro+PSOLA on 4 scripts → UTMOS +0.06 per line, but reveal endings fall only −0.2…−2.5 st vs −4…−7 st → Kokoro stays default, `ENGINE=chatterbox` opt-in. Details: RND.md, VOICE.md. | kept (opt-in)
- 2026-10-27 | R&D run 2 (no video) | Hybrid endings for Chatterbox (`lib/end_contour.py`): reveal lines now land −3.5…−4.0 st (was −1.0…−1.3) at ≤ 0.01 per-line UTMOS; on by default under `ENGINE=chatterbox`; Kokoro stays default. YouTube analytics now available (PERFORMANCE.md). Details: RND.md, VOICE.md. | kept (opt-in engine)
- 2026-10-27 | Airline miles: why Amex paid Delta $8.2B (100.9 s, 30 shots) | Data: first YouTube numbers (number/tension titles 740–1,360 views vs flat autopilot titles 41–326) → YouTube title now carries the number ('Airline Miles: Why Amex Paid Delta $8.2B'); Instagram stats frozen since 26 Oct. Voice: am_puck 0.1 blend A/B vs default on this script — UTMOS 4.395 → 4.409, worst line 4.07 → 4.17, range 18.4 → 17.9 st, 169 → 170.5 wpm, low_fall −5.4 → −5.1 st, ASR 0 bad lines both → kept for this video (not yet template default); wh-question hook left to fall naturally (ending None); voice_report/tts_bakeoff ASR normaliser now reads years ('twenty twenty') and 'ten and a half' (were false ASR bad lines). Final VO: UTMOS 4.409, F0 137 Hz, 17.9 st, 170.5 wpm speaking, 0 ASR bad lines. Visual/story: frame 1 = card pumping cash into a jet with the '$8 BILLION?' question on screen and the loop-back on 'the card in your wallet'; new prop set (generic jet, rewards card, novelty cheque, balance scale that tips, split-flap departures board re-hook, money-flow map with animated arrows you→bank→airline→miles, mile tokens, chained treasure chest = collateral, value dial, rulebook + 'subject to change' stamp, melting mile coin, earn/use/hoard checklist); 3 re-hooks (18 s, 34 s, 51 s); usable takeaway; bossa-nova/airport-lounge score (new genre) + PA-chime and flap-clatter SFX → kept; generic props + clouds/arrow/dial moved into template anim_props3 (render-tested). QA: 1080x1920 h264/aac, −11.8 LUFS / −1.4 dBTP, VO/bed 15–20 dB. 2 renders (2nd: plane motion in two static shots, digit-only flaps). Fixes caught in test frames: white/yellow captions unreadable on cream, ink bar labels unreadable on emerald/purple, card covering a bar value. Quality bar: hook 5, clarity 5, pacing 4, voice 4, visual 4, audio 4, ending 5. | kept
- 2026-10-27 | R&D run 3 (no video) | Kokoro weak lines traced to our PSOLA (flat lines 4.43–4.52; PSOLA drops some to 3.9) → per-line prosody gate `PGATE=0.15` in template make_vo: worst line 3.98 → 4.25 (gas), 4.05 → 4.25 (airline), Duolingo unchanged, range −0.1…−0.3 st, endings kept. puck .1 blend re-tested on 3 scripts with the gate: equal to default → stays a per-video option. Details: RND.md, VOICE.md, lab/voice_gate/. | kept (template)
- 2026-10-27 | De Beers: diamonds aren't as rare as their price (117.7 s, 34 shots) | Data: 6th identical Metricool pull — Instagram AND now YouTube stats frozen (posts after 26 Oct show PUBLISHED but have no analytics rows) → no new signal; chose an everyday-object, 'that can't be right' topic (insight 1) with a usable takeaway (insight 3); YouTube likes pulled for the first time (YTVP09). Voice: chain-only A/B on one fixed vo_raw (new lab/voice_chain/chain_ab.py, removes PSOLA run noise): de-ess −11→−8, room −21→−27 dB, compressor 2.2→1.5:1 → per-line UTMOS 4.396 → 4.425, worst line 3.996 → 4.063, 6 shortest lines 4.301 → 4.344; stage ablation found the 2.2:1 compressor costs the short line a1 0.14 → kept, template default (DEESS/ROOM_DB/COMP env knobs, voice_clean ratio=). voice_report.py: chunked whole-file UTMOS for VOs > 80 s (117 s was OOM-killed), per-line mean/min/weak lines, q_rise/low_fall; ASR normaliser reads decades ('nineteen eighties'); dropped a real surname from the VO (ASR heard 'Francis Jarity'). Final VO: UTMOS 4.396 (chunked) / per-line 4.426 (min 4.07), F0 137 Hz, 18.2 st, low_fall −6.6 st, 169.8 wpm speaking, 0 ASR bad lines. Visual/story: 'trick in three moves' structure (supply / feeling / price rule) + twist (lab-grown −96%, De Beers' own lab brand shut, core loss, for sale); frame 1 = ring on velvet pillow under a spotlight with a swinging '2 MONTHS' SALARY' tag + question caption, loop ending on the same composition ('…was the story'); new props (cut gem with crack, ring, pillow, hanging tag, bride icon array 1→8 of 10, drawer vault, diamond hourglass, mine cart, vintage serif print ads, typewriter typing the slogan in sync, award medal, animated crashing line chart, lab bell jar, SHUT DOWN sign) → template anim_props3; re-hooks at ~10, 31, 58, 71 s; film-noir heist-jazz score (new genre: walking bass, brushed ride, vibes + celesta glints, muted trumpet) + typewriter/shimmer SFX. QA: 1080x1920 h264/aac, −11.8 LUFS / −1.3 dBTP, VO/bed 15–23 dB. 2 renders (2nd: filled two 2-s waits where the main prop sat empty: pie gems shown before '90%', '?' + gem before the loss bar). Quality bar: hook 5, clarity 5, pacing 4, voice 4, visual 4, audio 4, ending 5. | kept
