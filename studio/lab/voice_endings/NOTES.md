# Hybrid endings lab — 27 Oct 2026 (R&D run 2)
Scripts: run.sh (Kokoro shipped vs Chatterbox q4 vs Chatterbox + end_contour, one example script), variants.sh (re-run only the
end_contour variants on an existing lab project). The algorithm now lives in ../../lib/end_contour.py and runs inside make_vo.py
when ENGINE=chatterbox. Summary table + lessons: ../../VOICE.md "Hybrid endings"; decision: ../../RND.md log.

Raw rows (UTMOS whole / per-line mean / min, low_fall st):
gas     Kokoro 4.317/4.399/4.13 −4.8 | CB 4.522/4.480/4.40 −1.3 | v1 −3/+3 4.518/4.475 −1.2 | v1 −5/+4.5 4.517/4.477 −1.8
        v2 (land early) −4/+5 4.304/4.456/4.16 −1.3 | v3 (+uptalk cap) −3 4.488/4.476 −1.3, −5 4.474/4.462/4.32 −1.4
        v4 (+85 Hz floor, ≥0.5 s window) −4 4.511/4.472/4.40 −4.3 | v5 (+gate .03) −4 4.513/4.476/4.40 −4.0 (b1 skipped −0.16)
duo     Kokoro 4.382/4.428/4.38 −7.1 | CB 4.264/4.458/3.91 −0.2 | v1 −3/+3 4.258/4.438/3.89 −0.8 | −5/+4.5 4.255/4.437/3.90 −1.0
        v4 −4 (no gate) 4.242/4.439/3.73 −3.0 | gate .03 4.256/4.456 −1.6 | gate .05 4.253/4.449/3.91 −1.7
costco  Kokoro 4.321/4.402/4.30 −4.9 | CB 4.501/4.474/4.43 −1.0 | v5 −4 gate .05 4.380/4.468/4.41 −3.5 (c2, e1 skipped −0.27)
Per-line low ends on Duolingo (st vs line median): Kokoro −10…−4, CB −2.5…+5.3, CB+ends −6.0…−2.2 (a2 +5.3 skipped).
Kokoro+PSOLA routinely ends at 76–81 Hz; Chatterbox+PSOLA below ~85 Hz creaks and confuses the pitch tracker (octave jumps).
