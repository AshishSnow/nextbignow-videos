# Narrator voices (synthetic only)
- `narrator_slow_ref24k.wav` — 11 s reference read by **our own Kokoro narrator** (am_michael .5 / am_eric .3 / am_fenrir .2,
  SPD 0.78, make_vo PSOLA melody), text: "Have you ever wondered where the money really comes from? Most companies hide it in
  plain sight. And once you see it… you can't unsee it." No real person's voice is involved.
- `narrator_slow.cbcond.npz` — Chatterbox-Turbo speaker conditioning computed from that clip (so runs don't need the 1 GB speech encoder).
Rebuild: `python3 -c "import sys; sys.path.insert(0,'$STUDIO/lib'); import cb_turbo; cb_turbo.Turbo('narrator_slow_ref24k.wav')"` (needs speech_encoder.onnx).
- `narrator_flat_ref24k.wav` — 11 s of the same Kokoro narrator **without** PSOLA (SPD 0.88, Starbucks lines i1–i3), 24 kHz.
  As a Chatterbox reference it gives a calmer, flatter take that leaves room for a light PSOLA layer (hybrid test, 27 Oct, RND.md).
