# Voice engine lab — 27 Oct 2026 (raw bake-off rows)

Files: post_chain.py (make_vo's shipped chain + optional global stretch), run_ab.sh (Kokoro shipped vs Chatterbox q4). Summary + decision: ../../VOICE.md, ../../RND.md.

```
# lab_20261027
{"file": "vo.wav", "rtf": null, "utmos": 4.474, "utmos_line": 4.43, "utmos_line_min": 4.38, "f0_hz": 142.9, "range_st": 18.1, "wpm_speaking": 163.2, "dur_s": 37.6, "asr_wer": 0.011, "asr_bad": []}
{"file": "bake_kokoro_dry.wav", "rtf": 0.49, "utmos": 4.52, "utmos_line": 4.473, "utmos_line_min": 4.43, "f0_hz": 133.6, "range_st": 12.5, "wpm_speaking": 167.6, "dur_s": 36.7, "asr_wer": 0.011, "asr_bad": []}
{"file": "bake_cb_flat.wav", "rtf": 12.5, "utmos": 4.517, "utmos_line": 4.461, "utmos_line_min": 4.37, "f0_hz": 139.4, "range_st": 13.2, "wpm_speaking": 186.2, "dur_s": 33.5, "asr_wer": 0.0, "asr_bad": []}
{"file": "bake_cb_expr.wav", "rtf": 12.7, "utmos": 4.528, "utmos_line": 4.478, "utmos_line_min": 4.45, "f0_hz": 148.2, "range_st": 16.0, "wpm_speaking": 186.8, "dur_s": 33.4, "asr_wer": 0.0, "asr_bad": []}
{"file": "bake_cb_expr_chain.wav", "rtf": 12.7, "utmos": 4.517, "utmos_line": 4.471, "utmos_line_min": 4.45, "f0_hz": 148.4, "range_st": 16.4, "wpm_speaking": 186.8, "dur_s": 33.4, "asr_wer": 0.0, "asr_bad": []}
{"file": "bake_cb_expr_chain_slow.wav", "rtf": 12.7, "utmos": 4.489, "utmos_line": 4.425, "utmos_line_min": 4.24, "f0_hz": 149.5, "range_st": 15.8, "wpm_speaking": 166.8, "dur_s": 37.4, "asr_wer": 0.0, "asr_bad": []}
{"file": "bake_kokoro_dry_chain.wav", "rtf": 0.49, "utmos": 4.513, "utmos_line": 4.462, "utmos_line_min": 4.41, "f0_hz": 133.0, "range_st": 12.5, "wpm_speaking": 167.6, "dur_s": 36.7, "asr_wer": 0.011, "asr_bad": []}
{"file": "bake_cb_slowref.wav", "rtf": 12.94, "utmos": 4.542, "utmos_line": 4.49, "utmos_line_min": 4.45, "f0_hz": 140.8, "range_st": 16.4, "wpm_speaking": 165.5, "dur_s": 37.1, "asr_wer": 0.011, "asr_bad": []}
{"file": "bake_cb_slowref_chain.wav", "rtf": 12.94, "utmos": 4.531, "utmos_line": 4.451, "utmos_line_min": 4.24, "f0_hz": 141.0, "range_st": 16.4, "wpm_speaking": 165.5, "dur_s": 37.1, "asr_wer": 0.011, "asr_bad": []}
{"file": "bake_cb_slowref_q4.wav", "rtf": 1.84, "utmos": 4.544, "utmos_line": 4.494, "utmos_line_min": 4.44, "f0_hz": 142.2, "range_st": 17.0, "wpm_speaking": 168.8, "dur_s": 36.5, "asr_wer": 0.011, "asr_bad": []}
{"file": "vo.wav", "rtf": null, "utmos": 4.474, "utmos_line": 4.43, "utmos_line_min": 4.38, "f0_hz": 142.9, "range_st": 18.1, "q_rise_st": 2.2, "low_fall_st": -5.5, "wpm_speaking": 163.2, "dur_s": 37.6, "asr_wer": 0.011, "asr_bad": []}
# lab_20261027b
{"file": "vo.wav", "rtf": null, "utmos": 4.257, "utmos_line": 4.38, "utmos_line_min": 4.19, "f0_hz": 141.4, "range_st": 18.3, "wpm_speaking": 176.1, "dur_s": 42.1, "asr_wer": 0.0, "asr_bad": []}
{"file": "bake_cbq4.wav", "rtf": 1.81, "utmos": 4.297, "utmos_line": 4.455, "utmos_line_min": 4.35, "f0_hz": 139.7, "range_st": 17.2, "wpm_speaking": 168.1, "dur_s": 43.9, "asr_wer": 0.0, "asr_bad": []}
{"file": "bake_cbq4_chain.wav", "rtf": 1.81, "utmos": 4.336, "utmos_line": 4.459, "utmos_line_min": 4.39, "f0_hz": 140.0, "range_st": 17.2, "wpm_speaking": 168.1, "dur_s": 43.9, "asr_wer": 0.0, "asr_bad": []}
{"file": "vo.wav", "rtf": null, "utmos": 4.257, "utmos_line": 4.38, "utmos_line_min": 4.19, "f0_hz": 141.4, "range_st": 18.3, "q_rise_st": null, "low_fall_st": -4.2, "wpm_speaking": 176.1, "dur_s": 42.1, "asr_wer": 0.0, "asr_bad": []}
{"file": "bake_cbq4_chain.wav", "rtf": 1.81, "utmos": 4.336, "utmos_line": 4.459, "utmos_line_min": 4.39, "f0_hz": 140.0, "range_st": 17.2, "q_rise_st": null, "low_fall_st": -2.5, "wpm_speaking": 168.1, "dur_s": 43.9, "asr_wer": 0.0, "asr_bad": []}
# lab_20261027c
{"file": "vo.wav", "rtf": null, "utmos": 4.375, "utmos_line": 4.424, "utmos_line_min": 4.38, "f0_hz": 138.7, "range_st": 18.4, "wpm_speaking": 175.7, "dur_s": 91.6, "asr_wer": 0.004, "asr_bad": []}
{"file": "bake_cbq4.wav", "rtf": 1.84, "utmos": 4.533, "utmos_line": 4.506, "utmos_line_min": 4.47, "f0_hz": 145.4, "range_st": 16.5, "wpm_speaking": 176.6, "dur_s": 91.2, "asr_wer": 0.008, "asr_bad": []}
{"file": "bake_cbq4_chain.wav", "rtf": 1.84, "utmos": 4.519, "utmos_line": 4.484, "utmos_line_min": 4.43, "f0_hz": 145.5, "range_st": 16.3, "wpm_speaking": 176.6, "dur_s": 91.2, "asr_wer": 0.008, "asr_bad": []}
{"file": "vo.wav", "rtf": null, "utmos": 4.375, "utmos_line": 4.424, "utmos_line_min": 4.38, "f0_hz": 138.7, "range_st": 18.4, "q_rise_st": -2.9, "low_fall_st": -7.2, "wpm_speaking": 175.7, "dur_s": 91.6, "asr_wer": 0.004, "asr_bad": []}
{"file": "bake_cbq4_chain.wav", "rtf": 1.84, "utmos": 4.519, "utmos_line": 4.484, "utmos_line_min": 4.43, "f0_hz": 145.5, "range_st": 16.3, "q_rise_st": -7.2, "low_fall_st": -0.2, "wpm_speaking": 176.6, "dur_s": 91.2, "asr_wer": 0.008, "asr_bad": []}
# lab_20261027d
{"file": "vo.wav", "rtf": null, "utmos": 4.34, "utmos_line": 4.405, "utmos_line_min": 4.31, "f0_hz": 139.3, "range_st": 17.1, "wpm_speaking": 176.4, "dur_s": 82.6, "asr_wer": 0.037, "asr_bad": [["i1", "Do you know Costco sells a hot dog and a soda for just$1.50?"], ["e1", "So that$1.50 hot dog isn't really food. It's an ad for the card."]]}
{"file": "bake_cbq4.wav", "rtf": 1.87, "utmos": 4.523, "utmos_line": 4.487, "utmos_line_min": 4.31, "f0_hz": 143.6, "range_st": 16.4, "wpm_speaking": 173.6, "dur_s": 83.8, "asr_wer": 0.009, "asr_bad": []}
{"file": "bake_cbq4_chain.wav", "rtf": 1.87, "utmos": 4.471, "utmos_line": 4.468, "utmos_line_min": 4.22, "f0_hz": 144.2, "range_st": 16.3, "wpm_speaking": 173.6, "dur_s": 83.8, "asr_wer": 0.023, "asr_bad": [["i1", "Do you know Costco sells a hot dog and a soda for just$1.50?"]]}
{"file": "vo.wav", "rtf": null, "utmos": 4.34, "utmos_line": 4.405, "utmos_line_min": 4.31, "f0_hz": 139.3, "range_st": 17.1, "q_rise_st": -3.5, "low_fall_st": -5.2, "wpm_speaking": 176.4, "dur_s": 82.6, "asr_wer": 0.037, "asr_bad": [["i1", "Do you know Costco sells a hot dog and a soda for just$1.50?"], ["e1", "So that$1.50 hot dog isn't really food. It's an ad for the card."]]}
{"file": "bake_cbq4_chain.wav", "rtf": 1.87, "utmos": 4.471, "utmos_line": 4.468, "utmos_line_min": 4.22, "f0_hz": 144.2, "range_st": 16.3, "q_rise_st": -2.3, "low_fall_st": -2.3, "wpm_speaking": 173.6, "dur_s": 83.8, "asr_wer": 0.023, "asr_bad": [["i1", "Do you know Costco sells a hot dog and a soda for just$1.50?"]]}
# e2e
{"file": "vo.wav", "rtf": null, "utmos": 4.534, "utmos_line": 4.479, "utmos_line_min": 4.36, "f0_hz": 143.2, "range_st": 17.1, "wpm_speaking": 168.4, "dur_s": 36.5, "asr_wer": 0.011, "asr_bad": []}
{"file": "vo.wav", "rtf": null, "utmos": 4.534, "utmos_line": 4.479, "utmos_line_min": 4.36, "f0_hz": 143.2, "range_st": 17.1, "q_rise_st": -1.1, "low_fall_st": -2.3, "wpm_speaking": 168.4, "dur_s": 36.5, "asr_wer": 0.011, "asr_bad": []}
```
