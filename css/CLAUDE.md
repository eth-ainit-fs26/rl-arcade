# css : the 80s arcade CRT chrome and pixel-font name overlay for the start screen

The one file here, `arcade.css`, is the look-and-feel layer of the attract-mode start screen. The
scene (starfield, frame, logo, sprites) is painted on a 320x240 backbuffer `#scene` canvas, integer-
scaled with `image-rendering:pixelated`; this CSS styles only the chrome that wraps and overlays it.

What it provides:
- `@font-face` for **Press Start 2P** (`../assets/fonts/`, `font-display:block`) and a global flat-
  pixel reset (`border-radius:0 !important`, `font-smoothing:none`, black bg, no scroll).
- The cabinet stack: `#cabinet` (letterbox) > `#glass` (sized in JS; gets mild barrel curve via
  `body.curve`) > `#scene` + `#names` + `#crt`. `#crt` adds scanlines, RGB shadow-mask, vignette,
  and a slow flicker, kept subtle so names stay legible.
- The crisp **`#names`** DOM overlay: names are NOT on the canvas (would go mushy). Per-row `.nrow`
  with a `.ntxt` span, absolutely positioned by JS pixel-exactly over the canvas list rows.
- Chrome: `#links` bar (PLAIN LIST / MUSIC / THEME / JP), touch `#pad` (▲/▼), and a
  `prefers-reduced-motion` block that kills flicker + curvature.

Contract with the root `cartridges.js` (the single content registry) via `js/arcade.js`:
- `arcade.js` reads `window.GAMES/EXTRA/VIEWS` and builds one `.nrow` per cartridge; this CSS only
  styles the hooks the engine toggles. State classes: `.sel` (selected, inverse video; canvas paints
  the bright bar), `.bundle` (the THEORY GAMES pseudo-cartridge, amber `#ffd23f`), and `.bundle.sel`.
- `#names.jp` swaps the overlay to an OS kana font stack (no kana webfont bundled); JS adds `.jp`
  when the 日本語 toggle is on and fills `.ntxt` from each cartridge's `g.jp` string in the registry.
- This file defines NO content (no game names, blurbs, sprites, or colours): names/strings come from
  `cartridges.js`, and per-row accent/number/sprite are drawn on the canvas by `arcade.js`. To change
  a game, edit `cartridges.js`; to change the cabinet/CRT/font look, edit here.
