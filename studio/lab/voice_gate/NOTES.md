# Per-line prosody gate for Kokoro — R&D 27 Oct 2026 (run 3)

Question: where do Kokoro's weak lines (worst line 3.9–4.1 UTMOS on gas / airline) come from, and can we fix them without flattening?
Files: `perline.py` (per-line UTMOS of any VO), `base.sh`/`base2.sh` (make_vo on an example + per-line scores of vo_flat and vo.wav),
`run_variants.sh` (the variant runner used here), `make_vo_pg.py` (the lab version that became template/scripts/make_vo.py).

## Diagnosis (gas station script, default blend)
Per-line UTMOS of the **flat Kokoro take** (before PSOLA): every line 4.43–4.52. After PSOLA (vo_raw): c1 3.93, b2 4.26, a2 4.33.
After the EQ/clean/room chain (vo.wav): c1 3.98, d2 4.23. → The weak lines are made by **our own PSOLA prosody**, not by Kokoro.
So the first idea (Kokoro retakes at other speeds, like take_picker for Chatterbox) would not have helped; dropped before building it.
Background: PSOLA is near-transparent for moderate shifts; a 2025 vocoder study treats ±6 st as the safe range for TTS pitch moves
(arXiv 2512.16519). Our moves stack range ×1.45 + per-line base + stress bumps (+2.4 st) + endings, clipped at −12/+13 st.

## Fix: per-line gate (PGATE)
Render PSOLA; score each line vs its flat take; a line that lost > PGATE is re-rendered at 0.6 (then 0.3) strength — pitch moves,
stress stretch scaled; loudness lift kept. Keep the strongest strength within the gate, else the best-scoring one.

## Results (shipped vo.wav; UTMOS whole / per-line mean (min line), range st, low_fall st, q_rise st)
| Script | A: default (template before) | PGATE 0.15 | PGATE 0.15 + clip −7/+8 st | PGATE 0.15 + puck .1 blend |
|---|---|---|---|---|
| Gas (79 s) | 4.234 / 4.379 (3.98), 18.1, −4.8, +1.7 | 4.373 / **4.411 (4.25)**, 17.8, −4.8, +1.9 — a2, c1 → 0.6 | 4.408 / 4.405 (4.29), **15.0**, −4.7 | 4.452 / 4.416 (4.31), 18.1, −4.6 — i1, c1 → 0.6 |
| Duolingo (91.5 s) | 4.386 / 4.423 (4.37), 18.4, −6.8, −2.9 | 4.421 / 4.421 (4.33), 18.3, −6.6, −2.8 — a4 → 0.6 | (stopped: clip lost range) | 4.193 / 4.426 (4.37), 18.1, −6.9, −3.4 |
| Airline (100 s) | 4.394 / 4.390 (4.05), 18.4, −5.3 | 4.402 / **4.406 (4.25)**, 18.2, −5.0 — c1 → 0.6 | – | 4.407 / 4.407 (4.15), 18.0, −5.1 — none gated |
ASR: 0 bad lines everywhere. Noise: re-running A on the same cached flat take gave 4.237 / 4.380 (c1 3.92 vs 3.98) → single lines move ±0.06.
Cost: +~40 s on a 100 s VO (flat per-line scoring + one extra PSOLA render).

## Decisions
- **PGATE=0.15 is the template default** (worst line +0.20…+0.27 on 2 of 3 scripts, mean +0.016…+0.032, range −0.1…−0.3 st, endings kept).
- Global clip −7/+8 st: not adopted (range fell to 15.0 st, no gain over the gate) — the gate fixes only the lines that need it.
- puck 0.1 blend: per-line mean = default within ±0.005 on gas/duo/airline (+0.005, +0.005, +0.001), worst line better on gas,
  worse on airline (a3 4.15 — a chain drop, not PSOLA) → not the default; still a fine per-video choice.
- Gate misses: Duolingo a4 scored better on raw at 0.6 but worse after the chain (4.38 → 4.33); airline a3 drops in the chain, not
  PSOLA. Next: gate on the chained line, or find what in the chain (de-esser? room) hurts short lines.
