"""
Repair or Replace: a tiny policy-learning demo (a bare-bones REINFORCE).

Same delivery van, same weekly choice, same money as repair_or_replace.py:
    RUN      drive the route, earn money, risk a breakdown
    SERVICE  spend a week in the shop, pay 50, the van gets better
    REPLACE  buy a new van, pay 130, start fresh

Q-learning (the other demo) learns a score for every choice and then picks the
best score. This demo never scores a choice. It keeps a PLAYBOOK OF ODDS: in
each condition, a chance of RUN, a chance of SERVICE and a chance of REPLACE.
Then it repeats four steps:

    1. play one quarter (13 weeks), rolling the dice with today's odds
    2. add up the money that came in after each week
    3. turn the dials: a choice becomes likelier when money followed it,
       and less likely when a loss followed it
    4. go back to 1

We do NOT tell the program the breakdown odds. It learns from the bills alone.

Run it with:  python3 repair_or_replace_reinforce.py
"""

import math
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
# van is SHAKY or FAILING: that is what will make REPLACE the better call there.
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
# 2. THE LEARNER (REINFORCE: do more of what paid)
# ---------------------------------------------------------------------------

# How much we value future money compared to money right now (0.9 = patient).
GAMMA = 0.9

# We learn from one stretch of weeks at a time. 13 weeks is one quarter.
WEEKS_PER_RUN = 13

# How hard we turn a dial for each coin of money. Small turns are slow but
# steady. Big turns are quick, but they can lock the playbook onto a wrong
# choice for good (at ten times this size, about one run in twelve never
# recovers).
STEP_SIZE = 0.0003

# Who gets the credit for the money? False: each week is judged only by the
# money that came after it (a choice cannot change the past). True: every week
# of a run is judged by the whole run's money, the first and crudest version
# of the idea. It still finds the right playbook, but needs about ten times as
# many weeks to get there every time.
WHOLE_RUN_CREDIT = False

# As it learns, we print the most likely choice in each condition a few times,
# so the class can watch the playbook settle. This is the pause (seconds)
# between those snapshots. Set to 0 for an instant run.
SNAPSHOT_PAUSE = 0.5

# The dials: for every condition, one number for each choice. A higher dial
# means a likelier choice. Every dial starts at 0, so at first every choice
# is equally likely (one chance in three).
DIALS = [
    [0.0, 0.0, 0.0],   # HEALTHY: RUN, SERVICE, REPLACE
    [0.0, 0.0, 0.0],   # WORN
    [0.0, 0.0, 0.0],   # SHAKY
    [0.0, 0.0, 0.0],   # FAILING
]


def odds(state):
    """
    Turn the three dials of this condition into three chances that add up to 1.
    Equal dials give equal chances, and a higher dial gives a bigger chance.
    (This is called a softmax. Taking the biggest dial away from all three
    first changes no chance, it just keeps the numbers small.)
    """
    biggest = max(DIALS[state])
    weights = []
    for action in [RUN, SERVICE, REPLACE]:
        weights.append(math.exp(DIALS[state][action] - biggest))
    total = weights[0] + weights[1] + weights[2]

    chances = []
    for action in [RUN, SERVICE, REPLACE]:
        chances.append(weights[action] / total)
    return chances


def most_likely(state):
    """Return the choice with the biggest chance in this condition."""
    chances = odds(state)
    best = RUN
    for action in [SERVICE, REPLACE]:
        if chances[action] > chances[best]:
            best = action
    return best


def play_a_run():
    """
    Play one quarter with today's odds, starting from a HEALTHY van.
    Write down every week: the condition, the choice we rolled, the chances
    we rolled it with, and the money we got.
    """
    conditions = []
    choices = []
    chances_used = []
    money = []

    state = HEALTHY
    for week in range(WEEKS_PER_RUN):
        chances = odds(state)
        action = pick(chances)                    # roll the dice with today's odds
        new_state, reward = step(state, action)

        conditions.append(state)
        choices.append(action)
        chances_used.append(chances)
        money.append(reward)

        state = new_state

    return conditions, choices, chances_used, money


def learn_from(conditions, choices, chances_used, money):
    """
    Turn the dials after one quarter: do more of what paid.
    """

    # The money from each week on: that week's money, plus the discounted
    # money of the weeks after it. We add it up backwards, from the last week.
    money_after = [0.0] * WEEKS_PER_RUN
    running_total = 0.0
    for week in range(WEEKS_PER_RUN - 1, -1, -1):
        running_total = money[week] + GAMMA * running_total
        money_after[week] = running_total

    for week in range(WEEKS_PER_RUN):
        state = conditions[week]
        chosen = choices[week]

        credit = money_after[week]
        if WHOLE_RUN_CREDIT:
            credit = money_after[0]

        for action in [RUN, SERVICE, REPLACE]:
            if action == chosen:
                # The choice we made: make it likelier.
                nudge = 1.0 - chances_used[week][action]
            else:
                # The choices we did not make: make them a little less likely.
                nudge = 0.0 - chances_used[week][action]

            # Good money: follow the nudge. A loss: go the other way.
            # The bigger the money, the bigger the turn of the dial.
            DIALS[state][action] = DIALS[state][action] + STEP_SIZE * credit * nudge


def policy_row(label):
    """Print one line: the most likely choice in each condition, and its chance."""
    cells = ""
    for state in [HEALTHY, WORN, SHAKY, FAILING]:
        best = most_likely(state)
        percent = round(100 * odds(state)[best])
        cells = cells + "%-8s%3d%%  " % (ACTION_NAMES[best], percent)
    print("%13s   %s" % (label, cells))


def train(runs):
    """
    Play many quarters, turning the dials after each one.

    Every so often we print the most likely choice in each condition and how
    likely it is, so the class can WATCH the playbook being learned: it starts
    as a shrug (every choice 33%) and settles down to the answer as the bills
    come in.
    """
    snapshots = {10, 50, 200, 1000, 5000, runs}

    # Header + the untrained playbook. Every dial starts at 0, so every choice
    # has the same chance and RUN is simply the first one on the list.
    header = "".join("%-14s" % STATE_NAMES[s]
                     for s in [HEALTHY, WORN, SHAKY, FAILING])
    print("%13s   %s" % ("", header))
    policy_row("start")

    for run in range(1, runs + 1):
        conditions, choices, chances_used, money = play_a_run()
        learn_from(conditions, choices, chances_used, money)

        # Now and then, freeze and show what the playbook would do today.
        if run in snapshots:
            policy_row("{:,} wks".format(run * WEEKS_PER_RUN))
            time.sleep(SNAPSHOT_PAUSE)


# ---------------------------------------------------------------------------
# 3. RUN IT AND SHOW THE RESULT
# ---------------------------------------------------------------------------

def show_policy():
    """Print the learned odds and the most likely choice in each condition."""
    print()
    print("Learned odds (the chance of each choice):")
    print("condition        RUN    SERVICE   REPLACE     most likely")
    for state in [HEALTHY, WORN, SHAKY, FAILING]:
        name    = STATE_NAMES[state]
        chances = odds(state)
        choice  = ACTION_NAMES[most_likely(state)]
        print("%-12s %7.1f%% %7.1f%% %7.1f%%      %s"
              % (name, 100 * chances[RUN], 100 * chances[SERVICE],
                 100 * chances[REPLACE], choice))


random.seed(2)        # so the live run tells the same story every time
QUARTERS = 30000

print("Learning from %s quarters of driving (%s weeks)."
      % ("{:,}".format(QUARTERS), "{:,}".format(QUARTERS * WEEKS_PER_RUN)))
print("Watch the odds settle down as the bills add up:")
print()
train(QUARTERS)       # prints a playbook snapshot every so often as it learns
show_policy()         # the final learned odds

print()
print("Read it top to bottom: run her while young, service her when worn,")
print("and scrap her once she gets shaky, even though she still drives.")
