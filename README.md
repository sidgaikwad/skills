# skills

Claude Code skills for making professional product videos.

| Skill | What it does |
|---|---|
| [video-director](video-director/SKILL.md) | Directs a product video end to end: interview (grill with docs) → brief and beat plan → one-frame mockup sign-off → HyperFrames build under house rules → audit against gates and the quality-bar reference → delivery. It also reviews existing videos. |

## video-director at a glance

- `SKILL.md`: the seven steps and their completion criteria.
- `interview.md`: the question tree for the opening interview.
- `rules/`:
  - `story.md`: story spine, length, copy, demo data
  - `text.md`: on-screen text
  - `footage.md`: product footage, framing, cursor
  - `motion.md`: eases, move recipes, transitions
  - `sound.md`: where music comes from, how it should sound, sound map, mastering
  - `brand.md`
  - `delivery.md`
  - `quality-bar.md`: the reference film every cut must match
- `templates/`: `BRIEF.md` (HyperFrames-compatible), `PLAN.md`, `REVIEW.md` and `BRAND.md`. Client brand profiles are kept privately, outside this repo.
- `gates.json`: every number the audit enforces, each with its reason.
- `scripts/audit_video.py`: measures a render or a music file (loudness, true peak, clipping, loudest moment, stereo width, air, bitrate, empty-stage share, first product frame, scene pace, still stretches). It writes contact sheets, a phone-size sheet and a timeline, and compares against a reference video.
- `scripts/master_audio.py`: two-pass loudness mastering to −14 LUFS / −1.5 dBTP. It re-encodes only the audio and copies the picture untouched.

## Install (Claude Code)

```bash
git clone https://github.com/sidgaikwad/skills.git ~/work/skills
ln -s ~/work/skills/video-director ~/.claude/skills/video-director
```

Restart Claude Code after installing. `git pull` in `~/work/skills` updates the skill.

## Requirements

- ffmpeg and ffprobe, plus Python 3 with numpy and Pillow, for the scripts.
- The HyperFrames skills (`/hyperframes` and its workflows) for the build step.
- `/grilling` and `/domain-modeling` for the interview.
