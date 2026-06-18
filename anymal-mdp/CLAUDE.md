# anymal-mdp : the "ANYMAL MDP" front-screen game (the four pieces of an MDP)

A robot dog (ANYmal) roams a grid chasing treats. The visualization builds
intuition for the four pieces every Markov Decision Process is made of:

- state (where the dog is on the grid),
- action (the moves it can take),
- transition (what outcome a move leads to),
- reward (the payoff for landing somewhere).

## What is here

- `index.html` : ONE self-contained, offline HTML file (no build step, no
  sidecar assets, no external requests). It is a scroll-snap course/explainer,
  titled "ANYmal MDP Course".

This file is VENDORED from the course's own repo `eth-ainit-fs26/coding-exercises`
(branch `week3`). It is upstream-owned: treat it as read-only.

## Updating

Do NOT deep-edit `index.html` here. To change it, re-vendor: copy the latest
build over from `coding-exercises` (branch `week3`) and replace this file
wholesale.

## Registration

Registered in the ROOT `cartridges.js` as a front-screen headliner:
`{name:"ANYMAL MDP", href:"anymal-mdp/", tag:"RL", ...}` (plus a Japanese
string keyed `anymal-mdp/`). The start screen and engine (`js/arcade.js`)
read it from there; nothing in this directory needs touching to relist it.
