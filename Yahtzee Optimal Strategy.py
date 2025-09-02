"""
Single-turn Yahtzee optimizer:
- Computes the optimal reroll policy for ONE turn (up to two rerolls),
  maximizing the final category score for that turn.
- Not a full-game strategy (does not track used categories/bonuses).
"""

#import libraries
import random
import itertools
from collections import Counter
from functools import lru_cache

#function list(itertools.product([True, False], repeat=5)) gives every combination of a 5 item list consisting of True and False items
KEEP_MASKS = list(itertools.product([True, False], repeat=5))


#automated best case category based on scores (no need for True/False validation based on input)
def score_roll(dice):
    # returns the best score based on current dice state
    counts = Counter(dice)
    values = list(counts.values())
    scores = [(sum(dice), 'Chance')]  # Chance

    # 3 and 4 of a Kind
    if max(values) >= 3:
        scores.append((sum(dice), '3 of a Kind'))
    if max(values) >= 4:
        scores.append((sum(dice), '4 of a Kind'))

    # Full House
    if sorted(values) == [2, 3]:
        scores.append((25, 'Full House'))
    # if any subsets from the list is equal to no-duplicates dice state, then append score,category to list

    # Small and Large Straights
    unique = set(dice)
    if any(s.issubset(unique) for s in [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]):
        scores.append((30, 'Small Straight'))
    if any(s.issubset(unique) for s in [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]):
        scores.append((40, 'Large Straight'))

    # Yahtzee
    if max(values) == 5:
        scores.append((50, 'Yahtzee'))

    return max(scores)

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

def get_sample_count(mask):
    return 6 ** mask.count(False)

#reduces MDP time by 10x, prevents redundant V() calls
@lru_cache(maxsize=None)
#recursive function: recursive chain ends up at re-roll = 0 and calculates the ev, creating a tree pathway for every possible combination
def V(dice, rolls_left):
    dice = tuple(sorted(dice))
    category_choice = score_roll(dice)

    if rolls_left == 0:
        score,category_choice = score_roll(dice)
        return score, None,category_choice  # no rerolls left

    best_ev = float ('-inf')
    best_mask = None

    # Try all 32 reroll patterns
    for mask in KEEP_MASKS:

        #Count how many dice we plan to reroll
        reroll_count = mask.count(False)

        #Generating every possible combination of rerolled dice (6^k, where k = reroll_count)
        possible_outcomes = itertools.product(range(1, 7), repeat=reroll_count)
        total_ev = 0

        #The amount of outcomes
        total_outcomes = 6 ** reroll_count

        #Build a full 5-dice hand combining the kept dice and the new rerolled values
        for reroll in possible_outcomes:
            new_dice = []
            i = 0

            #Reconstruct full hand with kept and rerolled values
            #zip(a,b) pairs elements from 2 lists/tuples position by position
            #Loop through each keep value in mask and dice value
            for keep, val in zip(mask, dice):
                if keep:
                    new_dice.append(val) # Keep original die
                else:
                    new_dice.append(reroll[i]) # Use rerolled value
                    i += 1

            #Sort dice so that the @lru_cache can use previous results and speed up when dealing with multiple runs
            new_dice = tuple(sorted(new_dice))
            #Recursively compute expected value from this new state
            ev, _, _ = V(new_dice, rolls_left - 1)
            total_ev += ev

        avg_ev = total_ev / total_outcomes

        if avg_ev > best_ev:
            best_ev = avg_ev
            best_mask = mask

    return best_ev,best_mask,category_choice

def average_turn_ev():
    total = 0.0
    for s in itertools.product(range(1, 7), repeat=5):
        ev, _, _ = V(tuple(sorted(s)), 2)
        total += ev
    return total / 7776

if __name__ == '__main__':
    avg = average_turn_ev()
    print(f"Average turn EV with optimal rerolling: {avg:.2f}")
