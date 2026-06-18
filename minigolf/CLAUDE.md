# minigolf : the MINIGOLF theory-screen visualization (noisy reward feedback under stochastic outcomes)

One vendored, self-contained, fully offline `index.html` (no build step, no sidecar
assets, no external/CDN references): "Mini-Golf in the Wind". You aim a putt at a
hidden hole while the wind nudges every shot, so any single swing's reward lies; the
right force is judged over many noisy tries. It builds intuition for **noisy reward
feedback under stochastic outcomes**, a companion to DARTS IN THE DARK.

## Contents
- `index.html` : the whole game (HTML + inline CSS + inline JS in one file).

This is the arcade cartridge only. The exercise notebook (`minigolf_notebook.ipynb`,
if present alongside) is NOT part of the arcade; leave it out of arcade work.

## Provenance and how to update
This file is upstream-owned, VENDORED from `eth-ainit-fs26/coding-exercises` (branch
`week3`). To update, **re-vendor** (copy the fresh `index.html` from coding-exercises)
rather than deep-editing the copy here, so changes stay in sync with upstream.

## Registration (do NOT edit here)
Registered in the root `cartridges.js` on the THEORY GAMES screen: `GAMES` entry
`{name:"MINIGOLF", href:"minigolf/", acc:"#22c55e", tag:"RL", ...}`, sprite key
`'golf'` (in `SPR`), and a Japanese string under `'minigolf/'`. The engine is
`js/arcade.js`. To change the name, blurb, or accent, edit the root `cartridges.js`,
not this folder.
