# Product footage

## Record

- Record the real product; never redraw its UI. Record at 2× device scale (4K for a 1080p film) from a seeded demo account, so punch-ins stay sharp.
- Take one clean take per action, with developer chrome, toasts, notifications and stray hovers hidden, and fictional customer names only.
- After the fix, record the problem view again from the same position, for the proof shot.

## Frame

- **Show the whole screen.** Every product shot is the full recording, scaled down into a rounded frame that fills about 90% of the picture. Never a static crop of a recording: a cropped screen loses the context that tells the viewer which screen they are on, and reads as a mock-up. (A client rejected cropped UI fragments outright.)
- Whatever the viewer must read gets a camera push, not a crop: a gentle, temporary push (≤ 1.4×) that starts from the full screen and returns to it, so the context is never lost. A whole-app view puts UI text at about 8–11 px at 1080p; deliver 4K so it stays crisp, and carry the key numbers in captions and labels.
- No more than about 25% of a product shot is empty; tighten the crop or move the window. One reviewed drag-and-drop shot was about 60% empty.
- Crop edges fall in the gaps between elements, so every title, breadcrumb, label and number is either whole or fully out of frame.
- Keep one product-window treatment for the whole film: same size, radius, hairline and shadow. The brand profile records it.

## Move

- Each shot gets one purposeful camera move: a push-in to what the words name, or a pan that follows the action (the drag, for example). Eases come from `rules/motion.md`.
- Show the fix as one continuous action: drag → drop → regenerate → result.
- Every screen stays up long enough to read:
  - a new screen stays up at least 3 s before it changes;
  - hold at least 2 s after each action settles, or 2.4 s when a label appears;
  - a settled hold longer than about 4.5 s is dead air (the `longest_still_s` gate).

## Cursor

- Use one visible cursor style for the whole film: dark, 34–48 px at 1080p, on a smoothed path. It enters from off-screen, shows a click ring or tap on every click, and fades after about 1 s idle. `/oversized-cursor` has the full technique.
- A faint grey cursor disappears against a light UI.

## Proof

End the product section on the proof view: the same row or cell that was red is now green, with a label ("Ships on time", "0 unscheduled"), held for at least 2.4 s.

## Phone test

Check the audit's `phone.png`. Every word and number the story depends on must be readable at phone size. If one isn't, punch in further or repeat it as a callout label.
