# Narrator voices (synthetic only)
- `narrator_slow_ref24k.wav` — 11 s reference read by **our own Kokoro narrator** (am_michael .5 / am_eric .3 / am_fenrir .2,
  SPD 0.78, make_vo PSOLA melody), text: "Have you ever wondered where the money really comes from? Most companies hide it in
  plain sight. And once you see it… you can't unsee it." No real person's voice is involved.
- `narrator_slow.cbcond.npz` — Chatterbox-Turbo speaker conditioning computed from that clip (so runs don't need the 1 GB speech encoder).
Rebuild: `python3 -c "import sys; sys.path.insert(0,'$STUDIO/lib'); import cb_turbo; cb_turbo.Turbo('narrator_slow_ref24k.wav')"` (needs speech_encoder.onnx).
- `narrator_flat_ref24k.wav` — 11 s of the same Kokoro narrator **without** PSOLA (SPD 0.88, Starbucks lines i1–i3), 24 kHz.
  As a Chatterbox reference it gives a calmer, flatter take that leaves room for a light PSOLA layer (hybrid test, 27 Oct, RND.md).
- `narrator_brisk_ref24k.wav` + `narrator_brisk.cbcond.npz` (6 Nov 2026, default): the same Kokoro narrator read faster and with a wider melody (SPD 0.92, EXS 1.3, same three sentences). Gives Chatterbox ~175 wpm instead of ~150 and +2.4 st of range. Synthetic only.
- `narrator_hype_ref24k.wav` + `narrator_hype.cbcond.npz` (8 Nov 2026, owner: "improve voice"): the same Kokoro narrator read at SPD 0.98, EXS 1.6 on an excited
  3-line text ("Wait, you've never heard this story? Okay. This is wild!" …). A/B on 6 Michelin lines vs brisk: UTMOS 4.462 vs ~4.45,
  pitch range 20.2 vs 18.5 st, ~152–160 wpm. Full episode comped from 3 takes: 4.503 (min 4.39), 20.4 st. Synthetic only. Use CBV=narrator_hype.
  (Built with speech_encoder.onnx from ResembleAI/chatterbox-turbo-ONNX, downloaded 8 Nov to $STUDIO/models/cbturbo.)
