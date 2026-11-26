# "Docu kinetic" style — teardown of the 2 reference reels + how we build it

Refs: Jamie Dimon reel (73 s) and Palmer Luckey / PayPal-mafia reel (78 s). Both 1276x718 (16:9), 24-25 fps, voice + light score, -14 to -18 LUFS.

## What makes it work
| Element | What the ref does | Our version (docu/scenes.py) |
|---|---|---|
| Pace | 106 cuts in 73 s (one every 0.7 s); 63 cuts in 78 s (1.2 s). A new picture for almost every phrase. | 2-4 shots per VO line, Ken-Burns push on every shot (`shot()`). |
| Footage | 90% real photos/footage, full-bleed, film-graded (low saturation, teal shadows, warm highlights, grain, vignette). | Wikimedia Commons photos, graded in `graded()`, grain + vignette in `finish()`. |
| Captions | ONE word at a time, small (~3% of height), white, centred, soft shadow. Never a subtitle block. | `capword()` Inter Medium 50 px. |
| Hero words | 3-5 words per video go huge: condensed bold caps (COLLAPSE in red, GOVERNMENT, EARTH, HOUSING PRICES). Pop in from 125% in ~0.2 s. | `hero()` Anton, white/red/yellow. |
| Paper interludes | Off-white page, words spread far apart, one small photo card in the middle ("he's [photo] basically"). Breaks the dark rhythm. | `paper_bg()` + `card()` + `word()`. |
| Typewriter | Mono font, typed char by char, blinking cursor, on black or dimmed footage ("15 years later...|", "Got bailed out"). Used for time jumps & suspense. | `typewriter()` DejaVu Sans Mono. |
| Name/location strap | Solid red bar wipes in, white condensed caps (JAMIE DIMON). | `tag()`. |
| Data devices | Flip-clock years (1997/2004/2007), document with yellow marker sweep, PayPal receipt highlight, newspaper clipping collage. | `flip_counter()`, `highlight_doc()`. |
| Split screens / grids | 2-4 photos tiled with thin gutters; tilted 3D photo walls. | half/half split with paper gutter. |
| Transitions | Whip-pan blur, RGB glitch + slice offsets, white flash, zoom-through. | `whip()`, `glitch()`, flash in `trans()`. |
| Metaphor B-roll | Pop-culture analogy shots (Godfather, Tony Stark), chess pieces, Newton's cradle. | Use only royalty-free / public-domain stand-ins; no film clips or public-figure photos. |
| Sound | VO-led; whooshes on whips, clicks on type, risers into reveals. | Mixkit whooshes + synth type clicks; no music (page rule). |

## Adapting to our page (vertical IG reel)
- 1080x1920, keep the safe zones (nothing key in top 250 / bottom 420 / right 120).
- Frame 1 still carries our 2-line text hook (page rule), styled as hero words over the first photo.
- Captions sit at y≈1300 (centre-low) so they never hit the IG caption bar.
- Our NEXT/BIG/NOW badge top-right; end card is paper + typewriter CTA.
- 30-35 s, share line around 55-65 %.
