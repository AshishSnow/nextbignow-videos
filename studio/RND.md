# R&D — how the studio gets better between videos

A separate scheduled R&D run (no posting) improves the studio one focus area at a time. The video runs read
`PLAYBOOK.md`/`VOICE.md`; this file holds the rules, the rotation, the backlog and the log of experiments.

## Rules
0. **Writers' room first (since 31 Oct, STORY.md §8):** if `episodes/queue/` holds fewer than 3 REVIEWED episodes, this run writes
   1–2 complete episodes (vo_lines.py + shots.md + SOURCES, story_check 7/7 + all S-gates, a fresh-eyes subagent review) and marks
   them REVIEWED in `episodes/README.md`. Only when the queue is full does the rotation below apply. Runs: 02:41, 08:41, 12:41 UTC.
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
6. Finish within 2 h; don't push template changes near episode runs (16:05 and 21:05 UTC).

## Focus rotation
| Area | What it covers | Last worked |
|---|---|---|
| Voice | engine, narrator reference, prosody, pace, post chain | 2026-10-27 (3×) |
| Sound | music score, SFX, mix levels, loudness | 2026-10-27 (run 6: word guard + `tools/mix_check.py`) |
| Visuals | props, sets, mascot acting, transitions, safe zones, frame 1 | 2026-10-28 (run 7: `tools/layout_check.py`, safe-area captions) |
| Story | hooks, re-hooks, structure, endings/takeaways, length | 2026-10-27 (`tools/story_check.py`, roadmap rule R8) |
| Tooling | render speed, smoke tests, QA automation | never (run 7 added a video path to smoke_test.sh as a side task) |
| Analytics | what the numbers say, cover frames, captions, posting times | never (refreshed every run; YouTube numbers flowing since 27 Oct) |
| Writers' room | episode scripts + storyboards + sources in `episodes/queue/` (default job — rule 0) | 2026-10-31 (interactive: pilot YOUR MOVE EP 1, Parts 1–2) |
| Brand | BRAND.md readiness: media-kit numbers, brand-safety rules, sponsor formats, disclosure templates, community | 2026-10-31 (interactive: BRAND.md) |
| Topics | keep `topic_bank.md` interesting and verified: research what makes business stories fascinating, verify 3–5 new topics per run (primary sources), score them with PLAYBOOK §2's interest test, retire weak ones | 2026-10-27 (R&D run 4: +7 → 23 Ready) |

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
- A/B music bed level vs avg watch; ~~sidechain ducking depth~~ (done 27 Oct run 6: word guard); SFX density per 10 s.
- **Mastering (found 27 Oct run 6): ffmpeg loudnorm never runs linear on our mixes** — pre-master PLR is 15–19 dB (printer −16.3 LUFS /
  −1.0 dBTP, gas −17.1/−0.3, Hoover −19.5/−1.0) but −11 LUFS at −1.5 dBTP needs ≤ 9.5 dB, so loudnorm falls back to *dynamic* mode
  (LRA squashed to ~2 LU; even a −14 target stays dynamic). A plain 4×-oversampled look-ahead limiter in front did not fix it (6 dB GR
  on 25 % of samples, still dynamic). Next: an explicit chain — gentle bus compressor (2:1, slow) + true-peak limiter with ≤ 3 dB GR,
  then a *linear* gain to −11 — and measure pumping (short-term loudness variance in gaps), LRA, phone ESTOI and UTMOS of the voice
  stem through the master gain curve, vs today. YouTube turns anything above −14 LUFS down (Wikipedia/YouTube −14 reference), so the
  extra 3 dB only matters on Instagram, whose normalisation is undocumented — keep −11 until measured.
- Phone-speaker check of SFX *audibility*: guard keeps words clear, but are SFX in the gaps still heard on a phone (most SFX
  energy below 300 Hz in boom/thud)? Measure phone-band SFX level vs bed; brighten booms with a 1–3 kHz click layer if needed.
Analytics
- YouTube vs Instagram per topic: YT winners differ (Compaq 1,332 YT vs 130 IG) — pull YTVP06/08 every run and compare after 10 posts.
Story
- Validate R8 (roadmap) when Metricool rows return: tag roadmap yes/no per post, `python3 lab/story/corr.py` at n ≥ 10 (PERFORMANCE K).
- Real reversal detection for story_check (good/bad polarity per line, e.g. a small lexicon or hand tags) — keyword "but" counts
  did not track retention.
- Comment test: one specific A/B question in the last line vs the friend CTA (comments ~0; owner's references 75–300 per reel).
Visuals / Story / Tooling
- ~~Cinematic texture~~ — done 27 Oct (interactive): `template/scripts/anim_cine.py` (lit worlds with depth, glow disc, 3D titles behind the
  hero, light rays, bokeh, DOF, film grade), default on. Next: prop **materials** (specular highlights, subtle texture on paper/metal/
  wood props, soft contact shadows everywhere), and speed (grade now ~0.22 s/frame after the 27 Oct cleanup; next: fuse the tone curve into a LUT).
- ~~Mascot upgrade~~ — done 27 Oct; ~~full-frame scenes + lit cast~~ — done 27 Oct evening (interactive, owner's references:
  "full frame… colours, more natural and 3D, change the style of clothes"): `anim_mascot3d.py` is now a lit 2.5D renderer
  (per-part normals from distance fields, key/ambient/rim light presets, contact occlusion, cast shadows), 10 looks with real
  clothes; `anim_sets.py` = full-frame sets (street/study/parlor/office/store/dusk), camera framing, foreground hand, smoke/embers/
  eyes, captions, part badge, HUD (clock, rule pill, timer, audience choice). Next: walk/run cycles with arm swing, sitting at
  a desk, 3/4 head turns, hands that grip props, more sets per topic (factory, bank, kitchen, night city), and a hair/fabric
  texture pass. Measure: does avg watch % rise on scene-heavy videos vs the disc style (compare from the next 5 posts).
- Story format from the owner's references (27 Oct): multi-part series ("Part 3") and audience choices ("comment A or B — you pick
  what happens next") get 75–300 comments per reel vs our ~0 — test a two-part story with a choice CTA and compare comments/shares.
- Photoreal background plates from a local open image model (owner's reference reels use realistic AI imagery): check licence
  (commercial use) + CPU speed at 1080×1920 on 2 cores; only for backgrounds behind our own mascot/props; label AI as we do now.
- ~~First-frame test sheet~~ — done 28 Oct run 7 (first 3 s of the 14 posted MP4s, `lab/visuals/`; no feature predicts the 3-s rate, n = 9).
- ~~Smoke test that renders video~~ — done 28 Oct run 7 (layout_check + 1 s anim.py encode of the Hoover shots).
- Props/labels that draw their own text (map pins, price signs, source chips placed by hand at y > 1465) are not nudged by the safe area:
  banana's chips still touch the bottom zone by ≤ 9 px; an optional `layout_check --strict` could flag prop text too (OCR-free: render
  with props on/off is not possible generically — needs per-prop text tagging).
- Retention per shot type: once Metricool returns per-second retention (not available now), compare scene vs disc shots.
- `_CINE_T` (window twinkle time) is set by the *previous* frame's finish() — harmless off-by-one in sequential renders, but parallel
  part renders start each part with t = 0 for the first frame's windows; set it at the top of compose() if a flicker is ever seen.

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
- 2026-10-27 | Topics (interactive session; owner: "topics need to improve — something interesting") | Hypothesis: 12 videos in a row
  used one formula ("how company X really makes money"); fresh story types (wild true stories, everyday-object economics, hidden giants,
  origin twists) will hold attention and get shared more. Built the interest test + type mix (PLAYBOOK §2) and `topic_bank.md`;
  3 research agents verified 15 candidates against primary sources (court opinions, SEC/DOJ/Mint/FAO documents, company reports) →
  16 Ready entries scored 26–32/35, with myths flagged (Pepsi jet price, Hoover "£100m", Nintendo love hotels, Kodak "hid it",
  "80% of eyewear", banana "extinction"). Hoover needs one more major outlet for the £48m before use. | kept — measure 3-s rate,
  avg watch, shares and saves by type in PERFORMANCE.md after ~5 new-type videos
- 2026-10-27 (run 4) | Topics | Trigger: topic_bank.md had **0 Ready** topics (rule 5) and the owner asked for more interesting topics.
  Hypothesis: non-F types (B everyday object, E trick, A wild story, C hidden giant, D origin twist) can be verified to primary-source
  standard and score ≥ 26/35 on the §2 interest test, giving the video runs a 2-day queue that never repeats a type. Method: 4 parallel
  research passes (12 candidates, primary sources: court opinions, DOJ, US Mint/Treasury, peer-reviewed papers, SEC, official
  histories), myth hunt per topic, my own spot-checks (Pepsi opinion jet cost: UW copy "$23 million", another copy summarised as $28M →
  VO says "over twenty million"; Common Cents Act dates conflict → "passed Congress in 2026"). **Result: 11 verified (27–30/35, all
  verifiable = 5 when limited to the listed numbers), 1 near-ready (Hoover), 2 dropped as myths/thin (Pepsi Soviet navy, hot dogs
  10 vs 8).** The interactive session had meanwhile pushed 16 Ready → merged: 5 overlapped (penny, Hoover, Pepsi jet, Nintendo,
  glasses — my extra cautions/sources added to theirs), **7 new unique entries 17–23** → bank now **23 Ready**. Myths caught that a script would likely have repeated: McDonald's Monopoly "$24M" (court/DOJ: >$13M /
  >$20M), Nintendo love hotels, the 1899 Coke contract "freezing" the price, "Toblerone left Switzerland", cake-mix egg, Oakley 1996.
  Data: by type, B/E reels averaged ~68 % 3-s / 23 s / ~1,350 views vs F ~57 % / 17.7 s / ~255 (PERFORMANCE insight I) → pick order
  in topic_bank.md starts B → E → C → A → D. Analytics: Metricool still frozen (7th identical pull, IG + YT). ALGORITHM.md is 1 day old → not redone.
- 2026-10-27 | Visuals (interactive; owner sent reference reels: cinematic AI story reels with golden light, depth of field, film
  grain and a giant 3D title behind the hero) | Built `anim_cine.py`: same shot code, new look — measured on 3 past videos (De Beers,
  gas station, airline miles): renders fine, colours kept vibrant after a second tuning pass (first pass was hazy: bloom 0.32 → 0.18,
  contrast S-curve 0.18 → 0.42, saturation 1.08 → 1.16), cost +0.19 s/frame. Hook demo with `title3d("DIAMONDS")` behind the ring.
  | kept (template default; CINE=0 to switch off)
- 2026-10-27 | Visuals (interactive; owner sent 3D-look cartoon story reels: "improve our character, not follow exactly, 3D, better colours")
  | Built `anim_mascot3d.py`: same identity (square face, orange tie), new volume and colour (shaded head + hair, royal-blue suit,
  shirt, tie, pocket square, cel-shaded limbs, hands with thumbs, shoes, ground shadow); same `guy()`/`head_el()` API → checked on
  6 poses and 4 De Beers shots (holding props, expressions, edges). Fixed a blush bug (PIL draw punched holes in the face alpha —
  also present in the old head). | kept (template default; MASCOT3D=0 to switch off)
- 2026-10-27 | Visuals (interactive; owner: "it's using full frame and looks engaging", then "not about face or dress — colours,
  more natural and 3D, change the style of clothes") | Rebuilt the cast as a lit 2.5D renderer (each part → mask → distance-field
  height → normals; one lighting pass with key, coloured ambient, rim, specular, contact AO; soft cast shadow), 10 looks incl.
  hoodie/tee/jacket/suit/dress/cardigan/overalls/coat; hero is now the orange-hoodie character. New `anim_sets.py`: 6 full-frame
  sets, set_view camera (+ matching light), close-up/OTS/foreground-hand framing, smoke/embers/eyes, `say` captions, part badge,
  HUD set. cine_grade 0.35 → 0.22 s/frame (same output, max diff 0.005). Old shots render unchanged in API (S1/S7 De Beers with
  holds checked). Cost ≈0.1 s per character per frame. | kept (template default); PLAYBOOK §6 now asks for ≥50% scene shots
- 2026-10-27 (run 5) | Story | Hypothesis: avg watch is stuck at 13–23 s at every length, so the middle leaks; measurable script
  features (hook, open-loop gaps, reversals, connectors, figures per sentence, recaps, roadmap, ending) should line up with the
  retention we have, and a script fixing the weak ones can be checked before any audio. Research (sub-agent, primary sources, in
  lab/story/NOTES.md): curiosity gaps (Kang 2009), suspense model (Ely et al. 2015), emotional volatility/reversals (Berger, Kim &
  Meyer 2021; Knight et al. 2024), story speed (Toubia et al. 2021 PNAS), causal coherence (Trabasso & van den Broek 1985), LC4MP
  load; myths flagged: Zeigarnik memory effect (meta-analysis 2025: no effect), 8-second attention span. Built `tools/story_check.py`
  (7 gates, no audio needed; real times from work/align.json) and ran it on 13 example scripts vs Instagram rows of 6 animated reels
  (Spearman, n = 6): **item labels rho +0.93 with avg-watch % of length; roadmap 29–34 % (Costco, Starbucks, Planet Fitness, printer
  ink; + restaurant 33 %) vs none 19–24 % (Amazon, Chick-fil-A)**; keyword reversal/"but" counts ran the other way (−0.60/−0.72) →
  info only, not gates; hook length not punished (+0.77, confounded). Before/after on the same material (Monopoly, same facts):
  4/7 → 6/7, longest stretch without a question/teaser 38 → 25 s, twist→end 22 → 17 s, roadmap none → "three moves" (+3 s).
  Finding: the last 5 videos (Visa → Monopoly) all dropped the roadmap the older winners had. **Kept:** story_check in PLAYBOOK §4
  (+ QA 4b) and smoke test; R8 roadmap per type. Not validated on views yet (Metricool frozen, 9th identical pull) → prediction
  in PERFORMANCE K. ALGORITHM.md 1 day old → not redone. No template code changed.
- 2026-10-27 (run 6) | Sound | Hypothesis: on a phone speaker, SFX hits and loud notes land on top of words more often than the
  mix.py "VO/bed ≥ 14 dB" print suggests (it measures whole lines with a 150 Hz high-pass); a word guard that keeps the bed ≥ 12 dB under
  the voice in the phone band (300 Hz–10 kHz, 50 ms bed windows vs 300 ms voice level, max dip 10 dB) lifts the worst moments to the
  ≥ 10 LU commentary-over-music recommendation (Torcoli et al., JAES 67(12) 2019; non-experts prefer ~4 LU more) and raises
  intelligibility, without changing loudness. Built `tools/mix_check.py` (per-line + 400 ms momentary loudness difference voice − bed,
  K-weighted, phone band; phone + full-band ESTOI; I/TP/LRA) and `lab/sound/` (hook.py, soundlab.py). Same VO/music/SFX, rebuilt from
  examples/ (Kokoro default VO): **printer ink** momentary LD p5 8.5 → 12.1 LU, windows < 10 LU 6.2 → 2.6 %, line min 12.7 → 15.3,
  ESTOI phone 0.952 → 0.962 (full 0.947 → 0.959); **gas station** p5 7.5 → 12.0, < 10 LU 8.3 → 3.2 %, line min 8.3 (b2 under 10) → 12.5,
  ESTOI 0.950 → 0.960 (0.946 → 0.956); **Hoover** p5 9.7 → 13.0, < 10 LU 5.3 → 2.1 %, line min 9.0 (d5) → 17.1, ESTOI 0.952 → 0.959
  (0.940 → 0.950). I/TP unchanged (−11.7…−11.8 / −1.5). Cost: bed −1.6 LU during speech, −0.7 LU in gaps (gas); parakeet ASR on the
  phone-filtered final mix: WER 0.119 → 0.114 (gas), 0.106 → 0.106 (Hoover; errors are number spellings) → no regression. Max dip 18 vs
  10 dB: equal within 0.6 % → kept 10 (SFX keep punch). Guard 10 dB: weaker (p5 11.4). **Kept:** `bed_carve.guard()` default in
  template mix.py (`GUARD=12`, 0 = off; lib == lab output to 1e-8), mix.py saves work/stem_vo.wav + stem_bed.wav and prints the
  loudnorm mode; template TP −1.0 → −1.5 dBTP (examples since Hoover already used −1.5; template had drifted); smoke test now checks
  the guard (synthetic bed: p5 5.1 → 10.6 LU); setup installs pystoi + pyloudnorm (MIT). Found, not fixed: loudnorm runs in dynamic mode
  on every mix (backlog). Analytics: IG pull ≈ identical to 01:45 IST (±3 views), De Beers still 0 (same-day), YouTube rows frozen
  since 27 Oct. ALGORITHM.md 1 day old → not redone.
- 2026-10-28 (run 7) | Visuals | Bank had 20 Ready → not Topics; Visuals/Tooling never worked → Visuals. Hypothesis A (data): something
  measurable in the first 3 s (frame-0 content, caption timing, motion, cuts, colour) explains why some reels lose viewers at 3 s (Duolingo
  24.8 % vs printer 73.7 %). Hypothesis B (craft): captions land in the platform UI (IG/YT overlays) more often than PLAYBOOK §6 assumes,
  and the caption helpers can keep them out automatically without changing the look. Research: measured app safe zones (adchecklab,
  verified 28 Sep 2026: IG organic 250/319/86/119 px; Meta ads 14 %/35 %/6 %), ClipSpeed (Sep 2026: YT ~288/288/140), Reap (7 Sep 2026: no
  official organic specs exist). **A — rejected:** `lab/visuals/first3s_features.py` on the 14 posted MP4s (hosting branches) vs IG 3-s rate,
  n = 9: every feature |rho| ≤ 0.27 (≤ 0.58 without Duolingo, none p < 0.1); 5 reels opened on an empty disc (mean 3-s 56.5 %) vs 4 with
  object + caption (57.6 %; 68.5 % without Duolingo, whose first 3 s look like gas station's) → topic/hook line decide (PERFORMANCE Q).
  **B — kept:** built `tools/layout_check.py` (renders each sampled frame twice, captions on/off, diff = exact caption pixels; zones = PLAYBOOK;
  `--fake-align` needs no audio) and ran it on all 15 examples rebuilt with the template (590 frames, every 3 s + first 3 s ×9). Before → after
  the template fix, same shots and timings: frames with captions in a UI zone **51 → 17** (settled, excluding full-width whip blurs 47 → 13),
  **in the first 3 s 16 → 2** (Hoover 9 → 0: the 3D "HOOVER" title's extrusion reached x 975; gas station 4 → 0: unclamped lead line to x 981),
  right-edge hits 16 → 3, bottom 17 → 8 (banana source chips at y ≈ 1550 now stop at 1505–1509), De Beers 4 → 0, airline 2 → 0. Remaining:
  ≤ 231-px anti-alias specks (Chick-fil-A, Costco), Hoover t = 39/87 s hairlines, whip transitions. Render cost 1.25 s/frame both ways.
  Template: ed_el lead/tail fit `maxw`; `safe_xy()` + `SAFE` switch in anim_base; ed_show/say/title3d/hud_rule/hud_choice + every chip nudge
  inside (< 220 px intrusions only); say max_w 860 → 800; title3d fits visible width incl. extrusion/shadow and centres the visible mass;
  chip max 800 px; part_badge title ≤ 600 px; hud_choice y 1480 → 1420, width 900 → 800; hud_clock y 262 → 272. Smoke test now renders video
  (layout_check on the Hoover shots + 1 s anim.py encode); passed. PLAYBOOK §6/§8 updated. Analytics: IG + YT pulls identical to 06:00 IST
  (no rows for Monopoly/Hoover/banana yet). ALGORITHM.md 2 days old → not redone.
- 2026-10-31 | Story + Brand (interactive; owner 30 Oct: "story line and everything need to be good, and topic… later I will get brand deals")
  | Data (Metricool 31 Oct 00:30 IST, 16 animated reels): story-shaped videos hold longest (Monopoly 31.2 s avg = channel best) but
  sends/saves/comments ≈ 0 and reach per reel fell ~1,300 → ~150 (27–28 Oct); Instagram ranks on watch time + sends per reach.
  Built: STORY.md (hero = "you", three series YOUR MOVE / SPOT THE TRICK / WHO REALLY OWNS IT, beat sheets, writing rules, signature
  beats incl. one "Oops."), BRAND.md (what sponsors buy, YPP/creator-marketplace eligibility, brand-safety rules, sponsor formats,
  disclosure, media-kit metrics, cadence), story_check S-gates (series, seat, stakes ≤ 15 s, series ending, Oops ≤ 1, part logic;
  "problem"/"question" now count as roadmap labels), writers' room `episodes/` with the pilot YOUR MOVE EP 1 Parts 1–2 (Pepsi jet;
  both 7/7 R + 6/6 S), PLAYBOOK gates (seat + choice, brand-safe) + posting (2 a day at 00:00/05:00 IST, firstCommentText = choice).
  Scheduled tasks: episodes 16:05 + 21:05 UTC; R&D → writers' room 3×/day. | kept; measure: sends + comments per 1,000 reach on the
  first 5 episodes vs the 16 animated reels before (≈ 0)
