---
name: video-director
description: Direct a professional product video end to end — interview the user first (grill with docs), lay out brief, beats and sound, get a one-frame mockup signed off, build with HyperFrames under house rules for story, text, footage, motion, music and delivery, then audit the render. Use first, before /hyperframes, whenever the user wants to make or plan a product, feature, launch, explainer or promo video (even from a vague idea or a few screenshots), or asks whether an existing video is professional enough or how to improve it.
---

# Video director

You direct; the user is the client. A director interviews before shooting, puts every decision on paper, gets sign-off on the look before building it, and checks the cut against the house rules before anyone else sees it. HyperFrames builds the film; this skill decides what the film is and whether it is good enough.

A professional product video, in this house:

1. **Product on screen.** The product is the hero and is on screen almost all the time; the words ride on it.
2. **One story.** One customer, one problem, one cause, one fix, one proof, told so a buyer could retell it.
3. **Every second earns its place.** Timing is set in the edit, shot by shot.
4. **Sound as finished as picture.** Produced stereo music, mastered to −14 LUFS.
5. **Nothing looks accidental.** Whole text at every crop edge, full frames, a visible cursor, a real end card.
6. **At par with the quality bar.** Every cut holds up next to the reference film in `rules/quality-bar.md`, moment by moment; anything cheaper-looking is redone before anyone sees it.

The rules behind each live in `rules/`; each step names the ones it needs. Brand profiles override house rules, and house rules override HyperFrames defaults. Profiles hold client specifics, so they live outside this public skill, in a private brands folder (on this machine: `~/work/video-brands/<client>.md`); start a new one from `templates/BRAND.md`. Paths below are relative to this skill's directory.

## Branches

- **New video** (an idea, brief, screenshots, a URL): steps 1–7.
- **Review an existing video** ("is this professional enough?", "how do we make it better?"): step 1, then the audit in step 6 on the file, then write the verdict with `templates/REVIEW.md`: verdict, measured gates, top 5 fixes with timestamps and evidence, what to keep, plan with times.
- **Rework an existing video**: review first; the fixes the user approves become the plan, from step 3 on.

## Steps

### 1. Read everything first

Look before asking. Open every screenshot, file and link the user gave, any existing project (`BRIEF.md`, `STORYBOARD.md`, renders), and the client's brand profile. With no profile yet, read the client's live website (copy and CSS) and start one from `templates/BRAND.md`.

Done when: a fact list exists (product and feature names in the product's own words, screens available, brand colours, fonts, tagline and call to action, audience clues, prior feedback), and every question you could answer by looking is already answered.

### 2. Interview (grill with docs)

Run a `/grilling` session using `/domain-modeling`: this is grill-with-docs for video. Walk `interview.md` branch by branch, one question at a time, each with your recommended answer drawn from step 1. The moment an answer settles, write it into `video-plan/BRIEF.md` (shape: `templates/BRIEF.md`) and every product term into `video-plan/CONTEXT.md`, so a dead session resumes where it stopped. For an existing HyperFrames project, `video-plan/` is the project root.

Done when: every branch of `interview.md` is answered or explicitly deferred by the user, and the user confirms the brief.

### 3. Lay out the film

Write `video-plan/PLAN.md` from `templates/PLAN.md`: the story spine, the beat table (seconds, product view and zoom target, words, move, sound), the music with its source and licence, the assets to capture, and the deliverables. Write it with `rules/story.md`, `rules/text.md`, `rules/footage.md` and `rules/sound.md` open.

Done when: the beat seconds sum to the brief length (±5%), every beat names its product view, words, move and sound, every box in the plan's pre-flight list is ticked, and the user approves the plan.

### 4. Mockup gate

Render one hero frame of the planned look and show it next to the matching moment of the quality-bar reference (`rules/quality-bar.md`); for a change to an existing look, show before and after side by side as well. Approving an idea in words is not approving how it looks: a whole restyle round was lost that way once.

Done when: the user has said yes to the frame, or the plan uses an approved brand profile unchanged.

### 5. Build

Hand over to `/hyperframes` with: "The intent is confirmed in `video-plan/`. Skip the intent interview, route to the `workflow:` in BRIEF.md, and right after `hyperframes init` copy `video-plan/{BRIEF,CONTEXT,PLAN}.md` into the project root." In an existing project, update its `BRIEF.md` in place instead. Build to `rules/motion.md` and `rules/footage.md`. When the motion library exists (on this machine: `~/work/motion-library`), reuse its blocks, templates and sound kit.

Done when: `npm run check` passes and a `--quality looks` render exists.

### 6. Audit

Run `python3 scripts/audit_video.py RENDER.mp4 --target <brief seconds> --reference <quality-bar video>` (add `--kind motion` for typographic pieces). Open `timeline.png`, `phone.png` and the contact sheets it writes, lay them beside the reference's sheets, and work through the manual checks at the bottom of `audit.md`. Fix, re-render, re-audit. The gates and their reasons live in `gates.json`.

Done when: no gate is FAIL, every WARN is fixed or accepted by the user in writing, every manual check is ticked, and every scene holds up next to its reference moment.

### 7. Deliver

Follow `rules/delivery.md`: the final render at delivery quality, `scripts/master_audio.py` for loudness, cut-downs, the SRT and the thumbnail. Share the files with the audit summary.

Done when: every deliverable in `PLAN.md` exists and its own audit passes.
