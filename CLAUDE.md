# rl-arcade : AI in Industry reinforcement-learning arcade

A browser-only, no-build, file://-safe arcade of reinforcement-learning
visualizations for the **AI in Industry** course (ETH Zurich, org
`eth-ainit-fs26`), aimed at managers with little formal math, plus the lecture
slides and notes. Deploys to GitHub Pages.

Live: https://eth-ainit-fs26.github.io/rl-arcade/

## Start screen

`index.html` is an 80s arcade attract screen. Cartridges split into two groups:

- **Front screen** (headliners): ANYMAL MDP, Repair or Replace, Last-Minute
  Pricing, Recycling Robot, Pokemon Battle, Stale by Sundown, Critical Spare.
- **THEORY GAMES** (the `TH` bundle row, opens a sub-screen): Casino, Spooky
  House, Darts in the Dark, Minigolf.

`?boot=0` skips the boot splash; `?jp=1` starts in Japanese; `?view=extra` opens
the THEORY bundle.

## The one file you edit for content: cartridges.js

`cartridges.js` is the single source of truth. It exports `window.GAMES`
(`{name, href, acc, tag:"RL"|"BIZ", blurb}` plus `jp`/`jb` Japanese strings),
`SPR` (sprite key per game, same order), `SPRITES` + `PX` (pixel-art sprites),
`EXTRA` (the THEORY bundle pseudo-cartridge), and `VIEWS` (`main` = front screen,
`extra` = THEORY games). To add a game: add a `GAMES` entry, add a sprite, add
its `SPR` key, and place it in `VIEWS.main` or `VIEWS.extra`. Counts and badges
derive automatically. The engine (`js/arcade.js`, `css/arcade.css`) is chrome
only and should not need editing to add content.

## Japanese mode

The top-bar `日本語` button (and `?jp=1`) switches the game names, the info
blurb, the badge sub-title and the START/COIN prompts to Japanese, drawn with the
OS kana font (no kana webfont is bundled, so it still works offline). The big
"CLASSIC RL" logo, the "N IN 1" badge and the marquee stay as arcade chrome.

## Layout

- `index.html`, `cartridges.js`, `js/`, `css/`, `assets/` : the start-screen engine.
- `<game>/` : each game is a self-contained page with its own `index.html`.
- `slides/` : the lecture deck (`rl-slides.tex` / `.pdf`).
- `lecture_notes/` : the manager-facing notes.
- `list.html` : a plain editorial list of the games.
- Every directory carries its own `CLAUDE.md` documenting its contents.

## Origin and conventions

This is the AI in Industry course's own copy of the arcade, kept separate from
the SML `classic_rl` repo so that one is no longer tampered with. The ANYMAL,
Casino, Darts, Spooky House and Minigolf cartridges are single self-contained
HTML files vendored from `eth-ainit-fs26/coding-exercises` (branch `week3`); the
other six games are the shared multi-file scene-engine visualizations carried
over from `classic_rl`. Their design specs live in that repo under
`mdp-gallery/` (NOT copied here).

Branding: "CLASSIC RL" is the arcade's own name; "AI in Industry" is the course
(the org name `eth-ainit` reads as AI iN IndusTry). ASCII punctuation only in
authored text: no em or en dashes, and no `--` used as a dash.
