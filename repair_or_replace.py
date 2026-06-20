"""
Repair or Replace -- a tiny reinforcement-learning demo.

One delivery van wears out, week by week. Every week we make ONE choice:
    RUN      drive the route, earn money, risk a breakdown
    SERVICE  spend a week in the shop, pay 50, the van gets better
    REPLACE  buy a new van, pay 130, start fresh

We do NOT tell the program the breakdown odds. It learns a good policy
just by trying things and seeing what they pay. That learning rule is
called Q-learning.

Run it with:  python3 repair_or_replace.py
"""

import random
import time


# ---------------------------------------------------------------------------
# 1. THE WORLD (the MDP)
# ---------------------------------------------------------------------------

# The van's condition is one number: 0, 1, 2 or 3.
HEALTHY = 0
WORN    = 1
SHAKY   = 2
FAILING = 3

STATE_NAMES = ["HEALTHY", "WORN", "SHAKY", "FAILING"]

# The three things we can do.
RUN     = 0
SERVICE = 1
REPLACE = 2

ACTION_NAMES = ["RUN", "SERVICE", "REPLACE"]

# Money the van earns this week if we RUN it, depending on its condition.
RUN_PROFIT = [95, 72, 40, 16]

# Chance the van breaks down this week if we RUN it (higher when older).
BREAKDOWN_CHANCE = [0.02, 0.08, 0.28, 0.55]

# A breakdown costs this much on top of losing the week, and wrecks the van.
BREAKDOWN_COST = 280

# If we RUN and the van does NOT break down, how many levels it wears this week.
# Each row is one condition. The three numbers are the chances of wearing
# 0 levels, 1 level, or 2 levels.
WEAR_CHANCES = [
    [0.35, 0.55, 0.10],   # HEALTHY
    [0.30, 0.55, 0.15],   # WORN
    [0.45, 0.55, 0.00],   # SHAKY
    [0.65, 0.35, 0.00],   # FAILING
]

SERVICE_COST = 50    # what a week in the shop costs

# How well a SERVICE helps, by condition. The three numbers are the chances of
# improving 0 levels, 1 level, or 2 levels. Notice SERVICE barely helps once the
# van is SHAKY or FAILING -- that is what will make REPLACE the better call there.
SERVICE_CHANCES = [
    [1.00, 0.00, 0.00],   # HEALTHY (nothing to fix)
    [0.05, 0.70, 0.25],   # WORN (works well)
    [0.45, 0.50, 0.05],   # SHAKY (often does not help)
    [0.55, 0.42, 0.03],   # FAILING (mostly stuck)
]

REPLACE_COST = 130   # what a brand-new van costs


def pick(chances):
    """
    Pick a number (0, 1 or 2) at random, using the given chances.
    Example: pick([0.7, 0.3, 0.0]) returns 0 most of the time, 1 sometimes.
    """
    r = random.random()
    running_total = 0.0
    for i in range(len(chances)):
        running_total = running_total + chances[i]
        if r < running_total:
            return i
    return len(chances) - 1


def step(state, action):
    """
    Do one week. Take the current condition and the choice we made,
    and return two things: the new condition, and the money we got
    (a profit is positive, a cost is negative).
    """

    if action == RUN:
        profit = RUN_PROFIT[state]

        # Roll the dice: did the van break down?
        if random.random() < BREAKDOWN_CHANCE[state]:
            # Breakdown: we still earned the profit, but pay a big repair
            # bill and the van ends up FAILING.
            reward = profit - BREAKDOWN_COST
            new_state = FAILING
        else:
            # No breakdown: we keep the profit, but the van wears a little.
            reward = profit
            levels_worse = pick(WEAR_CHANCES[state])
            new_state = state + levels_worse
            if new_state > FAILING:
                new_state = FAILING
        return new_state, reward

    if action == SERVICE:
        # A week in the shop: pay 50, the van may improve by 0, 1 or 2 levels.
        reward = -SERVICE_COST
        levels_better = pick(SERVICE_CHANCES[state])
        new_state = state - levels_better
        if new_state < HEALTHY:
            new_state = HEALTHY
        return new_state, reward

    if action == REPLACE:
        # Buy a new van: pay 130, condition resets to HEALTHY.
        reward = -REPLACE_COST
        new_state = HEALTHY
        return new_state, reward


# ---------------------------------------------------------------------------
# 2. THE LEARNER (Q-learning)
# ---------------------------------------------------------------------------

# How much we value future money compared to money right now (0.9 = patient).
GAMMA = 0.9

# How often we try a random action instead of the best one (to keep exploring).
EPSILON = 0.15

# As it learns, we print the policy a few times so the class can watch it
# settle. This is the pause (seconds) between those snapshots. Set to 0 for
# an instant run.
SNAPSHOT_PAUSE = 0.5

# The Q-table: for every state and every action, our current guess of how
# good that choice is. Start every guess at 0.
# Q[state][action] is one number.
Q = [
    [0.0, 0.0, 0.0],   # guesses for HEALTHY: RUN, SERVICE, REPLACE
    [0.0, 0.0, 0.0],   # guesses for WORN
    [0.0, 0.0, 0.0],   # guesses for SHAKY
    [0.0, 0.0, 0.0],   # guesses for FAILING
]

# How many times we have tried each choice. We use this to average:
# a guess is just the average of every outcome we have seen for that choice.
TIMES_TRIED = [
    [0, 0, 0],   # HEALTHY
    [0, 0, 0],   # WORN
    [0, 0, 0],   # SHAKY
    [0, 0, 0],   # FAILING
]


def best_action(state):
    """Return the action with the highest guess for this state."""
    best = 0
    for action in [RUN, SERVICE, REPLACE]:
        if Q[state][action] > Q[state][best]:
            best = action
    return best


def best_value(state):
    """Return the highest guess for this state."""
    return Q[state][best_action(state)]


def choose_action(state):
    """
    Most of the time pick the action we think is best (exploit).
    Sometimes pick a random action to keep learning (explore).
    """
    if random.random() < EPSILON:
        return random.choice([RUN, SERVICE, REPLACE])
    else:
        return best_action(state)


def policy_row(label):
    """Print one line: the current best choice in each of the four conditions."""
    cells = "".join("%-10s" % ACTION_NAMES[best_action(s)]
                    for s in [HEALTHY, WORN, SHAKY, FAILING])
    print("%13s   %s" % (label, cells))


def train(weeks):
    """
    Run the van for many weeks, updating our guesses as we go.

    Every so often we print the current best choice in each condition, so the
    class can WATCH the policy being learned: it starts as nonsense (everything
    looks like RUN, because every guess is still 0) and settles down to the
    answer as the bills come in.
    """
    snapshots = {200, 600, 5000, 30000, weeks}

    # Header + the untrained policy. Every guess starts at 0, so at first the
    # van just defaults to RUN in every condition: it has seen no bills yet.
    header = "".join("%-10s" % STATE_NAMES[s]
                     for s in [HEALTHY, WORN, SHAKY, FAILING])
    print("%13s   %s" % ("", header))
    policy_row("start")

    state = HEALTHY
    for week in range(1, weeks + 1):
        action = choose_action(state)
        new_state, reward = step(state, action)

        # What we now think this choice was worth:
        # the money we got, plus the discounted value of where we ended up.
        target = reward + GAMMA * best_value(new_state)

        # Nudge our old guess toward that target. The nudge gets smaller the
        # more times we have tried this choice, so the guess settles down to
        # the average of all the outcomes we have seen.
        TIMES_TRIED[state][action] = TIMES_TRIED[state][action] + 1
        step_size = 1.0 / TIMES_TRIED[state][action]
        old_guess = Q[state][action]
        Q[state][action] = old_guess + step_size * (target - old_guess)

        # Move on to next week.
        state = new_state

        # Now and then, freeze and show what the van would do today.
        if week in snapshots:
            policy_row("{:,} wks".format(week))
            time.sleep(SNAPSHOT_PAUSE)


# ---------------------------------------------------------------------------
# 3. RUN IT AND SHOW THE RESULT
# ---------------------------------------------------------------------------

def show_policy():
    """Print the learned table and the best choice in each condition."""
    print()
    print("Learned values (higher is better):")
    print("condition       RUN    SERVICE   REPLACE     best choice")
    for state in [HEALTHY, WORN, SHAKY, FAILING]:
        name = STATE_NAMES[state]
        run     = Q[state][RUN]
        service = Q[state][SERVICE]
        replace = Q[state][REPLACE]
        choice  = ACTION_NAMES[best_action(state)]
        print("%-12s %7.1f  %7.1f  %7.1f      %s"
              % (name, run, service, replace, choice))


random.seed(2)        # so the live run tells the same story every time
WEEKS = 400000

print("Learning from %s weeks of driving." % "{:,}".format(WEEKS))
print("Watch the best choice in each condition settle down as the bills add up:")
print()
train(WEEKS)          # prints a policy snapshot every so often as it learns
show_policy()         # the final learned value table

print()
print("Read it top to bottom: run her while young, service her when worn,")
print("and scrap her once she gets shaky -- even though she still drives.")
