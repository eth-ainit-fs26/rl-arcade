# darts : "DARTS IN THE DARK" theory game (one vendored offline HTML)

A single self-contained `index.html` (no build step, no sidecar assets, fully
offline) titled "Blind Bullseye" in the page itself. It is one of the THEORY
GAMES, **vendored** from the course's own repo
`eth-ainit-fs26/coding-exercises` (branch `week3`); upstream owns it.

## Concept it teaches
An **online running estimate converging**: learning rate vs stability. You
shoot darts at a hidden, drifting bullseye and only hear a score, then nudge
your aim toward the error each round. A **large, fixed step** keeps overshooting
and orbits the target forever; a **decaying step** `alpha(t)` lets the aim
fine-tune and settle. That decaying schedule is the Robbins-Monro condition for
convergence. Big misses, big corrections, then shrink the steps so the aim
settles.

## Updating
Do NOT deep-edit the HTML here. Re-**vendor**: copy the fresh `index.html` from
`eth-ainit-fs26/coding-exercises` (the darts/Blind-Bullseye visualization,
branch `week3`) over this file.

## Registration
Registered in the root `cartridges.js` (the single source of truth), not here:
`window.GAMES` entry `href:"darts/"` (name "DARTS IN THE DARK", tag `RL`,
accent `#38bdf8`), placed in the THEORY GAMES bundle `window.VIEWS.extra`, with
a Japanese name/blurb in the `JP` map. The engine is the root `js/arcade.js`.
