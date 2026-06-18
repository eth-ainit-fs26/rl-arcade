# lecture_notes : manager-facing RL lecture notes (LaTeX) for the Repair-or-Replace arcade

Self-contained LaTeX notes that teach reinforcement learning to a non-technical
(manager) audience through the running "Repair or Replace" delivery-van example,
mapped one-to-one onto the arcade's THEORY GAMES scenes.

## Key files
- `reinforcement_learning.tex` : the notes source. Standalone `article` (no
  external `.sty`/`.bib`); preamble pulls in `amsmath`, `mathtools`, `booktabs`,
  `hyperref`. Section order mirrors the slide deck one-to-one: Motivation, Markov
  decision processes, Policies and trajectories, accumulating reward, Exploration
  and exploitation, the Q-function and Bellman equation, Robbins-Monro, SARSA
  (including its off-policy cousin Q-learning), then the running average as the
  sole appendix. Links back to the live viz at
  `https://eth-ainit-fs26.github.io/rl-arcade/repair-or-replace/`.
- `reinforcement_learning.pdf` : the compiled 12-page output (the deliverable).
  Rebuild after editing the `.tex` (see Build below) so the checked-in PDF tracks.
- `sarsa-teaching-design.md` : design note proposing how to rework the SARSA
  section so managers *derive* the update via discovery activities and a
  Bellman->SARSA substitution morph. Largely applied now in both slides and notes
  (three-bookkeepers discovery, the write-the-line build, the Bellman->SARSA
  steps); the viz-code items it lists (e.g. an A/B toggle in `sarsa.js`) remain.

## Build
No Makefile; compile the single source directly (twice, for `hyperref`/refs):
```
pdflatex reinforcement_learning.tex && pdflatex reinforcement_learning.tex
```
