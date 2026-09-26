# Delivery

## Render

- Deliver 4K by default: `npx hyperframes render --resolution landscape-4k --quality delivery --crf 8`, which is near-lossless. Use a 1080p master (same flags without `--resolution`) only when asked.
- Control quality with CRF, not a bitrate target. Mostly-static UI compresses tiny even near-lossless: a CRF 8 4K product film measured 8.9 Mbps, and `--video-bitrate 45M` still averaged only 17.7 Mbps. The bitrate gates are warnings; the real check is 100% crops of the master.
- **4K sharpness has a zoom budget.** A 4K recording (2 px per CSS px) stays pixel-sharp in a 4K master only up to ~1.33× zoom inside a 1440-wide window (2880 px at 4K). Deeper punch-ins are upscaled: fine at 1080p viewing, soft at 100% on a 4K screen. For deep punch-ins at 4K, record the take at deviceScaleFactor 3–4, or accept 1080p-equivalent sharpness in those shots. Screencast frames recorded as JPEG show their 8×8 blocks once upscaled past ~2×.
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
