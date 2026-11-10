# What the platforms reward right now (keep this current)

Last researched: **2026-11-10** (R&D run: 3 extended searches + 4 pages read — Metricool Instagram news (mod. 6 Nov 2026), AIR Media-Tech YouTube month-by-month (upd. 4 Nov), OutlierKit YouTube updates (mod. 3 Nov), SocialBee (stale, last updated 24 Jul). Only dated items after 28 Oct: Instagram **ended linking Reels into a series on 28 Oct 2026** (Metricool) — we never used it, no change; YouTube **tests a 30-day lock instead of termination for some Spam-policy cases (29 Oct 2026)** (AIR, OutlierKit) — one original video a day, not affected. No Reels/Shorts ranking change dated after 1 Oct ("Shorts recommendations now favor original content"). Metricool lists undated items near the top — an AI-label rule tied to reach, "Your Algorithm" in Feed, original-content guidelines — re-check on a first-party Meta page before acting. Pages disagree on the Feb 2027 YPP rule (OutlierKit: existing members need 10M Shorts views / 90 days; AIR doesn't say) — the 11-shorts-money build gate already covers it. **Note:** the owner's Michelin post (9 Nov) went out with Instagram's AI label OFF (`isAiGenerated: false`) while every studio post sets it ON — keep it ON (BRAND.md). Previous: 2026-11-06.) Every run: if this date is more than 3 days old, research again (WebSearch, extended mode:
"Instagram Reels algorithm <month year>", "YouTube Shorts algorithm <month year>", "Instagram/YouTube policy AI content <month year>"),
update this file with dated, sourced facts, and say what changed in the run report.

## Instagram Reels
| Fact (date) | What we do about it |
|---|---|
| Top ranking signals are **watch time** (avg watch time, rewatches), **likes per reach** and **sends per reach**; sends matter most for reaching non-followers (Mosseri, Jan 2025, repeated since) | Hook in the first second, payoff held to the end, loop the last line into the first; CTA names a specific friend ("Send this to the friend who…") |
| Original content favoured; accounts reposting without meaningful edits stop being recommended (30 Apr 2026) | Every video is new, never re-cut |
| Max **5 hashtags** per caption (Dec 2025); hashtags describe, they don't boost reach; keywords in the caption matter for search | Keyword sentence first, exactly 5 specific hashtags |
| Public Reels of professional accounts can appear in Google search (Jul 2025) | Keyword-rich first line + alt text |
| "AI-generated profile" label for profiles presenting an AI-generated *person* (31 Aug 2026; unlabelled ones lose recommendations) | Our mascot is a cartoon, not an AI person; keep the per-post AI label (isAiGenerated) for the synthetic voice |
| Smaller accounts get equal initial test distribution on Reels | Every post is tested on non-followers first → the first 3 s decide everything |
| Mosseri, 23 Oct 2026: ranking focuses "a lot more on finding reels and photos that you might send to a friend" than on comments; scheduling a post does not hurt reach (ZoomSphere transcript, 28 Oct 2026) | Every episode is built to be *sent* (a surprising true story + a debatable choice); keep scheduling via Metricool |
| Mosseri, 16 Oct 2026: "We do not throttle reach of AI content just for being AI content" — as long as it is labelled; the Sep 2026 "AI-generated profile" label applies only to accounts presenting an AI-generated *person* (Metricool news, 28 Oct 2026) | Keep `isAiGenerated=true` per post for the synthetic voice; our cartoon hero is not an AI person → no profile label |
| Jul 2026: an "AI Info" label can be added to posts; Aug 2026: Bonuses program pays for photo/carousel posts; Oct 2026: a Reels-first feed is being tested on iOS (SocialBee, 26 Oct 2026) | Nothing to change for Reels; a photo/carousel "trick card" post could earn a bonus later |
| Mosseri, 16 Oct 2026, reported by ZoomSphere (30 Oct 2026, secondhand): experimenting with Trial Reels is fine, reposting the same trial reel repeatedly is not: "We're going to crack down on that." | Never re-post a trial reel; every post is new anyway |
| Mosseri, 30 Oct 2026 (same relay): "We don't demote content for being created with other apps other than ours", but a video with another app's logo is "going to get less distribution" | Our renders carry no third-party watermark; keep it so, and don't re-upload from an app that stamps one |
| Mosseri, 23 Oct 2026 (same relay): opt-in AI dubbing in "more than 12 languages" for creator and public accounts | Possible cheap reach test for EU viewers later; check how it interacts with the AI label first. Not adopted |
| Instagram stopped letting creators link Reels in a series from 28 Oct 2026 (Metricool news, page dated 30 Oct 2026) | Don't plan on IG series links; two-parts say "part two" aloud and in the caption |
| Meta Q3 2026 (21 Oct): an "upgraded model architecture that ranks sequences of Reels at a time instead of evaluating each Reel independently"; 26 Oct: US test of 90-minute horizontal videos with selected creators, "we're testing a dedicated home for horizontal videos" 3 Nov (Keywords Everywhere tracker) | Nothing to change; the first reason to care about how a reel sits next to others in a session. Not adopted |
| Mosseri on Threads, 27 Oct 2026 (Keywords Everywhere, 28 Oct): "Features is not fully launched yet, we're testing and ramping up access slowly"; "exploring multiple options to help long-form creators get paid" | Horizontal long-form test, reels link into it. Not for us yet |
| UK CMA "is seeking information from Meta on its new Meta One business subscription service", which sells links in posts and reels; "No decision has yet been taken" (30 Oct 2026, gov.uk via Keywords Everywhere, 2 Nov) | Don't plan on paid links in reels; bio link stays |

## YouTube Shorts
| Fact (date) | What we do about it |
|---|---|
| Main signal: **viewed vs swiped away** (YouTube Help: "How many chose to view"); Shorts are tested on a seed audience, then widened (Todd Sherman) | First frame must already be interesting (object + motion + question), no slow intro |
| Public views count from the first frame (24 Aug 2026); **engaged views** (watching past the first seconds) are what earn and what retention/AVD use | Optimise the first 2 seconds and average view duration |
| Original Shorts get more reach; re-uploads and "minor template changes" don't count as original (1 Oct 2026) | New props, new layout idea, new music genre every video — never just swap text in a template |
| Monetisation excludes repetitive, unsatisfying and AI-persona advice content (13 Jul 2026); YPP from 1 Feb 2027 needs 20M Shorts views / 90 days for new channels | Quality over volume; max one post per 4.5–5 h; each video must teach something real |
| No ideal length — "to what length do you need to tell your story?"; Shorts can be up to 3 min (Oct 2024) | 60–90 s when the story needs it; never pad |
| Custom Shorts thumbnails (24 Jul 2026, YPP first); dislike removed from Shorts player, "Not interested" shapes feeds (25 Jun 2026) | Set `videoCoverMilliseconds` on the clearest hook frame; avoid anything that feels like clickbait |
| Shorts series (Sep 2026) group Shorts into seasons/episodes | Our three named series (YOUR MOVE / SPOT THE TRICK / WHO REALLY OWNS IT) map onto Shorts series — set them up once the first episodes are live |
| AI labels (YouTube Blog, 27 May 2026): one label for all "photorealistic and meaningfully AI altered or generated content", shown as an overlay on Shorts; "unrealistic, animated, or slightly altered" content's disclosure sits in the expanded description; from May 2026 YouTube auto-applies the label when it detects undisclosed AI; "a disclosure label alone does not change how a video is recommended or whether it's eligible to earn money" | Keep `isAiGeneratedContent=false` for our code-drawn animation + generic synthetic narrator (not a realistic person); never a photoreal AI person or voice clone |
| 1 Oct 2026 (TeamYouTube via OutlierKit, 3 Oct): channels "primarily aggregating or re-uploading other creators' videos without significant changes will likely see less distribution within the Shorts feed"; 1 Sep 2026 (Todd Beaupre): "no metric on its own is a good indicator of value" | Every episode is an original story with its own scenes/props/music (BRAND.md §2) |
| 3 Sep 2026: YouTube may auto-apply a label to undeclared branded content: "we may automatically apply a branded content label to your video and notify you" (TeamYouTube via Miraflow, 13 Sep 2026; enforcement details on that page are the author's inference); creators got age and country controls for branded content (air.io, Oct 2026) | Tick "includes paid promotion" every time a deal arrives; BRAND.md §4 updated. Primary post not read yet: support.google.com/youtube/answer/17596007 |
| TeamYouTube test, 29 Oct 2026 (OutlierKit): "a 30-day locked period in place of immediate termination for certain Spam policy violations"; which ones not stated | Nothing to change |
| "YouTube is testing a $20 payment threshold (instead of $100) for some creators in the USA, India, and Indonesia" (SocialBee, 2 Nov 2026, citing Social Media Today, secondhand) | Not in YPP yet. If it reaches us, small Shorts money pays out sooner. Not Shorts-specific |

## Sources
- SocialBee — YouTube updates (2 Nov 2026): https://socialbee.com/blog/youtube-updates-news-features/
- Keywords Everywhere — Instagram tracker (read 4 Nov 2026; Meta Q3 sequence ranking, horizontal video test): https://keywordseverywhere.com/news/instagram-algorithm-updates/
- Miraflow — YouTube branded-content auto-label (13 Sep 2026): https://miraflow.ai/blog/youtube-auto-label-branded-content-ai-video-disclosure-2026
- YouTube Blog — "Improving AI labels for viewers and creators" (27 May 2026): https://blog.youtube/news-and-events/improving-ai-labels-viewers-creators/
- OutlierKit — YouTube algorithm updates 2026 (page updated 3 Oct 2026; Shorts originality 1 Oct, YPP 2027 bar, Beaupre 1 Sep): https://outlierkit.com/resources/youtube-algorithm-updates/
- ZoomSphere — Mosseri Q&A transcript, 16/23 Oct 2026 (sends, AI content, scheduling): https://www.zoomsphere.com/blog/instagram-algorithm-2026-what-actually-gets-reach
- Metricool — Instagram news (28 Oct 2026: AI-person label enforcement, originality definition): https://metricool.com/instagram-news/
- SocialBee — Instagram updates (26 Oct 2026: AI Info label, Bonuses, Reels-first feed test): https://socialbee.com/blog/instagram-updates/
- reeldrop.io — Instagram ranking signals Meta confirmed (updated Sep 2026): https://www.reeldrop.io/learn/instagram-algorithm
- keywordseverywhere.com — Instagram confirmed changes tracker: https://keywordseverywhere.com/news/instagram-algorithm-updates/
- implicator.ai — Instagram "AI-generated profile" label (31 Aug 2026): https://www.implicator.ai/instagram-will-cut-the-reach-of-ai-personas-that-skip-its-new-label/
- socialmediatoday.com — Instagram 5-hashtag limit (Dec 2025): https://www.socialmediatoday.com/news/instagrams-implementing-new-limits-on-hashtag-use/808309/
- outlierkit.com — Shorts algorithm in YouTube's words: https://outlierkit.com/resources/youtube-shorts-algorithm/
- air.io — YouTube 2026 month-by-month changes: https://air.io/en/trending/youtube-algorithm-in-2026-month-by-month-changes-that-affect-your-views
- YouTube Help — altered/synthetic content disclosure: https://support.google.com/youtube/answer/14328491
- newscaststudio.com — YPP requirements doubled from Feb 2027 (Aug 2026): https://www.newscaststudio.com/2026/08/10/youtube-partner-program-monetization-changes-2027/
