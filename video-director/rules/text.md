# On-screen text

## Text rides on the product

The words sit above or beside the live product while it plays: a headline zone above the product window, or a side column. Full-screen text on an empty stage is only for the title frame and the end card, and together they stay under the `sparse_share` gate (15% of the runtime).

*Why:* in one reviewed cut, 54% of the runtime was text or nothing on an empty stage. The product first appeared at 10.6 s, and the film switched between text and product 14 times. It read as a slide deck.

Starting layout for the mockup (16:9, 1920×1080): a centred headline zone at y 56–200 (two lines at 56 px) and the product window at 1440×810, placed at x 240, y 222, radius 16. Adjust it in the mockup, then keep it for the whole film.

## Size and placement (1920×1080; double everything for 4K)

- Headlines are at least 56 px. A proven style: Geist 500, 58 px, line-height 1.22, tracking −0.015 em, near-black ink on a light stage.
- Callouts and labels are at least 32 px.
- Every word or number the story needs is at least 24 px, including UI text after zooming in.
- Use one headline zone for the whole film, in the same position and alignment throughout, inside the 5% title-safe margins.
- Keep contrast at 4.5:1 or better against whatever is actually behind the text.
- Callouts are 3 words or fewer ("2 days late", "0 unscheduled"). They sit next to the element they name, joined by an ink ring or leader line.

## Reading time

- Hold each line for words ÷ 3 + 1 s, and never less than 2.4 s. (BBC subtitle pace is 160–180 words a minute.)
- Reveal fast, then hold still. Words cascade in over about 0.5 s in total: at most 0.045 s between words, each word taking 0.4 s on power2.out, rising y 10 → 0 and fading opacity 0 → 1, already at its final position. Hold the line, then it leaves as one block in 0.25 s.

*Why:* a slow word-by-word clock reads as jumpy and unnatural. A fast cascade followed by a still hold reads cleanly.

## Clean ground

Text sits on a clean area of the stage or frame, and the product behind it stays sharp. Some brand profiles forbid blur and scrims behind words; follow the profile.
