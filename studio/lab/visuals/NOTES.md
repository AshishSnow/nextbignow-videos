# Visuals lab — R&D run 7 (28 Oct 2026)

- `first3s_features.py` — first-3-second features of finished MP4s (frame-0 detail, caption timing, motion, cuts, colourfulness, brightness,
  audio onset). `first3s_posted.csv` = the 14 posted files (from the `omb-*` hosting branches). Result vs IG 3-s rate (n = 9): no feature
  |rho| > 0.27 (0.58 without Duolingo, none p < 0.1) → PERFORMANCE insight Q. Rerun when n ≥ 15:
  `python3 first3s_features.py *.mp4 > f.csv`, then Spearman vs IGRE28.
- `layout_before_after.json` — `tools/layout_check.py` summaries + violating frames for all 15 examples (fake timings, step 3 s),
  old template (before) vs safe-area template (after). Totals 51 → 17 frames with captions in a UI zone, first 3 s 16 → 2.
- Measured UI zones (third-party, Sep 2026): IG organic top 250 / bottom 319 / left 86 / right 119; Meta Reels ads 14 % / 35 % / 6 %;
  YT Shorts ~288 / ~288 (+ long titles) / right ~140. No official organic numbers exist (Reap, 7 Sep 2026).
  Sources: https://adchecklab.com/articles/instagram-reels-safe-zone-template , https://www.clipspeed.ai/blog/youtube-shorts-size.html ,
  https://reap.video/blog/short-form-video-safe-zones
