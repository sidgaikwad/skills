# Delivery

## Render

- Deliver 4K by default: `npx hyperframes render --resolution landscape-4k --quality delivery --video-bitrate 45M`. Use a 1080p master (`--video-bitrate 12M`) only when asked.
- Set the bitrate explicitly. Static UI encodes to a small file at CRF settings, and the explicit bitrate gives the platform's re-encode a clean source. The gates are at least 35 Mbps at 4K and 8 Mbps at 1080p, YouTube's upload recommendation. One 4K render measured 24 Mbps without the flag.
- YouTube serves 4K uploads with better codecs, which also improves what 1080p viewers see (widely reported, not official).
- The frame rate matches the capture rate: 30 fps for screen recordings.

## Master

- Run `python3 scripts/master_audio.py RENDER.mp4 FINAL.mp4`. It brings the audio to −14 LUFS and −1.5 dBTP as AAC 320 kbps at 48 kHz, and copies the picture stream untouched.
- Re-run the audit on `FINAL.mp4`.

## Versions

| Version | Aspect | Length | Where |
|---|---|---|---|
| Master | 16:9, 1920×1080 or 3840×2160 | as briefed | YouTube, website |
| Feed cut | 1:1 (1080×1080) or 4:5 (1080×1350) | 15–30 s | LinkedIn, X |
| Vertical | 9:16 (1080×1920) | 15–30 s | Shorts, Reels (only when asked) |

Recompose each cut-down: lay the stage out again for its aspect ratio, so the product and the words stay whole. A centre crop of the 16:9 master slices them.

## Extras

- An SRT of the on-screen text (and any voiceover), for accessibility and search.
- A 1280×720 thumbnail with 5 words or fewer and the product visible. Frame 0 is the default.
- For YouTube: a title, and a description with the URL in its first line. Add chapters only when there are at least 3 sections of at least 10 s.
- Keep the audit report next to the master.
