# lecture_notes : manager-facing RL lecture notes (LaTeX) for the Repair-or-Replace arcade

Self-contained LaTeX notes that teach reinforcement learning to a non-technical
(manager) audience through the running "Repair or Replace" delivery-van example,
mapped one-to-one onto the arcade's THEORY GAMES scenes.

## Key files
- `reinforcement_learning.tex` : the notes source. Standalone `article` (no
  external `.sty`/`.bib`); preamble pulls in `amsmath`, `mathtools`, `booktabs`,
  `hyperref`. Sections: Motivation, Markov decision processes, Policies and
  trajectories, accumulating reward, the Q-function and Bellman equation, SARSA,
  then Robbins-Monro and the running average. Links back to the live viz at
  `https://sml-fs26.github.io/classic_rl/repair-or-replace/`.
- `reinforcement_learning.pdf` : the compiled 10-page output (the deliverable).
- `sarsa-teaching-design.md` : design note proposing how to rework the SARSA
  section (slides §6 + notes §6) so managers *derive* the update via discovery
  activities and a Bellman->SARSA substitution morph. Not yet applied; planning only.

## Build
No Makefile; compile the single source directly (twice, for `hyperref`/refs):
```
pdflatex reinforcement_learning.tex && pdflatex reinforcement_learning.tex
```
