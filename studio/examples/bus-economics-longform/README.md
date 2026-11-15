# Bus economics long-form (16:9, vintage comic, 7:24)
OopsMyBusiness long-form. Posted to YouTube via Metricool post 429019020 (16 Nov 2026 19:30 IST).
- Landscape: NBN_ORIENT=land (1920x1080). Engine: pet-rock-comic modules (engine/comickit/toon/audiokit).
- Long VO (7+ min) OOMs make_vo on 8 GB: split script into two half-projects (p1/p2), join vo.wav.
- Render in two frame ranges in parallel; concat. To patch a scene: re-render its frame range, cut the
  rest with single-output trims (multi-trim filter_complex OOMs), concat with -c copy.
- Hosting: raw GitHub caps at 100 MB, releases blocked -> 2-pass x264 to ~94 MB for the post; master kept locally.
- QA lesson: never use a black title (KINK) on black outline; keep doc stamps off the body text.
