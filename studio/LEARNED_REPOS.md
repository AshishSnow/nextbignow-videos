# Lessons from the owner's shared repos (27 Nov 2026)
Sources: humanizer (MIT), ghost-editor (reel editor skill), Motion Video Director skill, Handy (offline Whisper dictation app).

## Script writing (humanizer)
- AI tells to cut from every script: staged openers ("Let's go back to the beginning", "Here's the thing"), a one-line closer after every section, "not X but Y" contrasts used for weight instead of meaning, forced triads, inflated claims ("pivotal", "game-changing"), sales language.
- Every line must add a fact the viewer doesn't have yet. Keep ONE mirror line per video (the payoff), not one per section.
- Triads only when there really are three things (a real list of jobs is fine).

## Editing grammar (ghost-editor + Motion Video Director)
- Long-form documentary recipe (16:9): every sentence = a new visual idea, 1–2 s per idea in hooks, 2–5 s per idea in explainers; vary rhythm (fast, fast, hold). Hits/whooshes land on the FIRST frame of a new scene, not on every word.
- Kinetic doc / archive look: black-and-white archive photos as prints and polaroids, one accent colour for emphasis, one big word + small words, punch lines on their own page. Matches our PAPER look with a series accent.
- Data Story: when a line carries a number, draw it (chart/counter) and show the source as a small caption. Only sourced numbers.
- On-screen text ≤ 6–8 words; reading time ≈ 0.3 s/word + 0.5 s. One focal point per moment.
- Motion: entrances 200–500 ms ease-out, exits faster, stagger 40–80 ms, overshoot 5–10 %. Never linear.
- Intensity by type: educational/case study = medium (3); calm music optional; no effects covering content.
- Inserts must match the plate: same warmth/saturation (we grade every photo warm or sepia), no random stock strangers, keep the subject (the person) on screen often.
- Cut-outs: portrait matting (BiRefNet portrait best; rembg u2net/u2netp OK for stills), erode/feather 1–2 px to avoid halos, white die-cut border for the paper look. Cut-out of the person also makes the YouTube thumbnail (1280×720) and the Reels cover (1080×1920).
- A meme or sound gag lands ON or AFTER the punchline, never before.
- QA every render: duration == voice, no text in platform UI zones, captions never over faces, loudness −14 LUFS.

## Tools
- Handy: free offline speech-to-text desktop app (Whisper). Useful for the owner to dictate topic ideas/notes; our pipeline already uses faster-whisper for alignment and transcript checks.
