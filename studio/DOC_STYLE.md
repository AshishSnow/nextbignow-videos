# DOC look — documentary kinetic edit (from the two reference reels, 26 Nov 2026)

## What the references do (measured)
- 16:9, 73–78 s, ~190–200 words/min voice, one shot every 0.5–1.1 s (72 and 137 cuts).
- Script formula: "This is the [most X] [person/thing] in [place]. And it's basically [pop-culture comparison]. Its name's ___.
  And the thing that made it ___ is the same thing that ___." -> rule-breaker story -> irony payoff ->
  callback close: "And at this point, that's basically just how ___ works."
- Visual grammar: full-bleed real footage/photos with slow push-ins; film grade (B&W for history, warm color for now), grain, vignette.
- Captions: 1–3 words at a time, white bold grotesk (Helvetica-like) with soft shadow, placed in empty space next to the subject — never a fixed subtitle bar.
- Big words: condensed heavy caps (Helvetica Condensed feel), often tucked BEHIND the subject (depth mask).
- Name label: red box, white condensed caps.
- Devices: date drum/flip counter for years, typewriter text with cursor, highlighter sweep over a document line,
  black tag boxes ("Boring / Conservative"), RGB-split glitch on a key word, tilted photo-print collage, cut-out sticker with white outline + echo trail,
  whip-blur cuts and white flash frames, gallery frame on a white wall for the final callback.
- Sound: whoosh/impact on every cut, typing/flip clicks, low bed.

## Our version (vertical, OMB rules)
- 1080x1920, 30–40 s, medium-fast voice (speed 1.0), no music (low drone + SFX only).
- Only public-domain / CC0 photos (Wikimedia Commons via studio/tools_ref/commons.py: use the ORIGINAL file url, non-standard thumb sizes get 429) — no people's likenesses, no logos, no film clips.
- Fonts: Archivo Condensed Black (big words, name box), Archivo Bold (kinetic captions), Liberation Mono (typewriter). OFL, in studio/fonts/doc.
- Code: studio/doc_kit.py (cover/push-in, film, kword, big_word, name_box, tag_boxes, typewriter, highlight, rgb_split, flip_counter, card, sticker, whip, flash);
  example: projects/fort-knox/info_fk.py.
- Depth tuck: needs a mask of the subject. For a building photo use a hand-measured roofline + color rule for flag/pole.

## v2 (owner frame notes, 26 Nov): what changed
- Grade: faded matte film (blacks lifted ~19/255, whites capped ~236, 38% desaturated, cool shadows) applied to every element via one ColorFilter; halation bloom on highlights; top/bottom bands softly blurred (only the middle sharp); grain + heavy vignette; photo scenes dimmed 20-40%.
- Type: captions small off-white (never pure white), Archivo SemiBold with tight tracking (letters nearly touching), soft dark glow, centred on the subject; hook words spread across the frame in columns over a thin grid; big words = grey "ghost" words in the same tight grotesk.
- Cutting/animation: 3D card spin-in with motion trail, triangle 3-pane split, photo wall with camera push, red wavy ribbons with repeating name, rolodex year card, red 3D word swinging on a pale wall, green-felt investigation board with pins, string and sticky notes.
