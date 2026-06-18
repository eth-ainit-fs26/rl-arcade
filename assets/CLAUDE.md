# assets : bundled static assets for the start-screen chrome (the arcade webfont)

Part of the start-screen engine (`index.html` + `js/arcade.js` + `css/arcade.css`),
not a game. Holds the static files the chrome ships with. Today that is one font.

## Contents

- `fonts/PressStart2P-Regular.woff2` : the Press Start 2P pixel font (the chunky
  80s-arcade typeface), ~4.7 KB, bundled so the arcade renders identically
  offline / over `file://` with no Google Fonts call.

## Contract

- Registered once via `@font-face{ font-family:'Press Start 2P'; src:url(
  '../assets/fonts/PressStart2P-Regular.woff2') }` in `css/arcade.css` (note the
  `../` : the path is relative to `css/`). `font-display:block` so it never
  flashes a fallback serif before loading. That family is then used for ALL chrome
  text: the logo, badges, marquee, boot/load splashes, and the `#names` game-name
  overlay drawn pixel-exact over the canvas.
- ASCII / Latin only. Press Start 2P has NO kana glyphs, so the Japanese strings
  from the registry are deliberately NOT drawn in it: `#names.jp` and the canvas
  fall back to the OS kana font (`css/arcade.css:82`). Keep it that way (no kana
  webfont is bundled).

## Relationship to the root `cartridges.js`

One-way and decoupled: `cartridges.js` is the single content registry (game list,
names, blurbs, sprites, Japanese strings); this directory supplies only the glyphs
the chrome uses to render that content. Adding/removing a game touches ONLY
`cartridges.js`, never this folder. Add a file here only for genuinely new static
chrome (e.g. an audio cue), and wire it from `index.html`/`css`/`js`. ASCII
punctuation only in authored text (no em/en dashes, no `--` as a dash).
