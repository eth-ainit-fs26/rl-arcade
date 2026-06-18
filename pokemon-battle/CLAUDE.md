# pokemon-battle : the Pokemon Battle MDP viz (Gen-1 Red/Blue dress)

A browser-only, no-build, file://-safe educational visualization of a
Pikachu-vs-Charmander **Gen-1 battle** as a Markov decision process, for the
same audience as the rest of the gallery. The concept is "the same RL lesson
dressed as a Game Boy battle screen": HP bars are the state, the four-move menu
is the action set, the damage rolls are the transitions. It is one cartridge in
the AI in Industry reinforcement-learning gallery (a sibling of
`critical-spare/`, `casino/`, `spooky-house/`, `darts/`, `minigolf/`,
`stale-by-sundown/`, ...) and is the "front screen" cartridge: the battle frame
is the gallery's most recognizable cover.

It is registered on the **arcade start screen** in the root `../cartridges.js`:

- `window.GAMES` entry (line ~25): `{name:"POKEMON BATTLE", href:"pokemon-battle/",
  acc:"#ffe000", tag:"RL", blurb:"A wild CHARMANDER appeared! The same RL lesson
  under a Gen-1 Red/Blue battle screen."}`.
- Japanese strings in the same file's `JP` map (line ~97):
  `'pokemon-battle/': {jp:'ポケモンバトル', jb:'野生のヒトカゲがあらわれた！...'}`
  (a forEach grafts `jp`/`jb` onto the matching `GAMES` entry).

The root engine `../js/arcade.js` reads `cartridges.js` to paint the cover and
deep-link into `pokemon-battle/index.html`. Nothing about this cartridge's
internals is known to the arcade beyond that one registration row.

It walks an **11-scene arc** (title -> tutorial -> battle -> MDP overlay ->
trajectory -> return & Q* -> pi* from Q -> DP fill -> why DP does not scale ->
deriving SARSA -> recap).

## The MDP

A single Gen-1 battle: Pikachu (the agent) vs a wild Charmander (the
environment). Pikachu always moves first (Gen-1 base speed); if the opponent
survives the hit it counter-attacks the same turn.

- **State** s = (your HP bucket, opponent HP bucket). HP is fully discretised
  into **5 buckets** {FULL (0), HIGH (1), MID (2), LOW (3), CRITICAL (4)};
  bucket 5 = FAINTED = off-grid terminal. So 5 x 5 = **25 non-terminal states**,
  laid out as a **5x5 grid** (your HP = rows, opponent HP = columns) so the whole
  Q-table renders on one board. There is **no continuous HP underneath**: the
  world the agent sees IS the world it lives in, so Markov holds exactly.
- **Terminal states**: WIN (opponent faints, reward **+10**) and LOSS (Pikachu
  faints, reward **-10**), both absorbing with V = 0 (the reward was paid on
  entry). This is an **episodic** MDP (unlike the ongoing-operation siblings),
  optimised with discount **gamma = 0.9** by default.
- **Reward** R: **-1 per non-terminal turn** (a step cost that rewards fast
  wins), **+10** on a win, **-10** on a loss.
- **Action** a = one of Pikachu's moves, ordered "more damage, less reliable"
  left to right (`accuracy` is the real hit probability; on a hit the damage is
  a bucket-drop distribution; the canon `power` field is flavour, not surfaced):

  | move | accuracy | on-hit bucket drop (baseline form) |
  |---|---|---|
  | **QUICK ATTACK** | 1.00 | drop 0 (55%) / drop 1 (45%) (weak, always lands) |
  | **THUNDERBOLT**  | 1.00 | drop 1 (50%) / drop 2 (50%) (reliable workhorse) |
  | **THUNDER**      | 0.55 | drop 2 (50%) / drop 3 (50%) (risky power play) |

- **The twist (state-dependent optimal move):** the optimal policy is **not a
  single move everywhere**. With a discount of 0.9 the agent trades reliable
  chip damage against risky burst depending on the HP cell (and, in the runtime,
  on which form the opponent has evolved into; see below). The precompute
  asserts the optimal policy at gamma = 0.9 uses **>= 2 distinct moves** across
  the 25 states, and that the policy at gamma = 0.30 differs from gamma = 0.99 in
  **>= 3 states** (patience changes the call).

### Two MDP definitions live in this repo (read this before editing numbers)

The runtime engine and the precompute currently model the opponent
**differently**. Both are internally consistent; they are NOT byte-identical
MDPs.

- **Runtime** (`js/battle.js` + `js/moves.js`, what the page plays): an
  **evolving 3-form opponent**. The Charmander evolves with its own HP bucket:
  CHARMANDER (FULL/HIGH) -> CHARMELEON (MID) -> CHARIZARD (LOW/CRITICAL). Each
  form has its own type-effectiveness table on Pikachu's three moves AND its own
  counter move (EMBER / FLAMETHROWER / OUTRAGE). Evolution can fire mid-turn:
  Pikachu's damage is keyed by the form *before* the hit, the counter by the
  form *after*. Action set = **3 moves** (quick_attack, thunderbolt, thunder).
- **Precompute** (`precompute/build-datasets.js`, what fills `data/datasets.js`):
  the older **static single-form** Charmander. EMBER counter everywhere, no
  evolution, and a **4-move** set that includes an extra **IRON TAIL**
  (acc 0.75, drop 1 70% / drop 2 30%). So `data/datasets.js` (V*, Q*, policy,
  SARSA curves) describes the 4-move static model, not the 3-form model the
  battle scene simulates live.

When changing the MDP, decide which is authoritative and reconcile both, or the
DP/SARSA scenes that read `window.DATA` will narrate a different game than scene
2 plays. Heads-up doc bugs in the source comments (the code is right, the
comments are stale): `js/bellman.js` and `js/sarsa.js` headers say "9-state" /
"9 states" but `N = window.Bellman.STATES.length` is **25**; `js/main.js`'s
top comment says "7 scenes" but the `SCENES` array has **11**.

## Layout

```
pokemon-battle/
  index.html              entry; fixed script/style load order, light theme
  css/
    style.css             light Press Start 2P pixel theme + a screen-only CRT
                          (black + orange neon) variant; chrome, topbar, dot
                          pager, badges, .poke-btn, overlays, responsive
    scene0.css            title screen
    sceneHowToPlay.css    tutorial
    scene1.css            the live battle (sprites, HP boxes, move menu)
    sceneConcepts.css     the MDP-overlay / objective / Q* essay scenes
    qtable.css            the 5x5 Q-table board widget
    sceneDp.css           DP-fill scene
    sceneSarsaDerive.css  SARSA-derivation scene
    scene5.css            recap / champion screen
    trajTree.css          the trajectory-tree widget
  js/
    moves.js              window.Moves: the 3-move action set (+ opponent move),
                          type icons, button sub-line html
    battle.js             window.Battle: the MDP (state/transition/sample/
                          successors) with the evolving 3-form opponent;
                          Mulberry32 rng shared with the precompute
    bellman.js            window.Bellman: value iteration over the 25 states
                          (sweep, VI, greedy policy, Q from V); reads Battle
    sarsa.js              window.SARSA: on-policy TD-control primitives
                          (eps-greedy, update, argmax policy, snapshots)
    qtable.js             window.* : the 5x5 Q-table board (per-cell battle
                          thumbnail + per-move Q-bars + deltas + move-freq strip)
    trajTree.js           window.TrajTree: engine-agnostic trajectory-as-tree
                          widget (E[G_t] as the weighted leaf sum)
    chart.js              tiny SVG learning-curve chart (episode vs reward + MA)
    hpbar.js, sprite.js, dialog.js, history.js   battle chrome: 5-segment HP
                          bar, sprite shake/faint, typewriter dialog box, the
                          per-scene action-History (prev = reset+replay)
    katex-helpers.js      window.Katex.render (vendored KaTeX, never throws)
    theme.js              window.Theme: light <-> crt, 't' hotkey, #theme= override
    i18n.js               window.I18N: ALL copy, EN + JP, in one STRINGS dict
    i18n-ui.js            language toggle button wiring
    music.js, music-ui.js, sfx.js   chiptune soundtrack (per-scene track) +
                          Web Audio SFX synth (no ripped audio) + MUSIC toggle
    trainer.js            window.Trainer: trainer name + concept badges,
                          persisted to localStorage
    speakerNotes.js       window.SpeakerNotes: lecturer crib sheet ('n' overlay;
                          note bodies actually live in i18n.js, localised)
    sprite.js + assets    Charmander/Charmeleon/Charizard + Pikachu sprites
    scenes/sceneX.js      the 11 scenes (each registers window.scenes.<key>)
    main.js               click-step engine: hash routing #scene=N, keyboard
                          left/right, dot pager, badges, speaker notes, slide
                          mode ('f'), quick-jump ('g'), help ('?'), boot anim
  data/datasets.js        GENERATED by precompute (window.DATA): VI history,
                          SARSA snapshots + curves, recap copy, KaTeX strings
  precompute/build-datasets.js   the rigor gate (see below)
  vendor/katex/           KaTeX vendored (no CDN)
  assets/                 sprite PNGs (modern + -gen1 pixel variants) and
    fonts/PressStart2P-Regular.woff2   bundled pixel font, offline
  scripts/, tests/        screenshot regression (regress-screenshots.sh,
                          shot.mjs, tests/shots/) for QA
```

No build step. Open `index.html` from `file://`; the engine, KaTeX, generated
data, chiptune, and SFX all work offline. (**DotGothic16**, the Japanese bitmap
font, is the one optional network asset, pulled from Google Fonts; it falls back
to the OS Japanese font offline.)

### Engine conventions (shared with the gallery)

- `window.Battle` is the MDP surface (`successors(s,a) -> [{sNext,p,reward}]` for
  VI; `sample(s,a,rng) -> {sNext,reward,terminal,log}` for SARSA + the live
  battle). `window.Bellman` and `window.SARSA` consume it. The 5x5 board reads
  `Battle.NUM_BUCKETS`, so the widget code is bucket-count agnostic.
- The Q-table is a flat **25 x A** array (`Q[stateIdx*A + moveIdx]`,
  stateIdx = your*5 + opp). A is **3** at runtime, **4** in the precompute (the
  IRON TAIL divergence above).
- Scenes register `window.scenes.<key> = function(root){ return { onEnter?,
  onLeave?, onNextKey?, onPrevKey? } }`. Returning `true` from a key handler
  consumes the keystroke for an internal step (e.g. stepping the action history);
  returning false lets the driver change scene. Scene keys are kept stable
  (scene0, sceneHowToPlay, scene1, sceneMdpOverlay, ...) so `#scene=N`
  deep-links survive reorderings.
- URL flags: `#scene=N` deep-links; `&instant` disables the cross-fade;
  `&theme=light|crt` overrides the theme; `&lang=jp` overrides the language
  (for screenshots); `&skipboot` (alias `&run`) skips the boot animation AND
  suppresses the trainer-name modal for headless capture. (Note: there is no
  auto-animation trigger flag here, unlike some siblings; `&run` only quiets the
  boot/modal chrome.)
- Hotkeys (from `main.js`): left/right = step/scene; `n` = speaker notes;
  `f` = slide mode (hide topbar); `g` = quick-jump scene list (number keys jump);
  `?` = help overlay; `m` = music; `t` = theme; Esc closes overlays.

## Internationalisation (EN + JP, one dict)

Unlike the siblings that split copy into `i18n/sceneN.i18n.js` files, this
cartridge keeps **everything in one `js/i18n.js`**: a single `STRINGS` object
with `en:` and `jp:` sub-dicts (each ~hundreds of keys). Every user-visible
string flows through `I18N.t(key, vars)` ({var} placeholders), so the `日本語`
toggle repaints the whole page (scene essays, tutorial dialog, DP/SARSA
narration, recap, speaker notes, help, trainer modal, HP-bucket labels, HUD),
not just the chrome. The KaTeX formulas stay in pure maths (symbols cross
languages). Japanese uses Gen-1-era kana phrasing (no kanji) with the canonical
move/Pokemon names (10まんボルト, ピカチュウ, ヒトカゲ). On language change,
`main.js` `rebuildAll()` drops and rebuilds every cached scene so no stale-language
DOM survives. Persisted to `localStorage('pokeviz-lang')`.

## The rigor gate (precompute)

`node precompute/build-datasets.js` defines the MDP (the **4-move static**
variant), runs value iteration on a 7-point gamma grid
[0.30, 0.50, 0.70, 0.80, 0.90, 0.95, 0.99], trains SARSA, **asserts**, and only
then writes `data/datasets.js`. If any assertion fails the file is NOT written.
Seeded Mulberry32 (pinned `seed = 20260512`) so re-running gives a
byte-identical file. Asserted invariants:

1. VI converges (max-deltaV < 1e-3) within 80 iters at every gamma.
2. The optimal policy at gamma = 0.90 uses **>= 2 distinct moves** across the 25
   states (the twist is real).
3. The policy at gamma = 0.30 differs from gamma = 0.99 in **>= 3 states**
   (patience changes the call).
4. SARSA learns: mean reward over the last 500 episodes minus the first 50 is
   **>= 5**.
5. SARSA win rate over the last 500 episodes is **>= 0.85**.
6. SARSA-vs-VI policy agreement on well-visited states (>= 5 visits) is
   **>= 0.70** (on-policy SARSA approaches, but is not asserted to exactly equal,
   the DP optimum).
7. Byte-identical regeneration given the pinned seed.

SARSA config: alpha = 0.20, gamma = 0.90, epsilon = 0.15, 5000 episodes,
snapshots at [0, 1, 5, 25, 100, 500, 2000, 5000]. Payload ~50 KB (per-gamma VI
history, final V/policy per gamma, full per-episode reward/win/turns arrays,
8 SARSA Q-snapshots, visit counts, recap copy, KaTeX strings).

### Regenerating the data

```
node precompute/build-datasets.js
```

Re-run after any change to the precompute's MDP. **Important:** edits to the
runtime `js/battle.js` / `js/moves.js` do NOT propagate to `data/datasets.js`
because the precompute carries its own copy of the MDP (and a different
opponent/action model). To make the DP/SARSA scenes match the live battle, the
two definitions must be reconciled first.

## SARSA path (on-policy, the model-free learner)

Like most siblings this cartridge takes the **on-policy SARSA path** (the
penultimate scene is "Deriving SARSA", badge `SAR`), not the
SARSA-vs-Q-learning split. The precompute asserts SARSA *learns* (reward gap,
win rate) and *agrees with VI on well-visited states* (>= 0.70), rather than the
stricter "SARSA == DP on every state" some other cartridges assert; the
episodic +10/-10 terminal structure with a -1 step cost makes the winning policy
the clearly dominant one in the cells the agent actually visits.

## QA (this Mac hangs headless Chrome)

Use the bundled screenshot harness: `scripts/regress-screenshots.sh` +
`tests/shot.mjs` (output under `tests/shots/`, gitignored). Same hard-won Mac
rule as the siblings: launch headless Chrome **detached** with a fresh
`--user-data-dir`, poll for the PNG, then kill the process (it writes the file
then hangs). For screenshots use `&skipboot&instant` so the boot animation and
the cross-fade do not race the capture, and `&lang=jp` / `&theme=crt` to grab the
Japanese and CRT variants. The densest widget is the 5x5 Q-table (25 cells x per-
move Q-bars + a battle thumbnail per cell); verify it still fits a phone.

## Parity checklist (vs critical-spare / casino)

- [x] Light Press Start 2P pixel theme, consistent with the siblings.
- [x] Screen-only CRT (black + orange neon) dark variant.
- [x] Vendored KaTeX (no CDN), file://-safe.
- [x] Full EN + 日本語 (all 11 scenes; DotGothic16 bitmap font for kana).
- [x] Chiptune music with the MUSIC toggle + Web Audio SFX (no ripped audio).
- [x] "BY CARLOS COTRINI" credit on the title scene.
- [x] Concept badges (MDP/RTN/Q*/DP/SAR), dot pager, #scene=N deep-link,
      keyboard left/right, speaker notes ('n'), slide mode ('f'),
      quick-jump ('g'), help ('?').
- [x] Seeded precompute rigor gate writing data/datasets.js.
- [x] Registered on the arcade start screen in ../cartridges.js (EN + JP).
- [ ] Runtime MDP (3-form, 3-move) and precompute MDP (static, 4-move) are NOT
      yet reconciled, see "Two MDP definitions" above.
