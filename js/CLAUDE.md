# js : the 80s arcade start-screen engine (attract mode, menu, chrome)

`arcade.js` is the ONLY file here (`arcade.css` lives in `../css/`). It is the
canvas engine + chrome for the start screen; it holds NO content. Everything it
shows comes from the root `cartridges.js` (the single content registry), loaded
first by `../index.html`.

## What it does
- Draws the whole scene on a 320x240 backbuffer (`#scene`), integer/fractional
  scaled into `#glass` with pixelated rendering: starfield, pixel frame,
  color-cycling "CLASSIC RL" logo, badge, the game list, info blurb, prompts,
  and a looping marquee, all via a `requestAnimationFrame` loop with motion
  quantized to a frame counter. A hand-pixel 5x7 bitmap font draws in-canvas
  text; flat fills + Bayer 4x4 dithering only (no gradients/alpha).
- Game NAMES are NOT on the canvas (would be mushy at low res): a DOM overlay
  `#names` renders them in Press Start 2P, positioned pixel-exactly over each
  canvas row, and carries the click/tap targets.
- Two views: `main` (front-screen headliners) and `extra` (the THEORY GAMES
  bundle); START on the bundle row opens `extra`, ESC/Backspace returns.
  `boot()` navigates to a cart's `href` (+`index.html`), records visits in
  `localStorage` (`classicrl_visited`), and stars played carts.
- Input: keyboard (arrows/WASD/Enter, Konami code), touch swipe + `#pad`
  arrows, gamepad; chiptune SFX via Web Audio; T cycles NES/GREEN/AMBER themes.
- Attract mode: after ~20s idle (skipped under reduced-motion) it cycles title
  / high-score / demo-walk / insert-coin; any input wakes it.

## Contract with `../cartridges.js`
Reads these globals and treats them as read-only truth:
`window.GAMES` (each `{name, href, acc, tag, blurb, spr}`, plus `jp`/`jb` in JP
mode), `SPR`, `PX`, `SPRITES`, `EXTRA` (the bundle pseudo-cart), and `VIEWS`
(`.main` / `.extra`). Counts (the "N IN 1" badge, "THEORY N") derive from these.
To change content edit `cartridges.js`, never this file.

## Japanese (nihongo) mode
The 5x7 bitmap font is Latin-only, so JP mode draws the localized strings
(`g.jp` names, `g.jb`/badge/prompt text) with `fillText` in the OS kana font
(`jtext`/`jwrap`; no kana webfont is bundled) and swaps `#names` to `g.jp` via
the `.jp` class. The `日本語` button (`#jp-btn`, `toggleJP`) toggles it live.

## URL params
- `?boot=0` skips the boot splash (start straight on the menu).
- `?jp=1` starts in Japanese (same as pressing the toggle).
- Others: `?view=extra` opens the bundle, `?i=N` preselects a row, `?demo=1`
  jumps to attract, `?phase=N` holds one attract phase (QA).
