# SCRIPT_FEEL.md: make a script *feel* like a story, not a fact list (owner, 18 Nov 2026)

The owner's note on 18 Nov: "Improve script. Understand how to write a script that has feel. Do more research."
His reference reel showed someone directing Claude like a film director. The director:
- writes a precise brief: the look, the one moment that matters, and what to build up to;
- asks for style frames first, before any animation;
- gives exact, physical feedback ("thin line, you can barely see it", "light in rain has no edges").

WRITING.md covers *sentences*, so a script sounds human. This file covers *shape*, so the script pulls the viewer to the end.
Both apply to every script.

## Diagnosis of our scripts
Up to Crocs, our scripts were correct and clean, but they read like "and then" lists:
> stock was $70, and then $1, and then lost $185M, and then tried shoes, and then cut, and then charms, and then $3.3B.

You could reorder most of those lines and nothing would break. That's the "list vs story" test failing: nothing causes the next beat.
The hook also often answered its own question in line 2, so there was no reason to stay.

## The 9 rules
1. **But / Therefore, never "and then".** Every beat must be caused by the one before it ("so" / "therefore") or
   blocked by something ("but"). If two lines could swap places, rewrite them or cut one.
   Source: Trey Parker and Matt Stone's writers' room rule, via David Perell; Tony Zhou on No Film School.
2. **One big question (the macro loop), opened in the first 3 s, closed in the last 5 s.** Line 2 still gives the main point
   (owner rule). But it gives the *what* and keeps the *how* or the twist open: "Short version: Crocs stopped fixing the ugly clog. But first,
   it almost died." Only one big question; two in the hook confuse people. Source: TokCount, open-loop strategy; Social Media Examiner.
3. **A small question every 8–15 s (micro loops).** Open a small question, answer it fast, open the next one:
   "Did it work?", "And the clog?", "The catch?". The middle sags without them, especially past 45 s. Source: TokCount; Kineclip.
4. **A protagonist with a goal and an obstacle.** The company (or "you" in the seat) *wants* something specific and something real
   blocks it. Use at least two obstacles, each forcing a decision. Keep obstacles real: viewers notice fake friction.
   Source: VideoToBlog, "cinema story mechanics".
5. **Lead with the strangest true detail.** Ask "what's the one thing here nobody would guess?" and put it in the first 2 lines.
   Example: the charms made more than most shoe brands. Source: Social Media Examiner, "front-load the angle".
6. **Present tense plus a time stamp for the story** ("Twenty oh seven. Crocs stock is almost seventy dollars."). Past tense
   puts the viewer in a museum; present tense puts them in the room. Keep rule 22 of WRITING.md: the time stamp is said out loud.
7. **Picture first (show, don't tell).** Write a SEE line under every voice line: the one image on screen. If the picture
   can say it, cut the words. Cut "tension" words ("shocking", "crazy"); show the number falling instead.
   Source: VideoToBlog, the "no voiceover first" test; our WRITING rule 18.
8. **Build to the big moment, like the beam in the reference reel.** Make the line before the reveal small and quiet,
   then the reveal, then one beat of silence: a 0.5–0.7 s pause in `vo_lines`, with the reveal line short (≤ 8 words).
   One big moment per video.
9. **End on the payoff, then stop.** The last voice line closes the macro loop with a callback to line 2 ("The shoe never
   got prettier. Crocs just stopped apologizing for it."). The CTA is one short question that *continues* the story, not
   "like and follow". Never talk after the payoff. Source: Social Media Examiner; Kineclip, "loop ending".

## Pre-voice checklist (run before showing the owner)
- [ ] Hook = title spoken + the strangest true detail; line 2 = main point with the *how* still open.
- [ ] Swap test: no two adjacent beats could trade places.
- [ ] Count but/so turns: at least 3 in the body.
- [ ] A small question every 8–15 s.
- [ ] Every voice line has a SEE line (the one picture), and no line explains what the picture already shows.
- [ ] One build-up + reveal + pause.
- [ ] Last line calls back to line 2; nothing after the payoff except a ≤ 8-word question.
- [ ] Then WRITING.md (human_check, 130–190 words) and the facts check against SOURCES.md.

## Visual brief (from the reference reel, applied to our pipeline)
Before rendering, write a short **director's brief** per video:
- the look in one line;
- the ONE moment that matters and how the scene builds to it (dim → hit → recover over 8–10 frames, never a one-frame pop);
- where text sits (empty area reserved);
- what is always moving (camera drift, parallax: never fully still).

Then render **3–4 style frames** (`render_X.py still t`) and send them to the owner for a yes/no **before** animating.
Feedback is taken as concrete, physical notes and applied only to what was named ("change only the beam, don't touch anything else").

## Worked example: Crocs, before → after (same facts, from SOURCES.md)

BEFORE (as shipped 18 Nov, "and then" shape):
How the ugliest shoe came back from one dollar. True story. / Short answer: Crocs stopped hiding the ugly clog, and made it the whole
business. / In 2007, Crocs stock hit almost $70. One year later? About $1. / In 2008, the company lost $185M. / It had tried everything…

AFTER (but/therefore, one loop, picture per line):

| id | voice | SEE |
|---|---|---|
| h1 | How the ugliest shoe came back from one dollar. True story. | clog cut-out drops onto a $1 price tag; title |
| h2 | Short version: Crocs stopped fixing the ugly clog. But first, it almost died. | clog sticker; a crack runs across the paper |
| a1 | Twenty oh seven. Crocs stock is almost seventy dollars. | line chart climbs to $70, the clog on top |
| a2 | A year later? About one dollar. | chart line falls off a cliff; the clog tumbles with it |
| a3 | The company loses a hundred eighty-five million dollars in one year. | stamp: −$185M, 2008 |
| b1 | It had been making all kinds of shoes. Dress shoes. Golf shoes. Even high heels. | three price tags swing in, one by one |
| b2 | And the clog itself? A joke. | clog alone, small, under a spotlight |
| c1 | So Crocs cuts the extras. Back to one clog. | tags fall away; the clog grows to fill the frame |
| c2 | But it's still the ugly clog. So instead of hiding it, Crocs lets you dress it up. | charms rain into the clog's holes |
| c3 | Little charms called Jibbitz. | charm close-up, snap SFX |
| d1 | Did it work? | (quiet: the scene dims slightly; build-up) |
| d2 | In twenty twenty-four, the charms alone made about two hundred seventy million dollars. | big $271M on a charm-shaped tag (the reveal), 0.6 s pause after |
| d3 | The charms. Not the shoes. | a charm next to the clog, the clog greyed out |
| e1 | Last year, the Crocs brand sold three point three billion dollars worth of shoes. | chart line climbs off the top of the frame |
| z1 | The shoe never got prettier. Crocs just stopped apologizing for it. | the first clog again, now wearing charms (callback) |
| z2 | Would you wear them? Tell me in the comments. | two pills: YES / NO WAY |

What changed:
- 3 "but/so" turns: lost money → *so* cut; cut → *but* still ugly → *so* decorate.
- The macro loop is "how did it come back?", closed by z1.
- Micro loops: "A year later?", "And the clog itself?", "Did it work?".
- One build-up (d1 quiet) → reveal (d2) → pause.
- Present tense with spoken years.
- A callback ending.
- The word count is about the same (~150).

## Sources (researched 18 Nov 2026)
- David Perell, "The But & Therefore Rule" (perell.com); No Film School on Tony Zhou, "Therefore & But instead of And Then" (2015).
- TokCount, "Scripting for retentive attention: the narrative open loop strategy".
- Social Media Examiner, "YouTube Shorts hooks and curiosity loops".
- Kineclip, "How to write viral short-form scripts 2026" (hook–context–payoff–loop, 80–150 words for 30–60 s).
- Subscribr, "Perfect YouTube Short length, structure, hooks" (opening promise → tension → payoff; trim dead ends).
- VideoToBlog, "Steal cinema story principles for retention" (show, intention + obstacle, cause + effect).
- Christy Tucker, "Voice-over scripts: writing style tips"; The MX Group, "How to write for the human ear".
- The owner's reference reel (18 Nov): brief → style frames → precise feedback → animate.
