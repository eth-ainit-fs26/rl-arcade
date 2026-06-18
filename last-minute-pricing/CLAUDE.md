# last-minute-pricing : the Last-Minute Pricing revenue-management MDP viz

A browser-only, no-build, file://-safe educational visualization of
**revenue management for perishable stock** (sell a seat / room / slot that
expires worthless at a midnight deadline), framed as a finite-horizon MDP for a
**manager audience**. It is one cartridge in the AI in Industry reinforcement-
learning arcade (a sibling of `critical-spare/`, `recycling-robot/`,
`stale-by-sundown/`, `pokemon-battle/`, ...). It walks the canonical **13-scene
arc** (title -> tutorial -> playtest -> formalization -> policy -> trajectory ->
return -> Q* -> Bellman -> DP -> DP-caveat -> SARSA -> recap).

It is registered on the arcade **front screen** in the root `../cartridges.js`:
the EN cartridge entry (`name: "LAST-MINUTE PRICING"`, `href:
"last-minute-pricing/"`, `tag: "BIZ"`, accent `#ff8a3c`, the "perishable stock,
a midnight deadline ... DP then SARSA" blurb) plus its Japanese title/blurb in
the same file (`'last-minute-pricing/': { jp: ..., jb: ... }`). The arcade shell
and that registry are the source of truth for the game list, names, blurbs, and
Japanese strings; this cartridge owns only its own scenes.

This cartridge was **built by cloning `pokemon-battle/`** (the 13-scene template)
and reskinning the dynamics from a battle to a pricing MDP. That ancestry is
still visible and is intentional, not a bug to "fix" blindly (see "Inherited
template detritus" below).

## The MDP

You hold a small stock of a perishable good and a few days to clear it. Each day
you pick one **price tag**, demand arrives, you sell what you can, time ticks
down. Anything unsold at the deadline is worth nothing.

- **State** s = (**units left** u, **days to deadline** d): u in {1,2,3,4,5} x
  d in {1,2,3,4} = **5 x 4 = 20 playable states**. The whole world is a **5x4
  board** (units = rows, 5 at top down to 1; days = columns, 4 at left down to
  1), so the entire Q-table / policy renders on one screen. Two ways an episode
  ends, both **off-grid terminals with value 0** (the analogue of the old
  WIN/LOSS cells): **DEADLINE** (d hits 0; leftover units score nothing) and
  **SOLD OUT** (u hits 0; the episode ends early). **gamma = 1**: the horizon is
  a hard 4 days, so undiscounted returns are already bounded and every value is
  small and hand-checkable (no discount needed for the story).
- **Action** a = two **price levers** (`js/levers.js`):
  **PREMIUM** (price 5, slow: demand draw 0 w.p. .60 / 1 w.p. .40, E ~ 0.40
  units/day) and **STANDARD** (price 2, fast: 1 w.p. .20 / 2 w.p. .40 / 3 w.p.
  .40, E ~ 2.20 units/day). Two genuinely different bets: hold out for the high
  price and sell slowly, or take the everyday price and clear stock fast.
  (STANDARD is the former FIRE-SALE tag, relabelled; a retired middle $3 tag is
  gone, so the action space is exactly 2.)
- **Transition** P: set the lever, draw demand **k** from that lever's
  distribution, **sell min(k, u)**, then time always ticks one day and inventory
  drops by what sold. The **demand draw is the only stochastic element** (no
  opponent, no accuracy roll); the odds are hidden from the player.
- **Reward** r = **price x units sold today**, paid on the transition. All
  rewards are non-negative; terminals pay 0.
- **The lesson (the optimal lever MOVES across the board), verified by value
  iteration:** it is NOT "always one tag". Both levers are optimal somewhere:
  with lots of stock and little time you **STANDARD** (clear it before it
  expires); with scarce stock and time to spare you hold out at **PREMIUM**. The
  precompute asserts two named corners: **Q*(u5,d1): STANDARD beats PREMIUM**
  (last day, dump the stock) and **Q*(u1,d4): PREMIUM beats STANDARD** (one unit,
  four days, hold for the high price). The full recovered policy fills all 20
  cells, premium-heavy in the scarce/time-rich corner and standard along the
  high-inventory / short-time seam. The two corner Q-rows ride along in
  `window.DATA.spotQ` for the scenes to quote.

## Layout

```
last-minute-pricing/
  index.html              entry; fixed script/style load order (scenes 0..12)
  css/
    style.css             the light Press Start 2P pixel house theme (warm
                          cream / hard black) shared with the arcade siblings;
                          chrome, badges, buttons, lever colours, responsive,
                          plus a screen-only CRT dark variant
    qtable.css            the 5x4 Q-table / policy board widget
    trajTree.css          the trajectory-as-tree widget
    scene0.css .. scene12.css   per-scene layout
  js/
    levers.js             the action space (PREMIUM / STANDARD: price + demand
                          distribution); window.Levers, aliased to window.Moves
    pricing.js            THE MDP: state/board geometry, step, sample (one demand
                          draw) and successors (full demand enumeration for VI),
                          Mulberry32 rng; window.Pricing, aliased to window.Battle
    bellman.js            value iteration + greedy policy + qFromV (the reused
                          solver; reads window.Battle / window.Moves)
    sarsa.js              on-policy SARSA update primitives (the reused learner;
                          eps-greedy, TD update, argmaxPolicy)
    katex-helpers.js      window.Katex.render/inline/display (vendored KaTeX)
    theme.js, i18n.js, i18n-ui.js, sfx.js, music.js, music-ui.js, dialog.js,
      speakerNotes.js     chrome (theme toggle, EN+JP i18n, chiptune, SFX, etc.)
    deck.js, chart.js, history.js, shelfCard.js, trajTree.js, qtable.js
                          shared scene widgets (a card deck, the learning-curve
                          chart, an episode-history log, the perishable-shelf
                          card, the trajectory tree, the Q-table board)
    i18n/sceneN.i18n.js   per-scene EN + JP copy (register into window.I18N)
    scenes/sceneN.js      the 13 scenes (register window.scenes.sceneN)
    main.js               click-step engine: hash routing #scene=N, keyboard
                          left/right + tappable PREV/NEXT, dot pager, concept
                          badges, speaker notes; window.PriceViz (aliased to
                          window.PokeViz for the reused chrome)
  data/datasets.js        GENERATED by precompute (window.DATA), ~174 KB
  precompute/build-datasets.js   the rigor gate (see below)
  vendor/katex/           KaTeX vendored (js + css + woff2 fonts; no CDN)
  assets/fonts/           PressStart2P-Regular.woff2 (bundled, offline)
  assets/*.png            INHERITED Pokemon sprites (template detritus; see below)
  scripts/, tests/        a headless-Chrome screenshot regression harness
                          (still labelled "pokemon-battle"; see below)
```

No build step. Open `index.html` from `file://`; everything (engine, KaTeX,
data, SFX, chiptune) works offline. The Japanese bitmap font **DotGothic16** is
loaded from Google Fonts (the one optional network asset) and is NOT bundled; it
falls back to the OS Japanese font offline.

### Engine conventions (shared with the arcade)

- **Battle/Moves aliases:** `window.Pricing` is aliased to `window.Battle`, and
  `window.Levers` to `window.Moves`, so the reused `bellman.js` / `sarsa.js`
  consume them unchanged. New scene code should read `window.Pricing` /
  `window.Levers`.
- The Q-table is a clean 20 x 2 (`Q[stateIdx * A + leverIdx]`, A = 2, leverIdx
  in [premium, standard]). `stateIndex(s) = row * NUM_DAYS + col` with
  `row = 5 - u` (units 5..1 top..bottom) and `col = 4 - d` (days 4..1
  left..right), i.e. the position in `NON_TERMINAL_STATES`, so everything aligns.
- Transitions come in two shapes (same names as the template): `sample(state,
  leverId, rng) -> { sNext, reward, terminal, log }` (one stochastic demand
  draw; used by the playtest + SARSA) and `successors(state, leverId) -> [{
  sNext, p, reward }]` (full enumeration over demand outcomes, aggregated by
  dest + reward; used by value iteration).
- Scenes return `{ onEnter?, onLeave?, onNextKey?, onPrevKey? }`; returning
  `true` from a key handler consumes the keystroke for an internal step (PREV /
  NEXT and the arrow keys both delegate to the scene first, then advance).
- Scenes must support **cold entry**: a scene reconstructs itself from
  `window.DATA` / `window.Pricing` and never assumes a prior scene ran.
- `#scene=N` deep-links; `&instant` disables the fade; `&run` sets
  `window.PRICING_AUTORUN` so a scene auto-triggers its primary animation for
  headless capture; `#theme=light|crt` and `#lang=en|jp` are handled by
  `theme.js` / `i18n.js`. Concept badges (MDP / POLICY / RETURN / Q* / DP /
  SARSA) light as you reach the relevant scene; `n` toggles speaker notes, `m`
  toggles music.

## i18n (EN + JP)

Full English + Japanese. `js/i18n.js` is the core: a private `{ en, jp }` dict
that scene fragments deep-merge into via `window.I18N.register({ en:{...},
jp:{...} })`; `I18N.t(key, vars)` looks up the current language, `I18N.setLang`
switches + persists to localStorage + notifies listeners, and `#lang=` can pin
it. Flipping language sets `body.lang-jp` (which selects the DotGothic16 font)
and calls `PriceViz.rebuildAll()` to drop every cached scene DOM and rebuild from
scratch so stale text is purged. English is the source of truth; each
`js/i18n/sceneN.i18n.js` carries the EN copy plus a JP mirror for that one scene.

## The rigor gate (precompute)

`node precompute/build-datasets.js` loads the verified runtime engine
(`js/levers.js` + `js/pricing.js` + `js/bellman.js`) via a Node `vm` `window`
shim (single source of truth, it does NOT reimplement the dynamics), runs value
iteration, trains SARSA, **asserts**, and only then writes `data/datasets.js`. If
any assertion fails the file is NOT written. Deterministic / seeded (re-running
gives a byte-identical file). Verified assertions:

1. **VI converges** (maxDelta < 1e-6) within 6 sweeps (it converges in ~4, one
   per day, sweeping the board right to left).
2. The optimal policy is **non-trivial**: BOTH levers are optimal somewhere on
   the board (not "always one tag").
3. Lever usage **covers all 20 cells**.
4. **Q*(u5,d1): STANDARD beats PREMIUM** (5 units, last day: clear the stock).
5. **Q*(u1,d4): PREMIUM beats STANDARD** (1 unit, 4 days: hold for the price).
6. **SARSA's learned greedy policy, run from a fresh shelf, reaches >= 88% of
   the optimal start value** V(u5,d4) and reproduces the optimal lever on
   **>= 0.65 of cells**. The residual disagreements are the tight diagonal-seam
   near-ties (see SARSA note below).

Payload `window.DATA` shape: `policy[20]`, `V[20]`, `Qstar[20*A]`
(stateIndex*A+leverIdx), `levers[]`, `leverIds`, `gamma`, `dims`,
`nonTerminalStates[]`, `recap[6]` (shelf-card voice), `demoTrajectory[]` (one
seeded optimal-policy episode for the tutorial / trajectory scenes), `spotQ` (the
two named corner Q-rows), `valueIteration{}` (per-sweep V history for the DP
scene), `sarsa{}` (config, reward/days per episode, visit counts, snapshots, the
greedy-revenue-from-fresh-shelf convergence curve, stats), and `tex{}` (shared
KaTeX strings).

## SARSA here is the honest "good enough, not exact" path

The model-free scene uses **on-policy SARSA** (scene 11, badge "SARSA"), trained
with **exploring starts** (random start state each episode so every one of the
20 cells is well visited), a geometric epsilon decay (0.30 -> 0.01), alpha = 0.08,
gamma = 1, 40000 episodes. Unlike some siblings (e.g. `critical-spare`, where the
precompute asserts SARSA == DP on every state), SARSA here does **not** match the
DP optimum exactly: the assertion is the softer "reaches >= 88% of the optimal
start revenue AND agrees with the DP lever on >= 65% of cells". The disagreements
are confined to the **tight diagonal seam** where PREMIUM and STANDARD are nearly
tied: on-policy SARSA with residual exploration is evaluating an epsilon-soft
policy, which flips the argmax on near-tie cells. That is correct RL behaviour
(the on-policy value of a near-tie cell legitimately differs from the greedy
optimum), not a bug, and the scene is built to tell that honest story; DP nails
those seam cells exactly. The headline convergence metric the SARSA scene plots
is `sarsa.greedyRevenueCurve`: the revenue of the *current greedy* policy run
from a fresh (u5,d4) shelf, sampled through training (this is comparable to the
optimum; the raw per-episode reward is not, because exploring starts average over
random start cells).

## Regenerating the data

```
node precompute/build-datasets.js
```
Re-run after any change to `levers.js` / `pricing.js` / `bellman.js` /
`sarsa.js`. Deterministic; prints the recovered 5x4 policy grid, the two corner
Q-rows, the SARSA-vs-VI agreement and seam ties, then writes `data/datasets.js`
in place (or aborts if an assertion fails).

## Inherited template detritus (cloned from pokemon-battle)

This cartridge was reskinned from `pokemon-battle/` and some template artefacts
remain. Be aware before "cleaning up":

- `js/bellman.js` and `js/sarsa.js` still carry **stale Pokemon header comments
  and hard-coded "9 states x 4 moves"** wording. They are nonetheless **correct
  for this MDP**: they read `window.Battle.NON_TERMINAL_STATES` (20 here) and
  `window.Moves.MOVE_IDS` (2 here) at runtime via the aliases, so the comments
  lie but the code is generic. The precompute uses the SAME `bellman.js` and
  asserts correctness, so do not "fix" the logic; only the comments are wrong.
- `assets/*.png` are the old **Pikachu / Charizard sprites**; the pricing scenes
  do not use them (state is drawn as the units x days shelf board). They are
  dead weight kept from the clone.
- `scripts/README.md` and `tests/shot.mjs` (the headless screenshot regression
  harness) still say **"pokemon-battle"** in their example commands and header;
  the harness itself works against whatever `index.html` is served.

## QA (this Mac hangs headless Chrome)

`tests/shot.mjs` (Playwright) captures a scene at a given theme/width;
`scripts/regress-screenshots.sh` drives it over all scenes against committed
baselines under `tests/shots/baseline/` and flags any scene whose PNG size
drifts > 6% (a cheap, ImageMagick-free layout-break detector). Launch detached
with a fresh `--user-data-dir`, poll for the PNG, and kill the process (this Mac
hangs an attached headless Chrome). **Mobile gotcha (general to the arcade):**
old headless Chrome with `--window-size=390` does NOT emulate a mobile layout
viewport (it renders at desktop width); to check true 390px responsiveness,
render the page inside a `width:390px` `<iframe>` and screenshot that. The 5x4
board (20 cells x 2 lever-chips x values) is the densest widget and must fit a
phone.

## Parity checklist (vs the arcade siblings)

- [x] Light Press Start 2P pixel theme, visually consistent with the siblings.
- [x] Screen-only CRT dark variant.
- [x] Vendored KaTeX (no CDN), file://-safe.
- [x] Full EN + 日本語 (all 13 scenes; DotGothic16 for kana, network font with
      OS fallback).
- [x] Chiptune music with the MUSIC toggle + SFX.
- [x] Concept badges (MDP / POLICY / RETURN / Q* / DP / SARSA), dot pager,
      #scene=N deep-link, keyboard + tappable PREV/NEXT, speaker notes (`n`).
- [x] DP-verified precompute rigor gate (asserts the non-trivial moving-optimum
      policy + the two named corner Q-values; SARSA on the honest >= 88% path).
- [x] Registered on the arcade front screen in `../cartridges.js` (EN + JP).
```
