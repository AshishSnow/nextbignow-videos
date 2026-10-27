# Sound lab — word guard + phone-speaker mix check (R&D run 6, 27 Oct 2026)

Hypothesis: SFX hits / loud notes land on words more often than mix.py's "VO/bed ≥ 14 dB" (whole line, 150 Hz HP) shows; on a phone
speaker that costs clarity. A guard keeping the bed ≥ 12 dB under the voice in 300 Hz–10 kHz fixes the worst moments at no loudness cost.

Research
- Torcoli, Freke-Morin, Paulus, Simon, Shirley, "Preferred levels for background ducking to produce esthetically pleasing audio for TV
  with clear speech", J. Audio Eng. Soc. 67(12):1003–1011 (2019): commentary over music ≥ 10 LU, over ambience ≥ 15 LU; non-experts
  prefer ~4 LU more than the experts who mix. https://cris.fau.de/publications/234640600 ; Fraunhofer IIS blog (12 Apr 2019)
  https://www.audioblog.iis.fraunhofer.com/?p=4251
- YouTube turns programmes louder than −14 LUFS down (Wikipedia "Audio normalization", citing Pro Video Coalition 2018).
  Instagram: no official number; blog claims (cutscore.io, audioforgepro.com, 2026) are unsourced → treated as unknown.

Method: examples printerink / gasstation / hoover rebuilt in $STUDIO/projects/lab_20261027 (Kokoro default VO, example music.py +
mix.py with `hook.py` exec'd after `mix = VO + bed`; env TAG, GUARD, GMAX, PRELIM, TGT). Metrics: tools/mix_check.py; asr_mix.py
(parakeet on the phone-filtered final mix, crude WER — number spellings dominate the errors).

| Video | Variant | LD p5 (LU) | windows < 10 LU | line min | ESTOI phone / full | I / TP / LRA |
|---|---|---|---|---|---|---|
| printer ink | A shipped | 8.5 | 6.2 % | 12.7 | 0.952 / 0.947 | −11.7 / −1.5 / 2.0 |
| | C guard 12, max 18 | 12.1 | 2.0 % | 15.5 | 0.962 / 0.959 | same |
| | **F guard 12, max 10** | 12.1 | 2.6 % | 15.3 | 0.962 / 0.959 | same |
| | G guard 10 | 11.4 | 3.1 % | 14.9 | 0.959 | same |
| | E guard 15 + prelimit | 14.4 | 1.6 % | 17.8 | 0.969 | −11.3 |
| gas station | A | 7.5 | 8.3 % | 8.3 (b2) | 0.950 / 0.946 | −11.8 / −1.5 / 2.0 |
| | **F** | 12.0 | 3.2 % | 12.5 | 0.960 / 0.956 | same |
| Hoover | A | 9.7 | 5.3 % | 9.0 (d5) | 0.952 / 0.940 | −11.8 / −1.5 / 2.0 |
| | **F** | 13.0 | 2.1 % | 17.1 | 0.959 / 0.950 | same |

ASR WER (phone-filtered final): gas 0.119 → 0.114, Hoover 0.106 → 0.106. Bed loudness (gas): −1.6 LU in speech, −0.7 LU in gaps.
Guard 15 is cleaner still but ducks the music more (31 % of samples dipped vs 20 %) → 12 chosen; revisit with listening/retention data.

Mastering finding (not fixed): loudnorm is in *dynamic* mode on every mix (pre-master PLR 15–19 dB vs ≤ 9.5 dB needed for −11 LUFS /
−1.5 dBTP linear); −14 LUFS target is dynamic too. PRELIM (4×-oversampled look-ahead limiter to the needed ceiling) took 6 dB GR on
25 % of samples and loudnorm still went dynamic (limiting lowered I). → RND.md backlog: explicit comp + limiter chain, then linear gain.
