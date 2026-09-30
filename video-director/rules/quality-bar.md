# Quality bar

The bar is a set of six product videos (2026) from Claude, Linear and OpenAI:

- https://x.com/claudeai/status/2100632677904744716 (Projects, 83 s)
- https://x.com/claudeai/status/2013754136265621952 (health integrations, 72 s)
- https://x.com/OpenAI/status/2047008987665809771 (workspace agents, 70 s)
- https://x.com/OpenAIDevs/status/2039482146369458526 (Linear plugin in Codex, 24 s)
- https://x.com/linear/status/2013643099147248054 (Reviews, 25 s)
- https://x.com/linear/status/2049897250449391850 (Releases, 30 s)

They come in two families:
- **Product storytelling on a flat stage** (Claude and OpenAI): typed headlines, the product shown whole or in large pieces, lists that build and tick, hard cuts or gentle dissolves, median shot 3.5–3.9 s, nothing still for more than 4 s.
- **Dark 3D trailers** (Linear): borrow only their slow mono titles typed with a block caret.

The Zelios-style SaaS explainer remains a source for motion recipes (`rules/motion.md`), not the bar.

## The rule

Put our cut next to the reference, moment by moment. If any scene looks less designed, less sharp, less smooth or less deliberate than the matching moment of the reference, it is not finished: rework it before anyone sees it. Use production-grade inputs only. The table lists the cheap tells we have already caught and what replaces each one.

| Cheap tell (fails the bar) | Replace with |
|---|---|
| Full-screen sentences on an empty background: a slideshow | Words riding on the product or on a designed stage (`rules/text.md`) |
| A flat, empty stage | A stage with depth: graded footage or light (a sunlit wall, drifting light, soft leaf shadows), glass surfaces, gradients with glow |
| A raw screen recording at 1.0× with tiny text | The product presented as a designed object: a glass card, a device mockup, or a punch-in, with key text ≥ 24 px |
| Default fades everywhere, idle wobble | Designed transitions: zoom-throughs, masked wipes, scale-swaps, letter staggers (`rules/motion.md`) |
| AI music from small models, mono beds, quiet mixes | Licensed, produced stereo music at −14 LUFS (`rules/sound.md`) |
| Robotic text-to-speech | Text-led, or a professional voice |
| A low-bitrate encode, a global speed-up | A delivery render at ≥ 8 Mbps (1080p), with timing set in the edit |
| Raster or blurry logos, off-brand fonts | Vector marks, the brand's own fonts, and letters as live text |

## What the reference does (its opening, from the tutorial breakdown)

- **Stage:** 4K footage of a sunlit concrete wall with diagonal sun stripes and plants. Soft light leaks drift across it, under a slightly lifted, desaturated grade.
- **Type:** a big two-tone headline with the logo set inline ("Build something [logo] lovio"). The words build in one by one, with a quieter subtitle underneath.
- **Product as an object:** a frosted glass prompt card with pill buttons and send and voice icons. The prompt types in with a caret.
- **Brand moment:** the keyword ("idea") appears huge on a blue→purple wave field, with a gradient fill and glow, revealed by a feathered wipe. It shrinks into the logo mark (an overshoot pop), then the wordmark letters stagger in.
- **Device:** the product on a laptop in a studio set, with a slow push-in.
- **Motion:** one house ease, `cubic-bezier(0.2, 0, 0.22, 1)`, everywhere. Overshoot only on the logo, and nothing moves without a reason.
- **Sound:** gentle, produced music, with sound marks on typing, taps, whooshes and the logo.

## How to check

1. Keep a local copy of the reference for comparison only, never for redistribution: `~/work/motion-library/reference/lovio-zelios.mp4`.
2. Run `python3 scripts/audit_video.py OUR.mp4 --reference <that file>` and compare loudness, stereo width, air, bitrate, scene pace and still stretches side by side.
3. Lay our contact sheets next to `reference/contact_*.png`. For each of our scenes, name the reference moment it should match and say where ours falls short.
4. Fix every shortfall before showing the cut.
