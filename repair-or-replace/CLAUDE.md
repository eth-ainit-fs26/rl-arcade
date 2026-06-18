# repair-or-replace : the Repair-or-Replace MDP viz

A browser-only, no-build, file://-safe educational visualization of the
**Repair or Replace** fleet-maintenance MDP for a **manager audience**. It is a
**front-screen headliner** cartridge in the AI in Industry reinforcement-learning
arcade (a sibling of `critical-spare/`, `last-minute-pricing/`, `pokemon-battle/`,
`recycling-robot/`, ...). It walks the canonical scene arc (title -> tutorial ->
playtest -> formalization -> policy -> trajectory -> return -> patience knob ->
Q* -> Bellman -> DP -> DP-caveat -> SARSA -> live SARSA -> recap).

It is registered on the arcade **start screen** in the root `../cartridges.js`
(see "Registration" below); the arcade chrome and engine live in
`../index.html` and `../js/arcade.js`. This cartridge is its own self-contained
scene engine and does not depend on the arcade engine at runtime.

## The concept (one delivery van, wearing out)

OLD BESSIE the delivery van wears down a little every week. Every week you make
exactly one call: **RUN** the route, put her in for **SERVICE**, or **REPLACE**
her outright. Patch her forever and the breakdowns bleed you dry; scrap her too
early and you burn capital. The optimal call is **state dependent** (it changes
as she ages) and the **timing is set by the discount gamma**: short-sighted
owners patch forever, patient owners replace while the van still starts. The
headline surprise: at **SHAKY** the optimal call is **REPLACE even though the van
still runs**.

## The MDP

One aging van, three levers, no spares to track: the whole state is the wear
level. The reference model is `precompute/value_iteration.py`; the JS port is
`js/van.js` (and they are kept in lockstep by the precompute, see "The rigor
gate").

- **State** s = the van's **wear level**, one of **4** states:
  HEALTHY(0), WORN(1), SHAKY(2), FAILING(3). **No terminal states**: the fleet
  runs forever, optimised with discount **gamma = 0.9** (a clean infinite-horizon
  discounted return; the "weekly" framing is the narrative wrapper).
- **Action** a = three levers, cheap to expensive, all **always legal**:
  **RUN** (drive the route, earn this week's profit, risk a breakdown),
  **SERVICE** (a week in the shop, -50, no profit, wear improves), **REPLACE**
  (buy new, -130, a week offline, condition resets to HEALTHY).
- **Transition** P + reward (baked into successors; locked, mirrors
  `value_iteration.py`):
  - **RUN** earns weekly profit `REV_RUN = [95, 72, 40, 16]` (a steep cliff
    WORN 72 -> SHAKY 40). With probability `P_BD = [0.02, 0.08, 0.28, 0.55]` the
    van **breaks down** (a -280 hit ON TOP of the week's profit) and is dumped to
    FAILING; otherwise it degrades 0/1/2 levels per `DEGR[s]` (capped at FAILING).
  - **SERVICE** costs -50 and improves wear 0/1/2 levels toward HEALTHY per
    `SERV_UP[s]`: strong on a merely-worn van, weak on a clapped-out one (this is
    what lets REPLACE decisively beat SERVICE at SHAKY). Deterministic cost.
  - **REPLACE** costs -130 and resets to HEALTHY with probability 1.
- **The optimal policy (verified by value iteration at gamma = 0.9):**

  | wear | RUN | SERVICE | REPLACE | pi* |
  |---|---|---|---|---|
  | **HEALTHY** | **311.0** | 229.9 | 149.9 | RUN |
  | **WORN**    | 203.4 | **226.1** | 149.9 | SERVICE |
  | **SHAKY**   | 96.5 | 126.4 | **149.9** | REPLACE |
  | **FAILING** | -3.1 | 86.9 | **149.9** | REPLACE |

  Optimal policy: **RUN / SERVICE / REPLACE / REPLACE** (run her young, shop her
  worn, scrap her shaky). Two confident frontiers (each margin ~ +23 by
  construction). The surprise: at **SHAKY** REPLACE beats SERVICE by ~ +23 even
  though the van still earns; at **FAILING**, RUN actually **loses money**
  (Q*(FAILING, RUN) = -3.1). REPLACE's value is the same 149.9 from every state
  (it always resets to HEALTHY), so it is the floor the other two must beat.

- **The patience knob (gamma sweep):** as gamma rises, **both frontiers slide
  left** (toward bigger commitments) and never regress. Signposts:
  gamma 0.4 -> RUN RUN SVC SVC; 0.6 -> RUN RUN SVC NEW; 0.8+ -> RUN SVC NEW NEW.
  This is the "turn the patience knob" scene's slider.

## Layout

```
repair-or-replace/
  index.html              entry; fixed script/style load order
  css/
    style.css             light "paper" pixel theme (Press Start 2P) + a
                          screen-only crt (black + orange neon) variant;
                          chrome, badges, buttons, lever colours
                          (RUN calm-blue / SERVICE amber / REPLACE hot-red)
    qtable.css            the 4x3 Q-table widget
    scene0.css .. scene14.css   per-scene layout (15 files)
  js/
    actions.js            the 3-action space; window.Actions, aliased to
                          window.Moves; inline-SVG glyphs (wheel / wrench /
                          sparkle) shared with slides/img/action/*.pdf
    van.js                the MDP (state / transition / sample / successors);
                          window.Van, aliased to window.Battle
    bellman.js            value iteration (reused from the gallery via the
                          Battle / Moves aliases)
    sarsa.js              on-policy SARSA primitives (eps-greedy, the TD update)
    katex-helpers.js      window.Katex render helpers (vendored KaTeX)
    theme.js              light / crt toggle ('t', #theme=, localStorage)
    dialog.js, sfx.js, music.js, music-ui.js   chiptune + SFX + MUSIC toggle
    vanCard.js            window.VanCard: the recurring van state-icon
                          (coloured by wear), used across scenes
    qtable.js             the 4x3 Q-table widget
    chart.js, history.js  the return / convergence charts + trajectory tape
    speakerNotes.js       per-scene speaker notes (the 'n' overlay)
    scenes/scene0.js .. scene14.js   the 15 scenes (register window.scenes.sceneN)
    main.js               click-step engine: SCENES order + titles + music keys,
                          hash routing #scene=N, keyboard, dot pager, concept
                          badges, speaker notes, slide mode, quick jump, help
  data/datasets.js        GENERATED by the precompute (window.DATA); do not edit
  precompute/
    value_iteration.py    the design contract (reference VI, asserts pi*)
    build-datasets.js     the rigor gate (loads the real engine, asserts, writes
                          data/datasets.js)
  vendor/katex/           KaTeX vendored (no CDN), file://-safe
  assets/fonts/           PressStart2P-Regular.woff2 (bundled, offline)
```

No build step. Open `index.html` from `file://`; everything (engine, KaTeX,
data, SFX, chiptune) works offline.

### Engine conventions (shared with the gallery)

- `window.Van` is aliased to `window.Battle`, and `window.Actions` to
  `window.Moves`, so the reused `bellman.js` / `sarsa.js` consume them unchanged
  (A = 3 actions, N = 4 states). NOTE: `bellman.js` carries some stale "9" / "4"
  comments from a copied sibling; the live dimensions are N = 4, A = 3.
- The Q-table is a clean 4x3 (`Q[stateIdx*3 + actionIdx]`, stateIdx = wear,
  actionIdx in [run, service, replace]). All three actions are legal in every
  state (no clamping), so no null / -Infinity bookkeeping is needed.
- Scenes are builders `window.scenes.sceneN(root)` returning
  `{ onEnter?, onLeave?, onNextKey?, onPrevKey? }`; returning `true` from a key
  handler consumes the keystroke for an internal step (so PREV/NEXT and the
  arrow keys step a scene before changing scene).
- `main.js` SCENES is the **live order**, which reorders two late-built files:
  scene13 ("Turn the patience knob") sits between scene6 and scene7, and scene14
  ("SARSA: let her drive") sits between scene11 and scene12. So there are **15**
  logical scenes even though some code comments still say 13.
- Deep links / QA flags: `#scene=N`; `&instant` disables fade; `&run`
  auto-clicks a scene's `[data-run-primary]` button for headless capture;
  `&autostep=K` fires `onNextKey` K times after build; `#theme=light|crt`.
- A one-time intro modal pops only when you advance OFF the title (scene 0 ->
  scene > 0), never on an initial deep link and never under `&run`.

## The rigor gate (precompute)

The model has **two source-of-truth files** kept in lockstep:

1. `precompute/value_iteration.py` is the **design contract**: a tiny reference
   value iteration that prints the Q* grid and **asserts** the intended policy
   (RUN / SERVICE / REPLACE / REPLACE), the SHAKY replace margin (> +15), and
   both WORN frontiers (> +15). Run: `python3 precompute/value_iteration.py`.
2. `node precompute/build-datasets.js` is the **rigor gate**: it loads the real
   runtime engine (`js/actions.js`, `js/van.js`, `js/bellman.js`) under a
   `window` shim (single source of truth), runs value iteration to a tight fixed
   point, **asserts**, and only then writes `data/datasets.js`. If any assertion
   fails the file is NOT written. Deterministic (re-running gives a stable file).
   Verified assertions:
   - The full **Q* grid matches the Python contract** (to ~0.05), and the
     optimal policy is exactly **RUN / SERVICE / REPLACE / REPLACE**.
   - The **SHAKY surprise**: Q*(SHAKY, REPLACE) > Q*(SHAKY, SERVICE) + 15.
   - The **WORN frontier**: SERVICE beats both RUN and REPLACE by > 15.
   - Q*(FAILING, RUN) is **negative** (running a failing van loses money).
   - The **gamma-sweep signposts** (0.4 -> RUN RUN SVC SVC; 0.6 -> RUN RUN SVC
     NEW; 0.8 / 0.9 -> RUN SVC NEW NEW) and **monotonicity** (as gamma rises,
     each state's policy only ever moves toward a bigger commitment).
   - The **demo trajectory** (a hand-built canonical six-week tape, raw total
     +177) is a legal sequence of engine transitions.

`data/datasets.js` (`window.DATA`) carries: the static MDP config (profits,
breakdown odds, costs, gamma), the solved `policy` / `V` / `Qstar`, a 100-point
`gammaSweep` (policy + V + Q at gamma 0.00..0.99) for the patience-knob slider,
`convergence` (sweep counts + first-30-sweep DP history for the DP stepper), the
canonical `demoTrajectory`, and 6 `recap` concept cards (Bessie's voice, with
KaTeX symbols).

## Regenerating the data

```
node precompute/build-datasets.js
```

Re-run after any change to `js/actions.js` / `js/van.js` / `js/bellman.js` (and
keep `precompute/value_iteration.py` in step, since it is the contract the build
asserts against). Fast and deterministic.

## SARSA (the model-free learner)

The model-free scenes (scene11 "SARSA: the one-cell nudge" and scene14 "SARSA:
let her drive") teach the **on-policy SARSA** update
`q[s,a] <- q[s,a] + alpha*(r + gamma*q[s',a'] - q[s,a])` with eps-greedy
exploration, recovering the same three bands from nothing but driving, billing,
and breakdowns (no model of the odds). `js/sarsa.js` holds the primitives;
the recap frames it as "learn it from the logbook" against DP's "compute it if
you know the odds".

## Registration on the arcade start screen (../cartridges.js)

All arcade content lives in the root `../cartridges.js` (the single source of
truth). This cartridge appears there as:

- `window.GAMES[1]`:
  `{name:"REPAIR OR REPLACE", href:"repair-or-replace/", acc:"#9aa7ff", tag:"BIZ", blurb:"One van, four states of wear. Run it, shop it, or buy new: scrap it while it still starts, timing set by gamma."}`
- Sprite key `'van'` in `window.SPR` (same index as GAMES), with the blue van
  pixel sprite `window.SPRITES.van`.
- Placed on the **front screen** via `window.VIEWS.main` (it is a headliner, not
  a THEORY GAMES bundle entry).
- Its **Japanese** start-screen strings are in the `JP` map keyed by href:
  `'repair-or-replace/': {jp:'修理か交換か', jb:'...'}`. The `?jp=1` arcade
  toggle swaps the start-screen name/blurb to these.

Note: the **Japanese lives in the arcade's cartridges.js, not in this
cartridge**. The cartridge itself is **English-only** (no i18n folder, no kana
webfont).

## QA (this Mac hangs headless Chrome)

Use the watchdog recipe: launch detached with a fresh `--user-data-dir`, poll
for the PNG, then kill the process. To verify a true 390px mobile layout, render
the page inside a `width:390px` `<iframe>` and screenshot that (old headless
Chrome with `--window-size=390` renders at desktop width). Useful capture flags:
`#scene=N&instant`, `&run`, `&autostep=K`, `#theme=light|crt`.

## Parity checklist (vs critical-spare / the gallery)

- [x] Light Press Start 2P pixel theme, plus a screen-only crt (orange-neon)
      variant.
- [x] Vendored KaTeX (no CDN), file://-safe; PressStart2P bundled offline.
- [x] Chiptune music with the MUSIC toggle + SFX.
- [x] "BY CARLOS COTRINI" credit on the title scene.
- [x] Concept badges (MDP / POL / RTN / Q* / DP / SRS), dot pager, #scene=N
      deep-link, keyboard left/right, speaker notes ('n'), slide mode ('f'),
      quick jump ('g'), help ('?').
- [x] DP-verified precompute rigor gate (Python contract + Node build).
- [ ] Japanese: only the start-screen name/blurb (in ../cartridges.js); the
      cartridge scenes are English-only (unlike critical-spare's full EN+JP).
