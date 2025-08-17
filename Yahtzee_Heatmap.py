import random
import itertools
from collections import Counter
from functools import lru_cache
import matplotlib.pyplot as plt
import numpy as np

#automated best case category based on scores (no need for True/False validation based on input)
def score_roll(dice):
    score = 0
#returns the best score based on current dice state
    counts = Counter(dice)
    values = counts.values()
    scores = [sum(dice)]  # start with Chance
    category_choice = 'Chance'

#form a list of valid scores
    if max(values) >= 3:
        scores.append(sum(dice))  # 3 of a kind
        category_choice = '3 of a Kind'
    if max(values) >= 4:
        scores.append(sum(dice))  # 4 of a kind
        category_choice = '4 of a Kind'
    if sorted(values) == [2, 3]:
        scores.append(25)  # Full House
        category_choice = 'Full House'

    unique = set(dice)
# if any subsets from the list is equal to no-duplicates dice state, then append score to list
    if any(s.issubset(unique) for s in [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]):
        scores.append(30)  # Small straight
        category_choice = 'Small straight'
    if any(s.issubset(unique) for s in [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]):
        scores.append(40)  # Large straight
        category_choice = 'Large straight'
    if max(values) == 5:
        scores.append(50)  # Yahtzee
        category_choice = 'Yahtzee'
    score = max(scores)
#to avoid score overlap/maximise score, we return the maximum value of the list of scores and choice of category for later
    return score,category_choice

def generate_all_keep_masks():
    #function list(itertools.product([True, False], repeat=5)) gives every combination of a 5 item list consisting of True and False items
    return list(itertools.product([True, False], repeat=5))

def apply_keep_mask(dice, mask):
    new_dice = []

    for i in range(5):
        dice_value = dice[i]  # current die value
        keep = mask[i]  # whether to keep it or not

        if keep:
            # if dice is kept, add to new list
            new_dice.append(dice_value)
        else:
            # if dice is re-rolled, generate a new dice
            new_value = random.randint(1, 6)
            new_dice.append(new_value)

    # Return the final result
    return tuple(new_dice)

#reduces MDP time by 10x, prevents redundant V() calls
@lru_cache(maxsize=None)
#recursive function: recursive chain ends up at re-roll = 0 and calculates the ev, creating a tree pathway for every possible combination
def V(dice, rolls_left):
    category_choice = score_roll(dice)
    dice = tuple(sorted(dice))

    if rolls_left == 0:
        score,category_choice = score_roll(dice)
        return score, None,category_choice  # no rerolls left

    best_ev = float ('-inf')
    best_mask = None

    # Try all 32 reroll patterns
    for mask in generate_all_keep_masks():
        # Count how many dice we plan to reroll
        reroll_count = mask.count(False)

        # Generating every possible combination of rerolled dice (6^k, where k = reroll_count)
        possible_outcomes = itertools.product(range(1, 7), repeat=reroll_count)
        total_ev = 0

        # The amount of outcomes
        total_outcomes = 6 ** reroll_count

        # Build a full 5-dice hand combining the kept dice and the new rerolled values
        for reroll in possible_outcomes:
            new_dice = []
            i = 0

            # Reconstruct full hand with kept and rerolled values
            # zip(a,b) pairs elements from 2 lists/tuples position by position
            # Loop through each keep value in mask and dice value
            for keep, val in zip(mask, dice):
                if keep:
                    new_dice.append(val)  # Keep original die
                else:
                    new_dice.append(reroll[i])  # Use rerolled value
                    i += 1

            # Sort dice so that the @lru_cache can use previous results and speed up when dealing with multiple runs
            new_dice = tuple(sorted(new_dice))
            # Recursively compute expected value from this new state
            ev, _, _ = V(new_dice, rolls_left - 1)
            total_ev += ev

        avg_ev = total_ev / total_outcomes
        #if the new expected value is better, set it equal to the best and note down the mask combination of the list
        if avg_ev > best_ev:
            best_ev = avg_ev
            best_mask = mask

    return best_ev,best_mask,category_choice

# Vary Dice 4 and Dice 5 over all combinations (1 to 6)

# 6 x 6 grid (36 combinations of Dice 4 and Dice 5)
die_values = range(1, 7)
X, Y = np.meshgrid(die_values, die_values)

ev_list = []


dice_number = input('Which dice would you like to view as an EV heatmap? (separate by space)')
number_map = list(map(int, dice_number.split()))

# Loop through all combinations of Dice 4 and Dice 5 (1 to 6)
for d4 in range(1, 7):
    for d5 in range(1, 7):
        dice = (number_map[0], number_map[1], number_map[2], d4, d5)
        dice = tuple(sorted(dice))
        ev, *_ = V(dice, 2)  # Call MDP function with 2 rolls left
        ev_list.append(ev)
# Convert to 6x6 matrix
Z = np.array(ev_list).reshape(6, 6)

# 3D Plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Surface plot
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k', linewidth=0.3, antialiased=True)

# Labels and title
ax.set_title(f"EV Surface with Dice {', '.join(map(str, number_map))} Fixed at 1, 2, 3 respectively", fontsize=14)
ax.set_xlabel("Die 4 Value")
ax.set_ylabel("Die 5 Value")
ax.set_zlabel("Expected Value")

# Optional: add color bar
fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)

plt.tight_layout()
plt.show()