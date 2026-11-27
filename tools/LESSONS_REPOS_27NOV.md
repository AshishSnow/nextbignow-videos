# What we take from the 5 repos Ashish shared (27 Nov 2026)

## OpenMontage (agentic video production system)
- **documentary-montage pipeline**: retrieval-first. Build a corpus of REAL footage from open archives (Archive.org Prelinger/NASA collections, free stock), fill slot descriptions ("concrete noun + adjective" queries, 2-3 per slot), grade mixed-era clips to one look, music-synced edit, and close on ONE philosophical end-tag line.
- **long-form skill** (our new 5-6 min YouTube videos):
  - Hook + stakes + preview complete by 0:30; the first frame matches the thumbnail promise.
  - First real payoff before 2:00; pattern interrupt at about 1:45. A "burst" of 5-10 quick cuts every 2-3 min.
  - Minor interrupt every 20-30 s (graphic, SFX, direct address); major every 60-90 s (look change, music shift).
  - Re-hook at about 2:00 and every 3-4 min ("but that's not even the strange part..."). Chapters of 2-4 min, ~150 wpm.
  - Second exodus at 55-65%: resolve an open loop there.
  - Last 20 s is the end screen.
- Retention targets for 5-10 min: 45% is good, 60% is excellent. Natural narration matters a lot (robotic TTS loses viewers early).

## Motion Video Director skill
- Hook devices: bold claim, result-first, visual surprise in frame 1. Structure: Hook -> Problem -> Solution -> Proof -> CTA.
- One idea per shot. On-screen text <= 6-8 words. Reading time ~0.3 s/word + 0.5 s.
- Every sentence = a new visual world; cut on the first syllable.
- One accent colour carries all emphasis; keywords get treatment, filler stays quiet. 2D world, 3D only at peaks.
- SFX mark CHANGES (new world, reveal), not every word. Silence around the big hit sells it.
- Loudness -14 LUFS / -1.5 dBTP.
- Motion intensity by type: explainers = level 3 (highlights, arrows, diagrams), not reel-level flashes everywhere.

## ghost-editor (talking-head reel editor)
- B-roll rule: fewer inserts, each one SHOWING its line. If nothing shows the line, leave it bare rather than use loose footage. Stock stills in a frame/card often beat many video cutaways.
- Keep cutaways conformed to the main plate's look; an approval sheet (a frame at every cut) before the full render.
- Memes and reactions land ON or after the punchline, never before.

## humanizer (remove AI tells from scripts)
Check every script for:
- **"Not X but Y" contrasts**, which add weight without a claim. Our "Not a fender bender. A hit ten times faster than a bullet." is borderline; keep only when the reader actually holds X.
- **One-line closers and dramatic fragments** ("Every. single. time.", "Read that again").
- **Sayings that sound deep** ("the real question is...").
- **Staged run-ups** ("Here's the crazy part", "Here's what nobody tells you").
- **Forced triads.**

Rule: every sentence must add a new fact. Vary sentence length. Keep real numbers and names.

## Handy (offline speech-to-text, Whisper/Parakeet)
Same idea as our faster-whisper check: transcribe every voice line and diff against the script. Already in vo_cb.py.

## Sources we can actually reach from this workspace
- archive.org: public-domain archival film, Prelinger, NASA collections. Real footage is possible.
- assets.mixkit.co: free stock video and SFX.
- freesound.org: SFX.
- upload.wikimedia.org: reachable.
- Blocked: Pexels, images.nasa.gov, YouTube.
- Rule: no photos of real public figures pulled from the web. Show them as silhouettes or stylised figures with name tags, or use photos Ashish supplies.
