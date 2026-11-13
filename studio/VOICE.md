# Narrator voice — spec and engine research

Owner's brief: "find what voice suits my content". The narrator is a faceless explainer of business secrets for a
US/UK/EU audience on Reels/Shorts. Synthetic voice only (posts carry the AI label); open-weight models whose licence
allows commercial use; never ElevenLabs; **never clone a real person** — any reference clip must itself be synthetic
(our Kokoro narrator) and live in `studio/voices/` (< 1 MB).

## Spec (what "done" sounds like)
| Dimension | Target | How we measure |
|---|---|---|
| Timbre | Young-adult male, warm, mid-low (F0 median 130–150 Hz), clear consonants, no buzz/metallic edge | F0 median; listen |
| Naturalness (acoustic) | UTMOS ≥ 4.4 on whole VO **and** mean of per-line UTMOS ≥ 4.4, no line < 4.2 | `tools/tts_bakeoff.py score` |
| Intelligibility | 0 ASR bad lines, WER ≤ 2 % | parakeet read-back |
| Pace | 160–180 wpm while speaking, real pauses before reveals | bake-off `wpm_speaking` |
| Melody | Pitch range ≥ 15 st; questions rise, reveals land low; no "sing-song" PSOLA artefacts | `range_st`; listen to i1 (question) and the reveal line |
| Feel | Curious friend letting you in on a secret — calm, warm, a smile in the voice; not a hype-man, not a newsreader | listen |
| Cost | ≤ 5 min CPU (2 cores) for an 80 s VO | `rtf` × duration |

**Known limit of our metric:** our UTMOS22 tracks acoustic quality, not intonation. arXiv 2608.09930 (10 Aug 2026, re-read
27 Oct): of the automatic judges, only UTMOSv2 (τ≈0.29), Audiobox-Aesthetics CE (τ≈0.37) and PQ (τ≈0.27) correlate at all with
human *intonation* labels, NISQA/DNSMOS don't, audio-LLM judges mostly don't — and humans agree least on intonation (α 0.47).
So UTMOS is a guardrail (don't get worse), and melody is judged with pitch range, `q_rise_st`/`low_fall_st` and listening.
Whole-file UTMOS on 80–90 s files moves ±0.1 for edits that change per-line scores by < 0.01 → trust the per-line mean.

Status 27 Oct 2026 (De Beers video): **closer, not yet met.** Lighter chain lifts per-line mean to 4.43 and the worst line to 4.07; still short of
"no line < 4.2" (the worst is always the shortest line).
Status 27 Oct 2026 (3rd R&D run): **closer, not yet met.** Kokoro's weak lines came from our own PSOLA, not from Kokoro: a per-line
prosody gate (below) lifts the worst line to 4.25 on gas and airline (was 3.98 / 4.05). Remaining gaps: questions (q_rise −2.8 on
Duolingo's long hook), and lines the EQ/clean/room chain drops (airline a3 4.15–4.27, gas d2 4.23–4.26).
Status 27 Oct 2026 (2nd R&D run): **not yet met.** Hybrid endings (below) fix most of Chatterbox's statement endings, but its
questions still fall (q_rise −1.8…−6.7 st) and it has occasional weak lines (Duolingo a2: 3.91). Kokoro stays default.
Status 27 Oct 2026 (1st run): **not yet met.** Kokoro (default) passes the numbers; Chatterbox scores higher on UTMOS (+0.06 per line on
4 scripts) but its reveal lines don't land low (low_fall −0.2…−2.5 st vs Kokoro −4…−7) — it sounds "evener", which UTMOS rewards
and our format punishes. **Decision: Kokoro + PSOLA stays the default; Chatterbox is available as `ENGINE=chatterbox`**
(e.g. as a fallback, or if a future test fixes its endings). Added `q_rise_st`/`low_fall_st` to the bake-off so this is measured.

## Research basis (deep research 26–27 Oct 2026 — why these targets)
| Dimension | Evidence-based target | Source |
|---|---|---|
| Pace | 165–185 wpm overall incl. pauses (recall best at 170–190; ≥ 210 overloads, ~150 feels slow). Hook a bit faster, the key-number sentence slower (~150) | Rodero 2015/2020; Smith & Shaffer 1995 |
| Pauses | commas 150–250 ms, sentence ends 350–500 ms, **one 600–800 ms beat before each big reveal** (1–2 per video), never > 1 s | MacGregor et al. 2010 (pause before a word improves recall of it); Campione & Véronis 2002 |
| Pitch | male median ~110–150 Hz; variation matters, level doesn't — wide range reads charismatic, but *medium* variation beats high (over-acted) and monotone | Niebuhr 2017; Rodero 2022; Yang 2024 (US male mean ~116 Hz) |
| Melody | sentences start high, end low; statements fall, only real yes/no hooks rise (rising statements sound unsure) | Rodero, Potter & Prieto 2017; Levon & Yang 2019 |
| Emphasis | one focus word per sentence (two max): +2–4 st, 20–30 % longer, +2–3 dB; over-emphasis hurts | Rodero 2021; Frontiers 2022 (stress cues) |
| Timbre | warm, clean, audible "smile" on hook and payoff; no hiss/clicks (digital artefacts are the #1 AI-voice tell, then unnatural pauses, flat delivery) | Tartter 1979; Drahota 2008; Interspeech 2025 |
| Accent | General American young-adult male is a sensible default (European listeners understand GA as well as RP; UK listeners spot synthetic British voices more often) | PLOS ONE 2020; Vocal Image 2026 |
| Policy | label posts AI on Instagram (realistic audio); YouTube needs no label for a generic narrator over animation; never synthesise a real person | Meta AI-label rules; YouTube disclosure policy (blog.youtube) |
Links: journalistsresource.org/media/radio-news-pace-words · frontiersin.org/journals/communication/articles/10.3389/fcomm.2022.869084 ·
journals.sagepub.com/doi/10.1177/01461672952110006 · pub.dega-akustik.de/DAGA_2017/data/articles/000256.pdf ·
journals.plos.org/plosone/article?id=10.1371/journal.pone.0231089 · isca-archive.org/interspeech_2025/srinivasavaradhan25_interspeech.pdf ·
blog.youtube/news-and-events/disclosing-ai-generated-content

## Engines tested (dates = when we checked the licence / model card)
| Engine | Licence (checked) | Runs here? | Result |
|---|---|---|---|
| **Kokoro-82M v1.0** (onnx) — blend am_michael .5 / am_eric .3 / am_fenrir .2 + Praat PSOLA prosody | Apache 2.0 | yes, RTF ~0.5 | default 26 Oct–27 Oct; UTMOS 4.26–4.47 shipped, range ~18 st |
| **Chatterbox-Turbo 350M** (ResembleAI/chatterbox-turbo-ONNX, Dec 2025) | MIT (27 Oct 2026); model card: outputs may carry an inaudible PerTh watermark — the ONNX path only adds it if you call perth, we don't | yes: q8 LM RTF 12.7 (too slow), **q4 LM RTF 1.5–1.8** | opt-in `ENGINE=chatterbox` + hybrid endings (27 Oct) |
| Pocket TTS 100M (Kyutai) | CC BY 4.0 | HF repo is gated (needs login) → not tested; preset voices are real speakers → would need a synthetic reference anyway | later |
| Qwen3-TTS 0.6B/1.7B (Jan 2026) | Apache 2.0 | needs torch; ~0.2× real time on an M4 → far too slow on 2 CPUs | no |
| Magpie TTS Multilingual 357M (NVIDIA) | NVIDIA Open Model License (commercial OK) | needs NeMo/torch | candidate, untested |
| Maya1 3B, Orpheus 3B, Dia 1.6B, Zonos | Apache 2.0 | GPU-class | no |
| Ming-3.0-tts-0.5B (inclusionAI, Sep 2026) | MIT | untested on CPU (only GPU numbers published); highest open-licence score on the Artificial Analysis arena | R&D candidate |
| NeuTTS Air (Neuphonic, 748M) / NeuTTS-2E, Nano | Air: Apache 2.0; **2E/Nano: free only under US$5M company revenue — avoid** | CPU-first, GGUF | R&D candidate (Air only) |
| Qwen3-TTS 1.7B VoiceDesign as a *reference maker* (interactive test 27 Oct) | Apache 2.0 | bf16 on 2 CPUs: ~2 min per 13–15 s clip — fine for making a reference, not as an engine | "energetic young male" prompts came out 215–275 Hz (too high); a 168 Hz design gave Chatterbox only UTMOS 4.15; Qwen 0.6B "ryan" as engine 3.95 → not useful yet |
| F5-TTS, XTTS-v2, Fish S2, IndexTTS-2.5, Spark-TTS, ChatTTS, OmniVoice | non-commercial / by agreement | — | never |
| Supertonic 3 | OpenRAIL-M, repo archived Sep 2026 | — | no |
Sources: yaps.ai local-TTS licence round-up (10 Oct 2026) https://www.yaps.ai/blog/best-local-tts-models ;
Cartesia open-source TTS by licence (9 Oct 2026; Artificial Analysis Elo: Kokoro 1064, Chatterbox 1026) https://www.cartesia.ai/learn/open-source-tts ;
model card https://huggingface.co/ResembleAI/chatterbox-turbo-ONNX ; evaluator limits https://pith.science/paper/2608.09930

## Bake-off 27 Oct 2026 (same lines, same pauses; "shipped" = through make_vo's EQ + voice_clean + room chain)
Chatterbox voice = `voices/narrator_slow.cbcond.npz`: conditioning from an 11 s clip of **our own Kokoro narrator** read at
SPD 0.78 with the PSOLA melody (synthetic, `voices/narrator_slow_ref24k.wav`). UTMOS = whole file / mean per line (min line).
| Material | Kokoro shipped (make_vo) | Chatterbox q4 + slow ref, shipped | Δ |
|---|---|---|---|
| Gas station lines i1–b2 (37 s) | 4.474 / 4.43 (4.38), 18.1 st, 163 wpm | 4.544* / 4.494 (4.44), 17.0 st, 169 wpm | +0.07 / +0.06 |
| Gas station lines b3–e2 (43 s) | 4.257 / 4.38 (4.19), 18.3 st, 176 wpm | 4.336 / 4.459 (4.39), 17.2 st, 168 wpm | +0.08 / +0.08 |
| Duolingo full script (91 s) | 4.375 / 4.424 (4.38), 18.4 st, 176 wpm | 4.519 / 4.484 (4.43), 16.3 st, 177 wpm | +0.14 / +0.06 |
| Costco full script (83 s) | 4.340 / 4.405 (4.31), 17.1 st, 176 wpm | 4.471 / 4.468 (4.22), 16.3 st, 174 wpm | +0.13 / +0.06 |
| **Line-end melody** (q_rise / low_fall, st; gas1, gas2, duo, costco) | low: −5.5, −4.2, −7.2, −5.2 | low: −2.3, −2.5, −0.2, −2.3 | **Chatterbox lands endings 2–7 st less low** |
| End-to-end `ENGINE=chatterbox make_vo.py` (gas i1–b2) | 4.474 | 4.534, 17.1 st, 168 wpm, 1 min 47 s for 37 s VO | +0.06 |
| Chatterbox + make_vo PSOLA (EXS 1 / EXS 0 BMP .5) | | 4.302 (24.8 st!) / 4.307 (17.8 st) | PSOLA on Chatterbox = −0.23 |
*dry, before chain. Earlier variants on the first excerpt (q8 LM): flat Kokoro ref 4.517/4.461, 13.2 st, 186 wpm (too fast, flat);
PSOLA ref 4.528/4.478, 16.0 st, 187 wpm; slow PSOLA ref 4.542/4.49, 16.4 st, 165.5 wpm → **the reference sets pace and melody**.
Pace-matching a fast take with a global PSOLA stretch (×1.12) cost −0.05 UTMOS → make the reference slow instead.

## Hybrid endings — 27 Oct 2026, 2nd run (`lib/end_contour.py`, on by default under `ENGINE=chatterbox`)
Hypothesis: a pitch move on only the last word of `low` lines (PSOLA on that slice, cross-faded into the untouched take) gets
Chatterbox to low_fall ≤ −4 st without the −0.23 UTMOS cost of global PSOLA. Same 3 scripts, all through the shipped chain.
UTMOS whole / per-line mean (min line), low_fall st. Kokoro = shipped default (make_vo).
| Script | Kokoro shipped | Chatterbox q4 | Chatterbox + endings (−4 st, gate 0.05) |
|---|---|---|---|
| Gas station (80 s) | 4.317 / 4.399 (4.13), −4.8 | 4.522 / 4.480 (4.40), −1.3 | 4.513 / 4.476 (4.40), **−4.0** (7 of 8 lines moved) |
| Costco (83 s) | 4.321 / 4.402 (4.30), −4.9 | 4.501 / 4.474 (4.43), −1.0 | 4.380 / 4.468 (4.41), **−3.5** (5 of 7) |
| Duolingo (91 s) | 4.382 / 4.428 (4.38), −7.1 | 4.264 / 4.458 (3.91), −0.2 | 4.253 / 4.449 (3.91), −1.7 (5 of 6 moved: each −2…−3.5 st; a2 = the weak 3.91 line, ends in +5 st uptalk, gate skipped it) |
What we learned on the way (each cost a version):
1. v1 ramp to the end of the slice: barely moved anything — voicing ends 0.1–0.2 s before the line does, and parakeet's word
   starts run ~0.2 s late. → the move starts ≥ 0.5 s before the last voiced frame and is complete by 45 % of the word (a nuclear fall, then hold).
2. Chatterbox's "flat" endings are partly **uptalk** (gas e1 +4 st, c1 +1.2 st): a fall on top of a rise still ends high → cap the
   last word at the line median first, then fall.
3. Its endings already sit near 90–100 Hz; −5 st pushed some to ~70 Hz → creak, octave errors in the tracker (a4 read +7 st) and
   −0.2 UTMOS. → never below 85 Hz (`END_FLOOR`).
4. Some lines resist PSOLA (Duolingo a2 −0.16, gas b1 −0.16, Costco c2/e1 −0.27): a per-line UTMOS gate (keep the move only if
   the line loses ≤ 0.05) keeps the good moves and skips those.
5. +3…+4.5 st question rises on Chatterbox made q_rise *worse* (−1.8 → −2.1) and cost UTMOS → rises are off (`q=0`).

## Lighter chain — 27 Oct 2026, De Beers video (`DEESS`/`ROOM_DB`/`COMP` in make_vo.py; lab/voice_chain/chain_ab.py)
VOICE.md "Next" said short lines lose 0.1–0.2 in the EQ/de-ess/room chain. Tested chain-only on **one fixed vo_raw.wav** (so PSOLA/gate
run-to-run noise is out): per-line UTMOS mean / min / mean of the 6 shortest lines, De Beers script (24 lines, 116 s).
| Chain | line mean | min | 6 shortest |
|---|---|---|---|
| old: de-ess −11, room −21 dB, comp 2.2:1 | 4.396 | 3.996 | 4.301 |
| de-ess −8 | 4.400 | 4.011 | 4.308 |
| room −27 | 4.414 | 3.983 | 4.319 |
| de-ess −8, room −27 | 4.417 | 4.000 | 4.326 |
| room −33 / dry (no room) | 4.416 / 4.404 | 3.981 / 3.964 | 4.314 / 4.302 |
| **de-ess −8, room −27, comp 1.5:1 (new default)** | **4.425** | **4.063** | **4.344** |
| … comp off | 4.427 | 4.130 | 4.355 |
Stage ablation on the weak short line a1 ("Move one. Control the supply."): flat 4.32 → PSOLA 4.22 → EQ 4.22 → voice_clean 3.96;
inside voice_clean the **2.2:1 compressor** costs it 0.14 (no comp 4.10), the expander 0.05, tilt/320 Hz cut nothing.
Kept 1.5:1 rather than off so line levels stay even under the music (mix LINE_DB still does the intentional moves).
Shipped VO (make_vo with the new chain, gate re-run): whole 4.396 (chunked), per-line 4.426 (min 4.07), 18.2 st, low_fall −6.6 st,
169.8 wpm, 0 ASR bad lines — vs the same script on the old chain 4.361 / 4.398 (min 4.02).

## Prosody gate — 27 Oct 2026, 3rd run (`PGATE`, default 0.15 in make_vo.py; lab/voice_gate/)
Diagnosis on the gas script: every **flat** Kokoro line scores 4.43–4.52; after our PSOLA moves c1 falls to 3.93 (b2 4.26, a2 4.33).
So the weak lines are ours. PSOLA is near-transparent only for moderate shifts (±6 st "safe" for TTS pitch moves, arXiv 2512.16519);
our moves stack range ×1.45 + base + stress +2.4 st + endings, clipped at −12/+13 st. Fix: score each line after PSOLA against its
flat take; a line that lost > 0.15 is re-rendered at 0.6 (then 0.3) strength. UTMOS whole / per-line mean (min), range, low_fall:
| Script | Before (template) | PGATE 0.15 (new default) |
|---|---|---|
| Gas (79 s) | 4.234 / 4.379 (3.98), 18.1 st, −4.8 | 4.373 / 4.411 (**4.25**), 17.8 st, −4.8 (a2, c1 softened) |
| Duolingo (91.5 s) | 4.386 / 4.423 (4.37), 18.4 st, −6.8 | 4.421 / 4.421 (4.33), 18.3 st, −6.6 (a4 softened) |
| Airline (100 s) | 4.394 / 4.390 (4.05), 18.4 st, −5.3 | 4.402 / 4.406 (**4.25**), 18.2 st, −5.0 (c1 softened) |
Not adopted: a global pitch clip −7/+8 st (range fell to 15.0 st for the same gain); puck .1 blend as default (per-line mean equal
±0.005 on 3 scripts, worst line better on gas, worse on airline). Line-level noise: ±0.06 between identical runs. Cost +~40 s per VO.

## Per-line tempo — 14 Nov 2026 (childminding, `tools/tempo.py --target`)
usa_narr read this script at 149 wpm raw (163.5 speaking); trim_gaps → 159.2. Uniform atempo ×1.07 (7-Eleven method) → 170.6 wpm overall but
it also speeds lines that are already fast (hook i1 216 → 231 wpm, 11 lines > 200). Per-line target 178 (clamp 1.00–1.10, cut mid-gap) →
**166.7 wpm overall, 183.6 speaking, per-line UTMOS 4.443 (min 4.30) vs 4.439 (4.31) uniform, max line 216 wpm, 7 lines > 200, sd 22.3 vs 30.1.**
F0 134.2 Hz, 17.1 st, low_fall −5.4; ASR flags only spelling (b2 "£103", e3 "startup"). Default from now: `--target 178`.

## Rules learned
1. Never shift the whole voice up; use the blend for brightness (Kokoro lab, 26 Oct).
2. Slower + longer pauses helps; per-sentence generation helps Kokoro (SPLIT 0.12).
3. Chatterbox copies the reference clip's pace and melody → control delivery by choosing/making the reference, not with
   time-stretch. Keep references synthetic, 8–12 s, the same narrator, calm and expressive.
4. Chatterbox-Turbo on CPU: always the **q4** language model (q8 is 7× slower for the same score).
5. UTMOS can't hear melody — never accept a change that only raises UTMOS by flattening the voice (Kokoro dry scores 4.52 at 12.5 st: flat).
6. Check where a weak line is made before fixing it: score vo_flat, vo_raw and vo.wav per line (`lab/voice_gate/perline.py`).
   On Kokoro the PSOLA step makes the weak lines (3rd run); soften moves per line, not globally.

## Next
- ~~Chain drops on short lines~~ — 27 Oct: the compressor was the main cause → lighter chain is the default (table above). Next: confirm on 2 more scripts (gas, airline) with chain_ab.py.
- Old note: **Chain drops on short lines:** airline a3 ("And Delta isn't the only one.") and gas d2 lose 0.1–0.2 in the EQ/de-ess/room chain,
  not in PSOLA. Measured (airline a3): raw 4.263, +EQ 4.259, +voice_clean 4.217, +room 4.149 → A/B a lighter de-esser and a drier room.
- Gate on the *chained* line (Duolingo a4 scored better raw at 0.6 but worse after the chain).
- ~~Hybrid endings~~ — done 27 Oct (table above): low lines now land (−3.5…−4.0 st) at ≤ 0.01 per-line UTMOS cost.
- **Chatterbox retakes for weak lines:** it's deterministic, so a weak line (per-line UTMOS < 4.3, e.g. Duolingo a2 3.91) can only
  change through its text: try 2–3 punctuation variants ("dollar." / "dollar…" / comma before the number) and keep the best.
  If that lifts min-line ≥ 4.3 on all 3 scripts, Chatterbox + endings beats Kokoro on everything except questions.
- **Questions on Chatterbox:** shorter hook questions ending on the key word ("…makes money on gas?"), or a question reference clip.
- Second scorer for intonation: UTMOSv2 or Audiobox-Aesthetics (both correlate with intonation, 2608.09930) — check licence/onnx/RAM.
- Question lines: both engines often don't rise on long "Do you know … ?" hooks (q_rise −1 … −7 st) → test shorter hook questions.
- Build a second synthetic reference with more smile/energy (Kokoro read with wider PSOLA, EXS 1.3) and compare.
- Paralinguistic tags (`[chuckle]`, `[sigh]`) at one funny moment — check ASR doesn't count them as errors.
- Add an expressiveness check beyond range: question-final rise (st) and reveal-final fall per line.

- 2026-11-01 (drone episode): EXS 1.15 confirmed on a 2nd script (per-line 4.407 = 4.407, min 4.28 → 4.31, range 18.1 → 18.8 st, low_fall −6.0 → −6.3 st) → **template default**. Wh-question hook ('How can one drone start a whole business?', ending None) replaced the yes/no hook (q_rise was −4.4 st, i.e. it fell like a statement). SPD 1.0 for line speeds 1.0–1.04 (163 → 168 wpm).
- 2026-11-03 (food truck): take comping via `tools/comp_takes.py <project> <tag>` (needs work/vo_<tag>.wav, align_<tag>.json, vr_<tag>.log): only 1 of 23 lines swapped, per-line 4.412 → 4.414. A rewrite of the weak line beat it: spelled-out 'two thousand two hundred' 4.18 → 'twenty-two hundred' ≥ 4.26. Rewrite weak lines first, comp second. 'Save this.' alone misreads in ASR.
- 2026-11-04 (Christmas lights): **second voice.** `VOICES = {line_id: "af_heart:1.0"}` in vo_lines.py gives a line its own Kokoro voice (make_vo: narrator-only median, second voice clipped around its own register). Crew lead announces each step, the narrator explains. Mentor lines per-line UTMOS 4.26–4.46 after rewrites (first drafts: "Get covered before you climb" 3.96, "Own the lights yourself" 4.10; the prosody gate softens short step lines, so give them 6+ words). **The chunked whole-file UTMOS reads low on two-voice files (3.96–4.10 for per-line 4.39–4.41), and whole-file F0 range is inflated by the second voice: judge per-line only.** ASR reads "roof work" as "roofwork": a false bad line.
- 2026-11-05 (Spotify, HOW IT WORKS EP 1): **Chatterbox-Turbo beat Kokoro on the same text, and meets the spec's numbers for the first time.** Kokoro (SPD 1.0): per-line 4.388, min 4.20 (e1 weak), 18.3 st, low_fall −5.5, 174 wpm, 127.6 s, ASR 1 line flagged (d1 'Middle Man', false). Chatterbox q4 + narrator_slow, END_ST −4: 4.483, min 4.37, 0 weak lines, 16.7 st, low_fall −3.3, 165 wpm, 133.8 s, 0 ASR bad lines. **END_ST −5.5: 4.481, min 4.37, 16.7 st, low_fall −4.2, 165 wpm, 0 ASR bad → shipped.** NextBigNow's own narration is also Chatterbox Turbo (whatif-v3/README). Costs: range −1.6 st, softer falls than Kokoro, slower by 6 s; no yes/no question on the script needed a rise except z1, and it falls. **All of this is metrics: nobody has listened to it, including me. Owner's ear decides.** The mix needed the bed ~2.7 dB lower than the template (M −10.2 dB) to keep momentary LD p5 ≥ 10 LU (10.1). Render time for VO 133 s: ~5 min on 2 CPUs.
- 2026-11-06 (reselling, HOW TO START EP 5): **three findings, all metrics, nobody has listened.** (1) **Chatterbox is not deterministic.** The notes above say it is; they are wrong. The same text gives a different waveform each generation, and one line's score moves a lot between runs (a1 4.46 vs 4.02, d4 4.09 vs 4.39, d3 3.93 vs 4.39). It also misreads at random: "Ask a tax pro" came out "tax bro" in 2 of 5 takes. (2) **So comp it.** Three to four full takes through `tools/comp_takes.py`: per-line 4.43 best single take → **4.455 comped, min 3.93–4.09 → 4.385, 0 lines under 4.3**. Each take ~5.5 min for a 120 s VO. Comp against a report you have checked by hand, because the tool picks on score and can pick a misread (set the bad line's score to 0 in voice_report.json first). (3) **The reference sets the pace: new `narrator_brisk`** (our own Kokoro narrator, SPD .92, EXS 1.3 instead of .78 / 1.15). Same text:
| Take | per-line (min) | range | low_fall | wpm speaking | length | ASR |
|---|---|---|---|---|---|---|
| Kokoro, SPD 1.0 | 4.398 (4.31) | 19.0 st | −4.9 | 174 | 119.5 s | 0 bad |
| Chatterbox narrator_slow | 4.484 (4.41) | 16.6 st | −4.3 | 152 | 135.5 s | 0 bad |
| Chatterbox narrator_brisk, one take | 4.40–4.43 (3.93–4.09) | 18.9–19.2 st | −3.9…−5.1 | 175 | 118.7 s | 0–1 bad |
| **Chatterbox narrator_brisk, comped from 4 takes → shipped** | **4.455 (4.385)** | **19.0 st** | **−4.3** | **174** | 120.1 s | **0 bad** |
Brisk loses ~0.03 per line to slow but gains 2.4 st and 15 s of pace; F0 155 Hz sits above the spec's 130–150 Hz. END_ST −7 gave no deeper fall than −5.5 (the floor and gate stop it), so −5.5 stays. "Comment one word" read back "come in one word": "Leave a one-word comment." Weak-line rewrites still do more than anything for a specific line (d3 "all income" 4.06 → "all of your income" 4.39). **Chatterbox + narrator_brisk is now the template default** (2nd script it beat Kokoro; ENGINE=kokoro for the old voice). Multi-sentence Chatterbox lines hold real silence, which mix_check counted as "speech": fixed, see IMPROVEMENTS.
- 2026-11-07 (exporting, HOW TO START EP 7): **line speeds 0.95 (step titles) / 0.96 (body) / 0.97 (CTA)** with narrator_brisk + 3 comped takes = **173.9 wpm speaking** (0.96–0.98 gave 176.8–187), per-line 4.455, min 4.37, F0 148.5 Hz (inside the 130–150 spec for the first time), 18.0 st, low_fall −4.3, 0 ASR bad after two rewrites. Comp order that worked: base = take 1 with misread lines' text updated in align.json + score 0 → comp n2 (7 swaps) → re-run voice_report → comp n3 (1 swap). **Default line speeds for new scripts: 0.95–0.96.**
- 2026-11-08 (Prime 'Iliad', HOW IT WORKS EP 4): **dead air inside lines.** Chatterbox left 2.1–2.4 s silences between sentences of one line (4 cuts, 8.5 s = 7 % of the VO). `tools/trim_gaps.py <project>` (run after comping, before music/mix) caps any in-line silence > 0.65 s at 0.45 s and shifts align.json; between-line pauses stay. Note: voice_report's `wpm_speaking` = words / summed line durations, so in-line dead air counted as speech: 179.7 before the trim, 195 after (the true phrase rate); judge pace on `wpm_overall` (target 165–185 incl. pauses: 175.7 here). Comped per-line 4.465 (min 4.38), 0 ASR bad. Next: check whether 0.92 line speeds bring the phrase rate under ~185 without slowing the overall below 165.
- 2026-11-09 (dropship, HOW TO START EP 8): **pace gap closed with pauses, not speed.** Line speeds unchanged (0.95/0.96/0.97); Chatterbox left 0.84–1.0 s between sentences inside 11 lines (one 2.14 s). `trim_gaps.py` at 0.55 → 0.42 s (new default) cut 7.1 s: overall 161.2 → 171.2 wpm, per-line UTMOS 4.462 → 4.458, min 4.33, 18.1 st, low_fall −4.8; between-line beats (0.7 s after the hook question, 0.65 s before "Not to the FTC") kept. Note `wpm_speaking` rose to 189 because it now measures speech without the dead air — judge pace on `wpm_overall`.
- 2026-11-10 (same cart, HOW IT WORKS EP 5): **line speeds 0.94 body / 0.97 CTA** (from 0.95–0.97) with narrator_brisk + 4 takes comped: wpm_speaking 183.9 (dropship at 0.95–0.97: 189), wpm_overall 166.9, per-line UTMOS 4.458 (same), min 4.38. Slower lines also left less dead air for trim_gaps (0.96 s vs 7.1 s). **New default for scripts: 0.94 body, 0.97 CTA.** Note: one take of four was weak (mean 4.36, min 3.80) — keep ≥ 3 takes. ASR heard "Its promise now?" as "It's promised now?" in every take: an "Its + noun" opener is risky; name the company instead.
- 2026-11-10 (R&D Voice run): **(1) the per-line speed column does nothing on Chatterbox.** `make_vo.py` calls `cb.say(text)` with no speed (Turbo has no speed knob), so the 7 Nov and 10 Nov notes above that credit pace changes to line speeds 0.94–0.97 are wrong: those differences were different scripts and different takes. Pace on Chatterbox = the reference + pauses + `trim_gaps.py`. **(2) Re-timing to fake a speed costs too much:** Praat PSOLA per line (`lab/voice_engine/pace_lab.py`, same audio, gap-trimmed first) at 0.94 on brisk cut per-line UTMOS 4.469 → 4.378 (Netflix) and 4.423 → 4.344 (childminding), min 4.29 → 4.15 / 4.12 → 3.70; at 1.04 on hype 4.492 → 4.403 / 4.479 → 4.415 → **rejected**. **(3) narrator_hype beats narrator_brisk → new default `CBV`.** Same text (first 10 lines of the two queued scripts 19 Netflix + 20 childminding), q4, 2 takes each, scored after the same gap trim:
| Script · reference | per-line UTMOS (min) | range | low_fall | phrase rate | overall* | ASR bad |
|---|---|---|---|---|---|---|
| Netflix · brisk | 4.469 (4.29) | 18.2 st | −1.4 | 183.7 | 167.8 | 2 (number spellings) |
| Netflix · **hype** | **4.492 (4.40)** | **20.2 st** | **−4.2** | **170.1** | 156.4 | **0** |
| Childminding · brisk | 4.423 (4.12) | 17.8 st | −2.3 | 192.9 | 172.7 | 0 |
| Childminding · **hype** | **4.479 (4.40)** | **18.7 st** | **−3.6** | **182.9** | 164.6 | 0 |
*overall = words / (lines + script pauses × PZ 1.6), before the end-contour pass. Untrimmed bake-off rows (both takes): brisk 4.454/4.482 and 4.435/4.427, hype 4.492/4.492 and 4.479/4.479 — take 2 of hype was within 0.001 of take 1 on both scripts, so the run-to-run spread was small this time. Hype wins per-line mean, worst line, melody range and landings, and brings the phrase rate down into or near the 160–180 spec (brisk sat at 184–193). Costs: overall pace 156–165 wpm, a little under the 165–185 target (cutting PZ to 1.2 only adds ~3 wpm — leave the reveal beats), and F0 155–160 Hz (brisk 150–155; spec 130–150). **Still metrics only: the owner chose hype by ear on 8 Nov (Michelin); nobody has listened to this A/B.** If a build sounds over-excited, `CBV=narrator_brisk` restores the 6 Nov voice. Smoke test passed with hype (chatterbox UTMOS 4.459, 0 ASR bad).
- 2026-11-11 (Netflix 2011, HOW THEY GOT SO BIG EP 4 — first full build on narrator_hype): **(1) "takes" are not independent on Chatterbox Turbo** — greedy decoding: take 2 came out byte-identical to take 1 (same per-line scores to 3 decimals). Variety comes from *text* changes (and small prosody-gate differences between runs): a re-voice with 3 weak lines rewritten changed i1/b1/b2/b4 by ±0.1 too, so comp the rewritten run against the first one (base = run 2, 5 swaps from run 1, b5 swapped by giving align_t1 the new text). Don't spend 6 min per identical take. **(2) Pace: `tools/tempo.py` (ffmpeg atempo 1.05, WSOLA, pitch kept) after trim_gaps — A/B on the same trimmed take: per-line UTMOS 4.380 → 4.359 (−0.021; PSOLA cost −0.06…−0.09), range 20.1 → 20.1 st, overall 155.2 → 162.9 wpm; rubberband (ffmpeg filter, formant preserved) wrecked it (2.47).** Shipped: hype, 2 runs comped + trim_gaps (9.1 s cut) + tempo 1.05 → **wpm_overall 162.0** (untrimmed 146), wpm_speaking 180.1, per-line 4.392, min 3.39 (the one-word "Oops!" line; short clips score low), F0 154 Hz, 20.3 st, low_fall −6.5, ASR 0 real misreads (a2 flag = "$9.99" formatting). Still 3 wpm under 165: next try tempo 1.07 on one script and re-check the per-line cost.
