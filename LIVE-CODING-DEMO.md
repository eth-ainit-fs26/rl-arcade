# Live-coding demo: the smallest MDP + SARSA/Q-learning

A plan for building a whole MDP **and** a model-free learner (SARSA or
Q-learning) from a blank file, in front of students, in one sitting.

## Which cartridge, and why

Six arcade cartridges ship a TD learner (`sarsa.js`): recycling-robot,
repair-or-replace, stale-by-sundown, critical-spare, last-minute-pricing,
pokemon-battle. The repos are thousands of lines, but that is scene chrome,
music, i18n, KaTeX and pixel art. The part you actually live-code is the
**model** plus the **learning loop**, and on that measure the winner is:

### REPAIR OR REPLACE

| Cartridge | States | Shape | Horizon | Q-table | Illegal actions |
|---|---|---|---|---|---|
| **Repair or Replace** | **4** | **1-D (wear)** | **infinite, gamma=0.9** | **flat 4x3** | **none** |
| Recycling Robot | 4 | 1-D (battery) | finite (8 steps), gamma=1 | 3-D (s, steps-left, a) | none |
| Critical Spare | 9 | 2-D (health x spares) | infinite | 9x3 | REPLACE clamped |
| Stale by Sundown | 15 | 2-D (units x tier) | infinite | 15x3 | none |
| Last-Minute Pricing / Pokemon | many | 2-D | finite | large | varies |

Two properties make it the cheapest to write live:

1. **Infinite-horizon discounted (gamma=0.9)** so the Q-table is a flat
   `4 x 3 = 12` cells, `Q[state][action]`. Recycling Robot is the famous
   Sutton-Barto toy with the same 4x3 headline, but it is **finite-horizon**:
   its learned table is indexed `(state, steps-remaining, action)`, a 3-D array
   with a per-shift loop. More code, harder to narrate.
2. **All 3 actions are legal in every state** (no clamping), unlike Critical
   Spare which needs `-Infinity` masking for its illegal REPLACE.

Story bonus: you do not know the breakdown odds, so model-free learning is
motivated. The payoff is a real surprise: at SHAKY the optimal call is
**REPLACE even though the van still runs**.

Source of truth in the repo: model `repair-or-replace/js/van.js` (transition is
just lines 98-127); learner `repair-or-replace/js/sarsa.js` (update is lines
50-63).

## The MDP (faithful to the cartridge)

- **State** `s`: wear level, `0=HEALTHY 1=WORN 2=SHAKY 3=FAILING`. No terminals.
- **Action** `a`: `RUN`, `SERVICE`, `REPLACE`. All legal in every state.
- **Discount** `gamma = 0.9` (infinite horizon).

Constants (copy these to the board):

```
REV_RUN = [95, 72, 40, 16]      # weekly profit if you RUN, by wear
P_BD    = [0.02, 0.08, 0.28, 0.55]   # breakdown chance if you RUN
BREAKDOWN_COST = 280            # extra hit on a breakdown, then dumped to FAILING
DEGR    = [[.35,.55,.10],       # RUN survived: P(degrade 0 / 1 / 2 levels)
           [.30,.55,.15],
           [.45,.55,.00],
           [.65,.35,.00]]
SERV_UP = [[1,0,0],             # SERVICE: P(improve 0 / 1 / 2 levels)
           [.05,.70,.25],
           [.45,.50,.05],
           [.55,.42,.03]]
C_SERVICE = 50                  # SERVICE costs 50, no profit
C_REPLACE = 130                 # REPLACE costs 130, resets to HEALTHY
```

### Environment: one function

```
function step(s, a):
    if a == RUN:
        profit = REV_RUN[s]
        if random() < P_BD[s]:
            return (FAILING, profit - BREAKDOWN_COST)   # broke down
        d = sample_index(DEGR[s])                       # 0, 1 or 2
        return (min(3, s + d), profit)                  # aged, kept the profit
    if a == SERVICE:
        u = sample_index(SERV_UP[s])                    # 0, 1 or 2
        return (max(0, s - u), -C_SERVICE)              # improved, paid 50
    if a == REPLACE:
        return (HEALTHY, -C_REPLACE)                    # brand new, paid 130

# sample_index(p): return i with probability p[i] (a cumulative-sum draw)
```

That is the entire model. If you want it even shorter on the board, collapse the
two distributions to "RUN ages one level when it survives, SERVICE improves one
level" -- the qualitative policy (RUN / SERVICE / REPLACE / REPLACE) still falls
out; you lose only the exact Q* numbers.

## The learner

### Q-learning (recommended for the demo: off-policy, shortest, converges to optimal)

```
Q = zeros(4, 3)
s = HEALTHY
repeat N steps:
    a = eps_greedy(Q[s], eps)                 # explore w.p. eps, else argmax
    (s2, r) = step(s, a)
    Q[s][a] += alpha * (r + gamma * max(Q[s2]) - Q[s][a])
    s = s2

policy[s] = argmax(Q[s])    for each s

# eps_greedy(row, eps): if random() < eps return random action
#                       else return argmax(row)
```

### SARSA (the cartridge's headline learner: on-policy, a one-line change)

```
Q = zeros(4, 3)
s = HEALTHY
a = eps_greedy(Q[s], eps)
repeat N steps:
    (s2, r) = step(s, a)
    a2 = eps_greedy(Q[s2], eps)               # pick next action FIRST
    Q[s][a] += alpha * (r + gamma * Q[s2][a2] - Q[s][a])   # bootstrap on a2, not max
    s, a = s2, a2
```

The only difference: Q-learning bootstraps on `max(Q[s2])` (the best you could
do next); SARSA bootstraps on `Q[s2][a2]` (the action you will actually take).
That single token is the on-policy vs off-policy distinction -- a great thing to
flip live and discuss.

Suggested hyperparameters for a visible-in-seconds demo: `alpha = 0.1`,
`gamma = 0.9`, `eps = 0.1`, `N = 50000` steps (or anneal eps 0.3 -> 0.02). The
greedy policy should settle to **RUN / SERVICE / REPLACE / REPLACE**.

## Live-coding workflow (about 35-45 min)

1. **Frame the problem (3 min).** One delivery van, wears out weekly. Each week:
   RUN, SERVICE, or REPLACE. Ask the room for their gut policy. Plant the hook:
   "when do you scrap a van that still drives?"

2. **Name the four MDP parts (5 min).** State = wear (4 levels). Actions = 3
   levers. Reward = money that week. Transition = what wear you land in. Write
   the constants table on the board. Stress: *we are about to pretend we do not
   know `P_BD`*.

3. **Code the environment (8 min).** Type `step(s, a)` exactly as above. Test it
   by hand: RUN from HEALTHY a few times, show it usually ages and occasionally
   breaks down to FAILING with a big negative reward. SERVICE from SHAKY, REPLACE
   from FAILING. This is the whole MDP, ~15 lines.

4. **Code `eps_greedy` + the Q-table (4 min).** A `4 x 3` array of zeros and a
   five-line action picker. Explain explore vs exploit in one sentence.

5. **Code the Q-learning loop (6 min).** The four-line loop. Walk one iteration
   slowly: pick action, step, compute target `r + gamma * max(Q[s2])`, nudge
   `Q[s][a]` toward it. Emphasise: no `P_BD`, no model -- it learns from
   experience.

6. **Run it and read the policy (5 min).** Print `argmax(Q[s])` per state. It
   prints RUN / SERVICE / REPLACE / REPLACE. Land the surprise: SHAKY says
   REPLACE even though the van still earns 40/week, because the 28% breakdown
   risk (a -240 week) outweighs it.

7. **Flip to SARSA (5 min).** Change `max(Q[s2])` to `Q[s2][a2]` and pre-pick
   `a2`. Re-run, compare policies. Introduce on-policy vs off-policy. (On this
   MDP both reach the same bands, so it stays clean.)

8. **Turn the patience knob (optional, 4 min).** Lower `gamma` to 0.6 and re-run:
   the REPLACE frontier slides right (impatient owners patch longer). Shows the
   discount factor doing real work.

### What to pre-write vs type live

- **Type live:** `step`, `eps_greedy`, the Q-table init, the learning loop, the
  policy print. This is the whole point and it is only ~30 lines.
- **Pre-write (paste):** the constants block (`REV_RUN`, `P_BD`, `DEGR`,
  `SERV_UP`), and `sample_index` (a trivial cumulative-sum helper). Pasting these
  keeps the session on the ideas, not on transcribing decimals.

### Failure modes to rehearse

- Forgetting to set `s = s2` (or `s, a = s2, a2`): the agent never moves; Q for
  HEALTHY explodes. Good teachable bug.
- `eps = 0`: it gets stuck on whatever it tried first. Motivates exploration.
- Reward sign slips (forgetting the breakdown is *negative*): policy degenerates
  to always-REPLACE or never-REPLACE.
```
