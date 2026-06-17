# AI in Industry · Reinforcement Learning Arcade

An interactive arcade of reinforcement-learning visualizations for the **AI in Industry**
course (ETH Zurich), together with the lecture slides and notes. It is built for an
audience of managers with little background in formal math.

**Live:** https://eth-ainit-fs26.github.io/rl-arcade/

## The start screen

`index.html` is an 80s arcade "attract" screen. The cartridges split into two groups:

- **Front screen** (the headliners): ANYMAL MDP, Repair or Replace, Last-Minute Pricing,
  Recycling Robot, Pokemon Battle, Stale by Sundown, Critical Spare.
- **THEORY GAMES** (concept builders; select the `TH` row and press START): Casino,
  Spooky House, Darts in the Dark, Minigolf.

Controls: arrow keys or click to select, Enter / START to open, Esc to leave the THEORY
bundle. The top bar has music, screen-colour theme, a **日本語** toggle (Japanese), and a
plain-list link. Japanese can also be deep-linked with `?jp=1`.

## What teaches what

| Game | Idea it builds intuition for |
|------|------------------------------|
| ANYMAL MDP | the four pieces of an MDP: state, action, transition, reward |
| Casino | bandits; explore vs exploit (epsilon-greedy) |
| Spooky House | value and the Bellman recursion |
| Darts in the Dark | an online estimate converging (learning rate vs stability) |
| Minigolf | noisy reward feedback under stochastic outcomes |
| Repair or Replace | maintenance vs replacement, timing set by the discount gamma |
| Last-Minute Pricing | revenue management (DP, then SARSA) |
| Recycling Robot | acting on a battery budget (search / wait / recharge) |
| Pokemon Battle | the same RL lesson under a Gen-1 battle screen |
| Stale by Sundown | perishable inventory (hold / discount / dump) |
| Critical Spare | spare-parts pre-positioning before a failure strands you |

## Repository layout

- `index.html`, `cartridges.js`, `js/arcade.js`, `css/`, `assets/`: the start-screen engine.
  All content (game list, names, blurbs, sprites, Japanese strings) lives in **`cartridges.js`**,
  the single file an integrator edits.
- `<game>/`: each game is a self-contained page with its own `index.html`.
- `slides/`: the lecture deck (`rl-slides.tex` and `rl-slides.pdf`).
- `lecture_notes/`: the manager-facing notes (`reinforcement_learning.tex` / `.pdf`).
- `list.html`: a plain editorial list of the games.

## Adding a game

Edit `cartridges.js` only. The header comment in that file documents the four steps: add a
`GAMES` entry, add a pixel sprite, add its `SPR` key, and place it in `VIEWS.main` (front
screen) or `VIEWS.extra` (THEORY GAMES). The badges and counts derive automatically.

## Origin

This is the AI in Industry course's own copy of the arcade, kept separate from the SML
`classic_rl` repository. The ANYMAL, Casino, Darts, Spooky House and Minigolf visualizations
come from `eth-ainit-fs26/coding-exercises`; the remaining games are the shared RL and
business cartridges.
