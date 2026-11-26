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

## v4: measured from the reference audio (Whisper transcripts in /home/claude/ref/*.txt)
- **Speech pace: 185-198 words per minute** with almost no gaps (max pause 0.5-0.8 s). Ours was ~150 wpm, so v4 runs at ~181 wpm with tight 0.05-0.14 s gaps between lines.
- **Cuts land on words**: 69-76 % of cuts fall within 0.15 s of a word onset (137 cuts / 72 s). v4 adds hard 9 % punch-ins on key nouns (`PUNCH` in scenes3.py) plus a transition on every line.
- **Music is loud**: in the gaps between words the level is only ~1.5 dB below the overall mix, i.e. a strong bed. v4 uses a synthesised suspense score (`music.py`: drone, heartbeat, clock tick, risers, sub booms, silence drop) mixed louder with lighter ducking.
- **Script skeleton, identical in both reels:**
  1. "This is the [thing] that [stakes]." (demonstrative + stakes, ~3 s)
  2. "And it's basically [famous comparison]." (Godfather / Tony Stark)
  3. Pop-culture sound bite (film quote) as a pattern interrupt; we can't use film audio, so we use a hard visual/sound hit instead
  4. Name reveal ~9 s: "His name's ___."
  5. **Irony thesis**: "the thing that made him X is the same thing that got him laughed at" / "the same company that made him a billionaire threw him out"
  6. Vivid specifics, each a picture ("bartenders were becoming mortgage brokers")
  7. Turn: "But instead of ___, he did the one thing ___"
  8. Mirrored-phrase irony ("created so it would never need one banker... called one banker")
  9. Time jump: "Fifteen years later..." / "and the exact same thing happened. Same call, same man."
  10. Zoom-out ending that points at the viewer ("built the internet you scroll... the thing quietly watching you do it"). No CTA.

## v5 hook (first 4 s)
- Photo cards fly in from all four sides with a 3D tilt and motion blur, slam into a stack (whoosh + thud each, about 0.2 s apart), bounce slightly, then a "REPAIR RECEIPT" card with ??? fields slides up on top while the others darken, then the camera pushes through the stack into the next shot (zoom blur). Title stays from frame 1; the one-word caption sits between the title and the cards. Code: `hook5()` in scenes4.py.

## v6: type system + holding the viewer (26 Nov)
**Fonts** (OFL, in fonts-docu/):
- **Archivo ExtraCondensed Black** (static instance wght 900 / wdth 62) for hero words. Tall and condensed like the reference's COLLAPSE / SUBPRIME, and it fits big words on a vertical frame.
- **Instrument Serif Italic** for emotional accent words in red or yellow ("been?", "glued", "did.", "with an address."). This serif italic + condensed grotesque contrast is the editorial-documentary look.
- **Courier Prime** typewriter for time jumps and the receipt, replacing DejaVu Mono.
- **Inter Display ExtraBold** stays for the one-word captions and the black label boxes.

**How the video holds the viewer:**
1. **Open loop**: the hook shows a REPAIR RECEIPT with red ??? fields. The viewer wants them filled.
2. **Payoff in steps**: SAMPLES 10 and COATS 4-5 get stamped VERIFIED mid-video; WHERE = ITALY + CROATIA closes the loop at "Same ship. Different repair shops."
3. **One metaphor end to end**: receipts (hook → car analogy → "glued to the hull" → "a receipt with an address" → "its receipts did"). No metaphor switching.
4. **A twist line every 3-4 s**: "Except…", "And while it was sticky…", "So every coat…".
5. **Something on screen moves on every key noun** (punch-in / slam / stamp / type), and a sound accompanies each one.

## Reference 3: "Sol" launch film (104 s, 26 Nov). Manifesto style
Measured: ~95 wpm (half the speed of the power-story reels), 37 pauses over 0.5 s (longest 3.2 s), 62 cuts (one every ~1.7 s), -14 LUFS, quiet ambient bed.
**Words, beat by beat:**
1. Universal premise everyone agrees with: "Everything we make evolves. It's not a choice."
2. Proof as a list of single nouns, one picture each: "Light. Maps. Money. Pokémon. Music. Computers." (nostalgia hit: Charmeleon evolving)
3. Turn to the subject with a question: "And this?" (Mail icon)
4. "Oh, it evolved. Constantly." Then a verb list: crossed the world, held attachments, reached your pocket, sorted itself, defended itself.
5. Two-halves contrast, the spine of the film: "made mail better at arriving. Not one in 50 years made getting started any easier."
6. Personify the object so it hurts: "Your inbox watches your work arrive all day… It has everything it needs. And it waits for you anyway."
7. Silence, then "Until now." (beat drop, logo)
8. Fragment triplets: "The doc. Created. The time. Found. The reply. Drafted."
9. Trust line: "All of it ready. None of it sent. That part is still you."
10. Callback close that repeats the spine: "Half your inbox took 50 years. The other half starts today."
**Emotion arc:** wonder/nostalgia → recognition ("that's my inbox") → quiet frustration → relief ("Until now") → trust → hope.
**Styling:** black screen with small centred white words appearing one by one in silence; huge white grotesque words over archival photos (B&W past → colour present); map collages sliding; pixel-game UI insert; VHS/CRT footage with scanlines and yellow film subtitles; defocused UI close-ups; then a switch to bright white light-mode with an iridescent pastel glow ring (= "the new thing"); a 3D museum of pedestals as the evolution metaphor. Visual arc = emotional arc: dark, gritty past → bright, clean future.
