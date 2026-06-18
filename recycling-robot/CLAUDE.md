# recycling-robot : the Recycling Robot MDP viz (a front-screen cartridge of the rl-arcade)

A browser-only, no-build, `file://`-safe educational visualization of the
**Recycling Robot** MDP (the Sutton-Barto toy, redrawn as a battery gauge) for a
**manager audience**. It is one **front-screen cartridge** of the "AI in Industry"
reinforcement-learning arcade (`eth-ainit-fs26/rl-arcade`): it is registered in
the arcade's root `cartridges.js` (the RL-tagged game list, NOT the THEORY GAMES
bundle) and launched from the 80s arcade start screen, so it sits one level up
alongside sibling cartridges `pokemon-battle/`, `last-minute-pricing/`,
`critical-spare/`, `repair-or-replace/`, `stale-by-sundown/`. It walks the
canonical **13-scene arc** (title, tutorial, playtest, formalization, policy,
trajectory, return, Q*, Bellman, DP, DP-caveat, learning, recap).

## Design source of truth (NOT in this repo)

The full spec (exact numbers, scene-by-scene plan) is
`mdp-gallery/brainstorm/proposals/10-recycling-robot.md`, and the 13-scene DNA is
`mdp-gallery/reference/pokemon-arc.md`. **`mdp-gallery/` is a design-spec folder
that lives in the separate `SML classic_rl` repo and was NOT copied into this
arcade repo** (do not expect a `../mdp-gallery/` sibling here; those paths refer
to the other repo). This cartridge was built by mirroring the multi-file
structure, click-step scene engine, vendored KaTeX, chiptune music, EN+JP i18n,
and precompute approach of the gallery cartridges, with the gallery's **light
Press Start 2P pixel theme** (cream/ink, NOT the editorial serif theme). The
nearest still-present sibling to read for structure is `pokemon-battle/`.

## The MDP

- **State** s = the robot's **battery level**, a 5-rung gauge `s in {empty, low,
  mid, high, full}` (integers empty=0 .. full=4). `empty` is the terminal
  STRANDED state (value 0; entering it already paid the rescue). That leaves
  **4 playable rungs** (low/mid/high/full); the whole Q-table is one tall column.
- **Action** a = one of 3 levers: **SEARCH** (work, green), **WAIT** (idle,
  amber), **RECHARGE** (protect, blue). All three legal at every rung (no
  clamping), so the Q-table is a clean 4x3 (3 levers across, 4 rungs down).
- **Transition** P: on a **SEARCH** the **drain die** rolls `-1 rung w.p. 0.70`
  or `-2 rungs w.p. 0.30` (a drain reaching empty STRANDS, terminal). WAIT stays
  on the rung; RECHARGE jumps to full. Both WAIT/RECHARGE are deterministic (no
  die).
- **Reward** r: trash collected on a SEARCH = **+3 at high/full, +2 at mid/low**.
  WAIT = **+1**. RECHARGE = **0**. Stranding costs **-10**. KEY MODELLING CHOICE:
  a SEARCH that strands still collects its haul that step, then pays -10, i.e.
  `r = searchReward(s) + STRAND`. From `low` BOTH drains strand, so SEARCH-from-
  low is a certain `2 + (-10) = -8` (the proposal's canonical -8.00).
- **Horizon**: a work **shift of N = 8 steps**, `gamma = 1` (the shift length is
  the horizon, so returns are bounded without discounting). This is a
  **FINITE-HORIZON** MDP: the optimal action can depend on steps-remaining, and
  it does on the very last step.

(All of the above is enforced in `js/robot.js` / `js/levers.js` and re-asserted by
the precompute, see below.)

## The twist (state-dependent optimal action), VERIFIED EXACTLY

The best lever **marches up the gauge**. The converged optimal policy (the
start-of-shift / k=N layer, stable for all k >= 2) and its Q-values match the
proposal's stated table **exactly** (asserted by the precompute to 2 decimals):

```
rung    SEARCH    WAIT   RECHARGE   best
full    16.45    15.54    14.54     SEARCH    (push)
high    15.44    14.89    14.54     SEARCH    (push: the closest call, gap 0.55)
mid      7.71    13.44    14.54     RECHARGE  (protect)
low     -8.00    13.44    14.54     RECHARGE  (protect)
empty   terminal (STRANDED), value 0; entering it costs -10
```

Two wrinkles the proposal calls out, both verified:
- **The last-step (k=1) column differs**: with no future to protect, the safe +1
  WAIT wins at low/mid. So all three levers are genuinely optimal somewhere:
  across the 4 rungs x 8 shift steps (32 cells) the tally is **SEARCH 16,
  RECHARGE 14, WAIT 2**.
- **The marginal cell is `high`** (SEARCH 15.44 vs WAIT 14.89, gap 0.55), not
  mid; the precompute asserts the argmax there is stable (no float coin-flip) and
  that there are no exact ties.

## Layout

```
recycling-robot/
  index.html              entry; fixed script/style load order
  .gitignore              ignores .shots_tmp/ (the QA screenshot scratch dir)
  css/
    style.css             light pixel theme (cream / ink / Press Start 2P) +
                          a screen-only CRT variant; chrome, lever chips,
                          .formula-block cards, responsive @media
    gauge.css             the robot + 5-segment battery gauge + Q-table widget
    die.css               the battery-drain die popup (70/30 badge, tumble)
    scene0.css .. scene12.css   per-scene layout (13 files)
  js/
    levers.js             actions (search/wait/recharge); aliased to window.Moves
    robot.js              the MDP (state/transition/sample/successors, finite
                          horizon); window.Robot, aliased to window.Battle
    bellman.js            FINITE-HORIZON DP: per-step value layers, per-step
                          policies, the converged (k=N) headline layer, stableFrom,
                          the lever-usage tally; window.Bellman
    sarsa.js              TD-control primitives indexed by (rung, steps-left,
                          lever): on-policy SARSA `update` AND off-policy
                          `qLearningUpdate`, plus `layerAtK`; window.SARSA
    gauge.js              window.Gauge: robot+gauge state-icon + single-column
                          Q-table + paintPolicy + drain/strand/dock animations
    die.js                window.Die: roll(rng[,forced]) -> Promise<{delta}>
    katex-helpers.js      window.Katex.render/inline/display (vendored KaTeX)
    theme.js, i18n.js, i18n-ui.js, sfx.js, music.js, music-ui.js, dialog.js,
      speakerNotes.js     chrome (shared with the gallery; rr-prefixed storage keys)
    i18n/sceneN.i18n.js   per-scene EN + JP copy (register into window.I18N)
    scenes/sceneN.js      the 13 scenes (register window.scenes.sceneN)
    main.js               click-step engine: hash routing #scene=N, keyboard
                          left/right, dot pager, concept badges, speaker notes;
                          exposes window.RR
  data/datasets.js        GENERATED by precompute (window.DATA)
  precompute/build-datasets.js   the rigor gate (see below)
  vendor/katex/           KaTeX vendored (katex.min.js/.css + fonts/, no CDN)
  assets/fonts/           PressStart2P-Regular.woff2 (bundled, offline)
```

No build step. Open `index.html` from `file://`; everything (engine, KaTeX,
data, SFX, music) works offline. DotGothic16 (the JP bitmap font) loads from
Google Fonts when online and falls back gracefully offline. (Press Start 2P is
bundled locally.)

### Engine conventions (shared with the gallery)

- `window.Robot` is aliased to `window.Battle`, and `window.Levers` to
  `window.Moves`, so the reused `bellman.js` / `sarsa.js` consume them unchanged.
- The converged Q-table is `Q[stateIndex*3 + leverIdx]`, stateIndex = battery
  level - 1 (low=0..full=3), leverIdx in `[search, wait, recharge]`. The gauge
  widget renders full (top) .. low (bottom) so the gauge climbs upward (ROWS=4,
  COLS=1).
- The learned SARSA/Q-learning table is indexed by `(stateIdx, steps-left k,
  lever)` because the problem is finite-horizon; `SARSA.layerAtK(Q, k)` flattens
  one steps-left layer to the 4x3 the widget expects.
- Scenes return `{ onEnter?, onLeave?, onNextKey?, onPrevKey? }`; returning
  `true` from a key handler consumes the keystroke for an internal step.
- `#scene=N` deep-links; `&instant` disables fade; `&run` (read as `window.RR.run`)
  auto-triggers a scene's primary animation for headless capture; `&theme=light|crt`.

## The rigor gate (precompute)

`node precompute/build-datasets.js` loads the verified runtime engine via a
`window` shim (single source of truth), runs the finite-horizon DP, trains both
TD learners, **asserts**, and only then writes `data/datasets.js`. If any
assertion fails the file is NOT written. Verified assertions:

1. The converged policy is exactly full=SEARCH, high=SEARCH, mid=RECHARGE,
   low=RECHARGE.
2. The converged Q-table matches the proposal twist **exactly** (16.45 / 15.44 /
   14.54 / -8.00 ..., to 2 decimals).
3. The argmax at `high` is stable (SEARCH wins by gap ~0.55, >= 0.5) and there
   are NO exact ties among levers in the converged layer.
4. The policy is stable from the 2nd backup (k >= 2 identical); the last-step
   (k=1) column differs (WAIT wins at low/mid).
5. All three levers are optimal somewhere across 32 cells: SEARCH 16, RECHARGE
   14, WAIT 2.
6. Hand backups reproduce the table (2nd-backup-low = -8/2/3; last-step-low =
   -8/+1).
7. Off-policy Q-learning recovers the DP-optimal converged policy on all 4 rungs,
   and its greedy shift return from full lands near V*_N(full)=16.45.
8. On-policy SARSA is demonstrably MORE CONSERVATIVE: at the marginal `high` rung
   it does NOT play the bold SEARCH, and its DP agreement is strictly below
   Q-learning's.

## SARSA vs Q-learning : the honest model-free choice (scene 11, badge "TD")

The proposal asks for "SARSA that converges to the optimal policy". On this MDP
it does **not** (exactly the situation the gallery's Gambler's-Ruin proposal
hit). Established empirically and robust across seeds: the Q-gap at the marginal
`high` rung is tiny (SEARCH 15.44 vs WAIT 14.89), and **on-policy SARSA learns
the value of the eps-soft policy it actually follows**, which turns CAUTIOUS
there: an exploratory misstep from high can cascade toward stranding, so the
on-policy value of SEARCH-at-high is pulled below the safe levers. SARSA
therefore lands a conservative policy that **protects at high** (RECHARGE/WAIT)
instead of the bold SEARCH (agreement 3/4 vs DP, systematic, not noise).

The DP-optimal stripe is recovered by **off-policy Q-learning** (bootstrap on the
best next lever), which learns the value of optimal play regardless of
exploration and converges to the DP oracle exactly (4/4, return ~16.45).

So scene 11 shows the **honest SARSA-vs-Q-learning split** (cautious vs optimal,
both against the DP oracle), badge **"TD"**, and the precompute asserts
Q-learning == DP while SARSA is demonstrably more conservative at the marginal
`high` cell. Both updates live in `sarsa.js` (`update` = on-policy SARSA,
`qLearningUpdate` = off-policy). This is the truthful choice and the richer
teaching point (the cliff-walking cautious-vs-optimal distinction).

SARSA config (`SARSA_CFG` in the precompute): `constAlpha 0.05` (a constant step
that sits at the on-policy fixed point rather than decaying to Q*), `epsilon 0.15`
steady, `seed 1`, 400000 episodes with exploring starts. This is one of many
configs that show the cautious-high behaviour: ~6+ of 14 seeds reproduce it at
these params, and the direction (SARSA never bolder than DP at high) is
systematic. The Q-learning learner (`QL_CFG`) uses Robbins-Monro alpha
(`1/(1+visits)^0.7`), epsilon 0.30 decaying to 0.10, seed 20260615, 400000
episodes.

## Regenerating the data

```
node precompute/build-datasets.js
```
Re-run after any change to `levers.js` / `robot.js` / `bellman.js` / `sarsa.js`.
Payload (`data/datasets.js`, window.DATA) holds the converged V*/Q*/policy, the
last-step column, per-step DP fill frames, both learners' k=N snapshots + return
curves, a demo trajectory, the return histogram, spot-Q rows, recap copy, and the
KaTeX strings.

## QA (this Mac hangs headless Chrome)

Use the watchdog recipe (launch detached with a fresh user-data-dir, poll for
the PNG, kill the process). Shots go in `.shots_tmp/` (gitignored).
**Mobile gotcha:** old headless Chrome launched with a 390px window-size flag
does NOT emulate a mobile layout viewport (it renders at desktop width). To verify true
390px responsive layout, render the page inside a `width:390px` `<iframe>` and
screenshot that. Verified clean this way at 390px for the layout-critical scenes
(title, tutorial, Q*, DP board, TD).

**Headless-Chrome flaky `hidden`:** an author `display:flex/grid` on a class
beats the UA `[hidden]{display:none}` (equal specificity, source order). Any
element toggled via the HTML `hidden` attribute that ALSO has an author `display`
rule needs an explicit `.cls[hidden]{display:none}` guard (done for scene0 reveal,
scene3 cards, scene8 steps).
