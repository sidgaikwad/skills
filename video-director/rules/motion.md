# Motion

Sources: a frame-by-frame breakdown of a Zelios-style SaaS explainer and the house motion built from it (`motion-library/reference/zelios-saas-explainer-breakdown.md`, `motion-library/motion/house-motion.md`), plus client review rounds.

## Principles

- Motion carries the eye to the next thing to read. Every move has a job: reveal something, follow the action, or connect two scenes. Movement that is only decoration gets cut. `/motion-doctrine` covers the vector law, causal motion and stillness before a climax.
- A fast start with a long, soft settle, from the house ease, for almost everything. Overshoot only where a physical pop is the point: the logo mark or a button.
- One transition family per film, with matched speed across each cut. For example: cut-the-curve LEFT between scenes, UP into the close, and an inverse zoom-through into the outro. See `/cut-the-curve` and `/seam-craft`.
- Timing is set in the edit (holds and cuts) and rendered at 1× speed.
- **Crisp type at rest.** Every letter is crystal clear on a big screen the moment it settles. Blur on an entrance clears within 0.4 s, even when the move itself runs longer, so run blur as its own short tween. A glow is a blurred duplicate behind a sharp, full-opacity text layer. *Why:* 1 s blur-in ramps plus a heavy glow made big type read as soft in review.

## Hand-made, not generated

Viewers spot generated motion instantly: everything on one ease, text streaming in word by word, strokes popping in, straight-line cursors, template decoration. What reads as crafted:

- **Camera:** a critically damped spring on (centre x, centre y, log zoom) at about 1 Hz, sampled per frame. It eases in and settles like an operator, with no overshoot. Start annotations ~0.9 s after a new camera target, once it has settled.
- **Cursor:** a slight arc (bow ≈ 5% of the distance, ≤ 30 px), a minimum-jerk speed profile (10u³ − 15u⁴ + 6u⁵), and a ~1% overshoot that settles back on long moves. Duration ≈ 0.30 + 0.0004 × distance, clamped to 0.4–0.92 s, arriving exactly at the recorded click. Drags follow the recorded path, because the dragged item is attached to it.
- **Annotations:** a hand-drawn loop (a superellipse with a gentle wobble, drawn ~7% past its start and lifting away) and a pen-like arrow (a curved body, then a quick V head), drawn with `power2.inOut`. One loop per step. Red for the problem, green for the fix.
- **Text:** mask line reveals (each line slides up inside its own mask, `expo.out`, 0.07 s apart), never word-by-word streaming, which reads as a chatbot. Typing only for a hook headline, with an uneven typist's rhythm (longer after spaces and punctuation). A highlighter swipe on the payoff words.
- **Leave out:** dot-grid backgrounds, light sweeps, 3D-tilted floating chips, connector lines to nowhere, countdown numbers and pop-ins on everything.
- **Technical:** draw strokes with `pathLength="1000"`, `stroke-dasharray: 1000 1000` and a dash offset tween from 1000 to 0. Keep the stroke at opacity 0 until its draw starts, because round caps otherwise show dots. `pathLength="1"` pops instead of drawing in Chrome. Set every reveal's hidden start state at t = 0 (`immediateRender: false` leaves it visible until its tween starts), and keep a frame's content playing under the frame's own fade-out.

## Eases

| Name | Value | Use |
|---|---|---|
| `tutOut` (house) | `cubic-bezier(0.2, 0, 0.22, 1)`; GSAP `CustomEase.create("tutOut", "M0,0 C0.2,0 0.22,1 1,1")` | almost every move |
| pop | `back.out(1.6)` | the logo mark and button pops; the only overshoot |
| exit | `power3.in` | things leaving: zoom-through, a device sinking |
| ambient | `sine.inOut`, finite repeats | slow drifts and light sweeps |
| text cascade | `power2.out`, 0.4 s | word cascades (`rules/text.md`) |

`index.html` loads `CustomEase.min.js` after GSAP and calls `gsap.registerPlugin(CustomEase)`.

## Move recipes

| Move | Recipe |
|---|---|
| Headline build | words `opacity 0, y 44` → rest, 0.85 s `tutOut`, stagger 0.13; each word's `blur 12px → 0` runs over its first 0.4 s |
| Glass card rise | `opacity 0, y 70, scale 0.955` → rest, 1.05 s `tutOut`; buttons pop 0.55 s `back.out(1.6)`, stagger 0.08 |
| Typing | per-character schedule (0.022–0.038 s per character, 0.06 s at spaces) compressed into a fixed window; the caret blinks on a deterministic square wave |
| Button press | scale 0.86 over 0.1 s, back to 1 with `elastic.out(1, 0.45)`, plus a ring `scale 1 → 1.9, opacity 0.9 → 0` |
| Zoom-through seam | outgoing stage `scale 1.45, blur 18px, opacity 0` in 0.3 s `power3.in`; incoming arrives from `scale 0.72` → rest in 1.0 s `tutOut`, its `blur 18px → 0` over the first 0.4 s |
| Keyword reveal | feathered left-to-right mask wipe (mask 300% wide, position 100% → 0%) of a sharp text layer, with a subtle blurred duplicate behind it as the glow |
| Scale-swap | the word shrinks to 0.18 with blur and fade (0.55 s `power3.in`) while the mark pops in at the same centre 0.42 s later |
| Letter stagger | wordmark letters `opacity 0, y 60` → rest, 0.7 s `tutOut`, stagger 0.065; each letter's `blur 10px → 0` runs over its first 0.4 s |
| Dock and return | lockup `scale 0.42, y −318` (0.9 s) to make room; back to centre later (1.0 s) as the URL rises in |
| Device rise | laptop `y 760, rotateX 28°, scale 0.9` → `y 0, rotateX 7°` in 1.2 s, then a slow push to `rotateX 2°, scale 1.035` |
| Product push-in | 0.8–1.4 s `power3.inOut` (or `tutOut` when it starts from a click), ending ≥ 2 s before the next change |

## Brand overrides

- A brand profile can ban blur outright. Then replace the blur in these recipes with opacity and scale, and make product ↔ text changes opacity only.

## Render correctness (HyperFrames)

- Never CSS-`transform` an element that GSAP also moves; set starting values with `tl.set` at 0 or with `fromTo`.
- Hidden starting states go in CSS (`opacity: 0`), not in a `tl.set` at 0.
- One `fromTo` per element and property; later moves are `.to`.
- Animate with transforms; keep `letter-spacing`, `width` and `height` still.
- Colour-treat real footage with `hyperframes media-treatment` (`/media-use`), not CSS filters.
