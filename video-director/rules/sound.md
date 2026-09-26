# Music and sound

## Where music comes from, in this order

1. **The client's licensed production library:** Artlist, Musicbed, Epidemic Sound or Soundstripe. These tracks are full-band stereo and cleared for commercial use. Record the track ID and licence in the project ledger.
2. **The HeyGen audio catalog via `/media-use`** (`resolve` a BGM). A gentle ambient piano bed from here on the free OAuth plan measured −15.4 LUFS, stereo width 0.30.
3. **The motion library sound kit** (on this machine: `~/work/motion-library/sound/`, mapped in `sound-map.json`).
4. **Generated music**, only when 1–3 can't serve, from a high-fidelity model, and only after it passes the music audit below. MusicGen-small output failed it (stereo width 0.04, 8–16 kHz energy at −41 dB): it sounds small, dull and cheap.

## How it should sound

- The mood follows the story. For product explainers that means calm and confident: warm ambient piano, soft acoustic, or minimal modern electronic, around 80–110 BPM, with no vocals under words.
- One bed for the whole film, sitting under the picture. It comes in on a 1–1.5 s fade, lifts into the fix and proof, resolves on the logo, and fades out over the last 1.5–3 s.
- Cut the picture to the music: put scene cuts on beats or bar lines (get a beat grid from `npx hyperframes beats`). Choose a track that fits the length, or edit it at bar lines. Time-stretching music to fit changes its feel and can make it warble.

## Music audit (before the track goes in)

1. Run `python3 scripts/audit_video.py TRACK.wav --out <dir>` on the music file alone.
2. `stereo_width` must be at least 0.12 and `air_db` at least −36 dB (see `gates.json`), with no clipped samples.
3. The per-5 s table stays steady across the whole length. Sudden clipping, flatness or centroid jumps mean distortion or a bad loop seam.
4. Listen once on laptop speakers and once on headphones.

## UI sound map (house defaults)

| Sound | Volume | When |
|---|---|---|
| bed (music) | 0.3 | the whole film, with fades |
| typing | 0.45 | text typed into a field |
| tap | 0.9 | a button press or send |
| click | 0.35 | a UI screen change |
| whoosh-airy | 0.45 | a scene cut or zoom-through, starting ~0.12 s before the cut |
| whoosh-short | 0.25–0.4 | a device rising or leaving; wordmark letters at 0.25 |
| riser | 0.18 | the last 1.5 s into a reveal |
| bloom-intro | 0.35 | the logo mark reveal (default) |
| chime-soft | 0.35 | a highlight or callout appearing |
| shimmer | 0.3 | the URL and end card |

- The default logo reveal is riser → bloom-intro → whoosh-short on the letters. Leave impacts and booms out of logo reveals. One sat about 10 dB above the rest of the mix and was rejected in review as too loud.
- Every sound effect stays within a few dB of the bed. The audit's `loudest_moment_lu` gate warns above +8 LU; accepted mixes peak at +5 to +6.
- For key sound moments (the logo reveal, the fix click), audition 2–3 short mixed options and let the user pick by ear rather than guessing.
- Soft whooshes on product ↔ text changes read well.

## Mix and master

- With a voiceover, the voice is the loudest thing and the bed is carved under it (`/hyperframes-audio`, voiceover carve).
- UI sounds stay small. Only the moments they mark (the fix click, the logo) stand out.
- Master the finished render with `scripts/master_audio.py`: −14 LUFS integrated, aiming for −1.5 dBTP. The gates are −15 to −13 LUFS, true peak at or below −1 dBTP, and 0 clipped samples.
