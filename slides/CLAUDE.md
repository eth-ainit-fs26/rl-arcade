# slides : the Beamer lecture deck for the RL arcade ("Reinforcement Learning: from one delivery van to the Bellman equation")

Animated, minimal-text, light-theme Beamer deck distilled from the course's RL
lecture notes (same section order: MDP, policies/trajectories, return,
explore/exploit, Q-function/Bellman, Robbins-Monro, SARSA). It teaches the whole
loop through one running example: a delivery van you RUN, SERVICE, or REPLACE.

## Key files
- `rl-slides.tex` : the deck. Every diagram is hand-built TikZ; formulas are
  built term by term via `\only`/`\uncover` overlay chains held in fixed-height
  `\formulaslot` boxes so the layout never jumps. Defines `\van{}` and `\act{}`
  (van wear-state and action icons that replace state/action words inline).
- `beamer-preamble.tex` : shared preamble. Light Metropolis theme (dark text on
  a white canvas, for projectors), Libertinus serif + Libertinus Math, accent
  colors, and the TikZ styles (`nodebox`, `gridcell`, `good/bad/acc fill`,
  `\takeaway`).
- `roadmap.tex` : the arcade "you are here" section-divider map. `\roadmap`
  lights every ride; `\roadmapmdp` / `\roadmapbandit` / `\roadmapbellman` /
  `\roadmapdarts` / `\roadmapsarsa` light one and dim the rest.
- `img/van/` , `img/action/` : PDF+SVG icons used by `\van` and `\act`.
- `img/roadmap/` : PNG cartridge art plus `park.png` backdrop for `roadmap.tex`.
- `img/epigraph/` : public-domain artwork for the Faust and Machado opening
  frames, so they are not bare text. All sourced from Wikimedia Commons:
  `rembrandt-faust.jpg` (Rembrandt, etching "Faust", c.\,1652, Met Museum, CC0),
  `goethe.jpg` (J.\,K.\ Stieler, "Goethe", 1828, PD), `machado-oroz.jpg` (drawing
  of Antonio Machado by Leandro Oroz, 1925, PD). Credits are printed under each
  image on the slide; no attribution is legally required (PD/CC0).
- `rl-slides.pdf` : the compiled deck (checked in).

## Build
Engine is `lualatex` (the opening shows a line of polytonic Greek that Libertinus
renders only under lualatex; the preamble alone also compiles under pdflatex).
Compile from THIS directory, twice (for the section/overlay refs):

    lualatex rl-slides.tex && lualatex rl-slides.tex

## House rules
ASCII punctuation only; no Unicode dashes in rendered prose (use a comma, colon,
parentheses, or "to"). A TikZ line segment between two coordinates is the one
allowed hyphen pair. Manager audience: spell ideas out in words, never an
`argmax` or `max` symbol.
