# Ep 26 — brain freeze, REAL 3D (Zack D Films style test, owner request 6 Nov 2026 19:35 IST)
Owner: "Create a video and post now, Zack D Films style, make the front image attractive, improve voice and script."

Pipeline (new, no Blender needed): three.js 0.170 scene (`scene.html`) rendered headless in Playwright Chromium with
SwiftShader WebGL (`render.js`, 2 workers, ~2.2 s/frame for both together at 1080x1920 incl. bloom) -> JPEG frames -> ffmpeg.
- Setup: `npm i three@0.170.0` in the folder; models from the three.js repo (raw.githubusercontent.com/mrdoob/three.js/dev/examples/models/gltf/):
  LeePerrySmith/LeePerrySmith.glb + Map-COL.jpg + Map-SPEC.jpg + Infinite-Level_02_Tangent_SmoothUV.jpg (head scan by Lee Perry-Smith,
  Infinite Realities, **CC BY 3.0 — credit it in every caption**); font = Anton woff from studio/fonts (TTFLoader). Serve with `python3 -m http.server 8765`.
- Look: realistic scanned head + procedural t-shirt; sunny park backdrop; x-ray mode = fresnel shell (additive) + procedural anatomy
  (displaced-sphere brain, palate dome, tongue, branching blood-vessel tubes rebuilt per frame with animated radius, trigeminal nerve tube
  with travelling pulses, frost particles, radial glow sprites); UnrealBloom; HTML overlay for medical labels with leader lines + key-word captions;
  3D extruded title "BRAIN / FREEZE" behind the head for the cover frame.
- Timeline = word times from the VO (`tl.json`, built from work/align.json); `window.renderAt(t)`.
Voice: Chatterbox-Turbo (ENGINE=chatterbox) conditioned on FreshNestHub's OWN synthetic reference (`fnh_warm_ref24k.wav` = our Kokoro M2
narrator reading 3 casual lines at SPD 0.95 / EXS 1.2; `.cbcond.npz` precomputed) -> distinct from the OopsMyBusiness narrator_brisk.
Same-script A/B: Chatterbox 4.477 whole / chunk20 4.470 / line mean 4.409 / 13.6 st vs Kokoro M2 4.395 / 4.475 / 4.450 / 15.5 st; both ASR clean.
Chosen for the natural, conversational delivery (Zack-style narration); the pitch range is below the 15 st gate — next: a livelier reference.
Mix: `mix3d.py` (procedural 84 bpm lo-fi synth bed ducked under the VO, low-pass + drone during the nerve alarm, music stops before the
punchline, SFX on every beat) -> -12 LUFS / -1.4 dBTP.
Lessons: SwiftShader cost is all in the screenshot (GPU work flushes there); first frame compiles shaders (~25 s); bloom adds ~20 %;
physical skin with sheen + low bloom threshold washed everything out (exposure 0.88, no sheen, bloom threshold 0.9 fixed it).
