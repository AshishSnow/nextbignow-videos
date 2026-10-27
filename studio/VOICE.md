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

**Known limit of our metric:** UTMOS-family predictors track acoustic signal quality, not intonation or expressiveness
(arXiv 2608.09930, Aug 2026: no significant correlation with human ratings on intonation/expressiveness). So UTMOS is a
guardrail (don't get worse), and melody/feel must be judged with pitch range, the question/reveal contours and listening.

Status 27 Oct 2026: **not yet met.** Kokoro (default) passes the numbers; Chatterbox scores higher on UTMOS (+0.06 per line on
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
| **Chatterbox-Turbo 350M** (ResembleAI/chatterbox-turbo-ONNX, Dec 2025) | MIT (27 Oct 2026); model card: outputs may carry an inaudible PerTh watermark — the ONNX path only adds it if you call perth, we don't | yes: q8 LM RTF 12.7 (too slow), **q4 LM RTF 1.8** | see bake-off below |
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

## Rules learned
1. Never shift the whole voice up; use the blend for brightness (Kokoro lab, 26 Oct).
2. Slower + longer pauses helps; per-sentence generation helps Kokoro (SPLIT 0.12).
3. Chatterbox copies the reference clip's pace and melody → control delivery by choosing/making the reference, not with
   time-stretch. Keep references synthetic, 8–12 s, the same narrator, calm and expressive.
4. Chatterbox-Turbo on CPU: always the **q4** language model (q8 is 7× slower for the same score).
5. UTMOS can't hear melody — never accept a change that only raises UTMOS by flattening the voice (Kokoro dry scores 4.52 at 12.5 st: flat).

## Next
- **Hybrid endings:** Chatterbox take + a pitch move only on the last word of `q`/`low` lines (no global PSOLA, which costs −0.23),
  or a second reference clip whose sentences end clearly low; goal: low_fall ≤ −4 st with UTMOS ≥ Kokoro + 0.05.
- Question lines: both engines often don't rise on long "Do you know … ?" hooks (q_rise −1 … −7 st) → test shorter hook questions.
- Build a second synthetic reference with more smile/energy (Kokoro read with wider PSOLA, EXS 1.3) and compare.
- Paralinguistic tags (`[chuckle]`, `[sigh]`) at one funny moment — check ASR doesn't count them as errors.
- Add an expressiveness check beyond range: question-final rise (st) and reveal-final fall per line.
