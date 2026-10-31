# Storyboard — YOUR MOVE · EP 1 · Part 2 (Pepsi jet: the court case). Same look and music family as Part 1 (a variation, not the same cue).
Story kit (`anim_story.py`): `set_view("courtroom")`, `set_front(f, "courtroom", (176, 606, 904, 1004))` to put the judge BEHIND the
bench (judge: `person(f, 540, 930, 1.1, {"base": "lady", "top": (28, 26, 32), "outfit": "coat"}, shadow=False)`), `quote_card`,
`choice_card`, `oops_beat`, `cold_open`, `series_badge`, `jumpjet_el`, `crt_tv_el`, `catalog_el`. Lawyers: `exec` looks. The ad is only
our own cartoon re-staging inside a CRT frame — never real footage. Opinion quotes go on quote cards: "Leonard v. PepsiCo (S.D.N.Y. 1999)".

| Line | Set / shot | Cast + acting | HUD / props / caption | SFX / camera |
|---|---|---|---|---|
| i1 "You mailed Pepsi a check for a fighter jet. Will a judge make them deliver?" | courtroom WIDE, the jet visible through the tall window (dusk) | hero at the table (back view), judge above | `series_badge(f, "PART 2", "EP 1 · THE PEPSI JET")` in frame 1 | gavel echo, slow push |
| i2 "Part two. … seven million points. … ten cents. … seven hundred thousand." | 3 quick beats: CRT with 7,000,000 → a dime → money bags | — | `say("7,000,000 PTS")` → `say("10¢")` → `say("$700,000")` | coin clinks |
| a1 "Here's what really happened. Pepsi moves first." | Pepsi-side lawyers (3 `exec` looks) stride down a corridor | `brow="sus"` | `cold_open(f, "JULY 1996", "NEW YORK", "PEPSI GOES TO COURT")` | footsteps |
| a2 "…owes you nothing. So you sue back." | split: their filing / your filing slam on the table | hero determined | plain "COURT PAPERS" stamps ×2 (no real case captions) | slam + small shake |
| a4 "But watch the ad. … seven hundred million points… just kidding." | CRT CU: our re-staged ad's last frame; the number rolls 7,000,000 → 700,000,000 + "JUST KIDDING" | hero stares | number roll | TV static |
| a5 **"Oops."** (the hero's reaction) | hero turns to camera, CU | smirk | `oops_beat(f, t, t0)` | **Oops sting** |
| a6 "Not an admission, the judge later says. Just a way to head off more lawsuits." | judge CU (behind the bench) | calm | small caption "not an admission" | — |
| a3 "So three questions will decide who wins." | judge WIDE, three question pills appear (roadmap) | — | pills 1 2 3 | ding ×3 |
| b1 "Question one. Was the ad a real offer?" | CRT on a cart in court | — | pill 1 lit | — |
| b2 "Usually, an ad isn't an offer. It invites you to make one, and the company can say no." | street shop window with a SALE poster; a shopper offers cash, the clerk shakes head | hero shrugs | `say("AD = INVITATION")` | — |
| b3 "And the small print you read? The jet isn't even in the prize catalog." | `catalog_el` CU, pages flip — no jet | — | red ✕ over the empty slot | page flip, buzzer |
| c1 "Question two. Would a normal person believe it?" | gallery rows of generic people | crowd looks at each other | pill 2 lit | murmur |
| c2 "The judge watches the ad. A teen flies a fighter jet to school." | judge watching the CRT, jet on screen | judge `brow="up"` | — | tiny jet sound |
| c3 "She calls flying a jet to school an exaggerated adolescent fantasy." | quote card over the judge | — | `quote_card(f, "exaggerated adolescent fantasy", "Leonard v. PepsiCo (S.D.N.Y. 1999)")` | — |
| d1 "Question three. Did Pepsi ever sign anything?" | table top, hero searching an empty folder | — | pill 3 lit | — |
| d2 "A sale over five hundred dollars needs a written deal… Pepsi signed nothing." | empty signature line CU | — | `say("NO SIGNED DEAL")` | pen click |
| d3 "August, 1999. The ruling: no objective person…" | judge CU → gavel | — | `cold_open(f, "AUG 1999", "NEW YORK", "THE RULING")` + quote card with the exact quote | **gavel**, shake |
| d4 "You appeal. You lose again." | hero walks down courthouse steps in the rain | sad | stamp "APPEAL LOST (2000)" | rain |
| t1 "And even if you'd won? The Pentagon said you couldn't fly it home." | the jet in a hangar, "NOT FOR CIVILIANS" tag on a rope | hero peeks in | small caption "a civilian would get it without weapons — and couldn't fly it" | hangar echo |
| e1 "So price every joke like someone will pay it." | marketing desk, a toy jet with a huge price tag | — | `say("PRICE EVERY JOKE")` | — |
| e2 "Was that ad a joke, or a deal? Comment JOKE or DEAL." | **end card** in the courtroom | hero to camera | `choice_card(f, "JOKE OR DEAL?", "JOKE", "DEAL", y≈1410)` | choice whoosh |
| e3 "Send this to the friend who'd mail that check." | end card holds, the cheque flutters across | hero waves | series badge | — |

Loop: end on the courtroom window with the jet outside (frame 1 composition).
Post copy: first line "A judge decided if Pepsi owed a 21-year-old a fighter jet." · "Your Move · Ep 1 · Part 2" · firstCommentText "JOKE or DEAL?"
YouTube title "Did Pepsi Owe Him a Fighter Jet? | Your Move" (≤ 50 chars).
