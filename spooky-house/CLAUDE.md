# spooky-house : the SPOOKY HOUSE theory game (value and the Bellman recursion on a grid)

One self-contained, offline `index.html` (no build step, no sidecar assets, ~770 lines)
titled "Bellman's Spooky House". It is a THEORY GAMES cartridge on the arcade's theory
screen.

## Concept it teaches
A hero walks a grid of haunted rooms from the top-left to the bottom-right, moving only
right or down, and sums the per-room "spookiness" (1 to 9). Brute-forcing every path
explodes (6 paths for 3x3, 3432 for 8x8), so the viz reframes the question per room:
"what is the max spookiness I can still collect from room (row, col)?" = this room's
score plus the best of the two reachable neighbours. That is the Bellman recursion / a
value function on a grid: one recursion (DP) beats enumerating every route. A
scrollytelling layout walks from the playable game to the equation.

## Provenance and how to update
This file is VENDORED (copied) from `eth-ainit-fs26/coding-exercises` (branch `week3`),
which owns it upstream. Do NOT deep-edit it here: to change it, re-vendor the newer
`index.html` from coding-exercises rather than hand-patching this copy.

## Registration
Registered in the root `cartridges.js` (the single content registry) as `GAMES[7]`
(name "SPOOKY HOUSE", `href:"spooky-house/"`, `acc:"#c084fc"`, `tag:"RL"`, plus a blurb
and a Japanese `jp`/`jb` entry keyed by href). It is placed in `VIEWS.extra`, so it
appears inside the THEORY GAMES bundle, not as a front-screen headliner. The engine
(`js/arcade.js`) consumes that registry; nothing here needs editing to add or move it.
