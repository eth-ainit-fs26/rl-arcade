# casino : the CASINO theory game (multi-armed bandits, explore vs exploit)

A THEORY GAMES cartridge in the RL arcade. It builds intuition for the
**multi-armed bandit** problem: five slot machines with hidden payoff odds.
You pull levers by hand to learn which arm is best, then watch an
**epsilon-greedy** policy trade off **exploring** new arms against
**exploiting** the one that currently looks best.

## What's here

- `index.html` : the whole game. A SINGLE self-contained, fully offline HTML
  (~840 lines): all CSS is inline, there is no build step, and there are no
  sidecar assets or external script/style/CDN references.

## This is vendored, do not deep-edit

`index.html` is VENDORED from the course's `eth-ainit-fs26/coding-exercises`
repo (branch `week3`). It is upstream-owned. To change the game, edit it
THERE and **re-vendor** (copy the fresh `index.html` over this one) rather
than hand-editing the copy here, so the two do not drift.

## Registration

The cartridge is registered in the root `cartridges.js` (not here): its
`casino/` entry sits in the THEORY GAMES block (`window.GAMES`), with its
sprite, accent colour, blurb, and Japanese strings (`JP['casino/']`). It
opens from the THEORY GAMES bundle on the arcade's theory screen. See the
root `CLAUDE.md` for the project overview and how cartridges are wired.
