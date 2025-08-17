#import libraries
import random
import itertools
from collections import Counter
from functools import lru_cache

dice_state = []
position_list = []
game_scores = []

#setting up dictionary and values for lower score categories and checking
lower_score_card = {
    'Aces' : 1,
    'Twos' : 2,
    'Threes' : 3,
    'Fours' : 4,
    'Fives' : 5,
    'Sixes' : 6,
}

#setting up dictionary for checking upper score categories
upper_score_card = {
    '3 of a Kind' : 0,
    '4 of a Kind' : 0,
    'Full House' : 0,
    'Small Straight' : 0,
    'Large Straight' : 0,
    'Yahtzee' : 0,
    'Chance' : 0
}

#initial roll of dice as round 1
def roll_dice():
    dice_state.clear()
    for i in range(5):
        dice_number = 0
        dice_number= random.randint(1,6)
        dice_state.append(dice_number )
    print('You rolled: ', dice_state)

#user re-rolling for a new combination
def change_state():
    dice_number = 0
    position =  input('Which position would you like to change?')
    if position == 'none' or position == 'None':
        print('You rolled: ', dice_state)
    else:
        position_list = list(map(int, position.split(',')))
        for n in range(1,6):
            if n in position_list:
                dice_number = random.randint(1, 6)
                print(dice_number)
                dice_state[n - 1] = dice_number
        print('You rolled: ', dice_state)

#checking for 3 of a Kind
def is_3_of_a_Kind():
    # 'Counter' creates a frequency dictionary of how many times a number appears
    # '.values()' returns the counts [1,1,3]
    #'for' statement checks if every item in the list is greater than or equal to 3
    for count in Counter(dice_state).values():
        if count >= 3:
            return True
    return False

#checking for 4 of a Kind
def is_4_of_a_Kind():
    for count in Counter(dice_state).values():
        if count >= 4:
            return True
    return False

#checking for Full House
def is_Full_House():
    counts = Counter(dice_state).values()
    return sorted(counts) == [2,3]

#checking for Small Straight
def is_Small_Straight():
    #removes any duplicates in the 5 dices
    unique = set(dice_state)
    #setting up the list of possible small straights
    small_straights = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
    #checks if the unique dice state matches with any of the straights (if it does, returns True)
    for small_straight in small_straights:
        if small_straight.issubset(unique):
            return True
    return False

#checking for Large Straight
def is_Large_Straight():
    unique = set(dice_state)
    large_straights = [{1,2,3,4,5},{2,3,4,5,6}]
    for large_straight in large_straights:
        if large_straight.issubset(unique):
            return True
    return False

#checking for 5 of a Kind or Yahtzee
def is_Yahtzee():
    counts = Counter(dice_state).values()
    return counts == [5]

#user selects a category based on their final combination of dice
def category_selection():
    valid_category = False
    scores = []
    category_choice = input('What category would you like to put your final roll in?')
    while not valid_category:
        if category_choice in upper_score_card:
            if category_choice == '3 of a Kind' and is_3_of_a_Kind() == True:
                scores.append(sum(dice_state))
                valid_category = True
            elif category_choice == '4 of a Kind' and is_4_of_a_Kind() == True:
                scores.append(sum(dice_state))
                valid_category = True
            elif category_choice == 'Chance':
                scores.append(sum(dice_state))
                valid_category = True
            elif category_choice == 'Full House' and is_Full_House() == True:
                scores.append(25)
            elif category_choice == 'Small Straight' and is_Small_Straight() == True:
                scores.append(30)
            elif category_choice == 'Large Straight' and is_Large_Straight() == True:
                scores.append(40)
            elif category_choice == 'Yahtzee' and is_Yahtzee() == True:
                scores.append(50)
            else:
                print('Invalid category')
                valid_category = False
                category_choice = input('What category would you like to put your final roll in?')


        elif category_choice in lower_score_card:
            for j in range (0,5):
                if lower_score_card[category_choice] == dice_state[j]:
                    scores.append(lower_score_card[category_choice])
            valid_category = True

        else:
            print('Invalid category')
            valid_category = False
            category_choice = input('What category would you like to put your final roll in?')

    return scores

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

def get_sample_count(mask):
    reroll_count = mask.count(False)
    if reroll_count <= 2:
        return 6 ** reroll_count  # Enumerate exactly
    elif reroll_count == 3:
        return 216  # or 500 for better smoothing
    elif reroll_count == 4:
        return 1000
    else:
        return 3000  # rerolling all 5 dice

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

def reroll_dice(start,best_mask):
    temp_list = list(start)
    dice_position_reroll = []
    for i in range(0,5):
        if not best_mask[i]:
            dice_position_reroll.append(i+1)
            temp_list[i] = random.randint(1,6)
        #else:
            #print('Keep positions: ', i+1)
    #print('Positions to re-roll:', dice_position_reroll)
    start = tuple(temp_list)
    return start

#new simulation run w/o printing
def simulation(_):
    start = tuple(random.randint(1, 6) for _ in range(5))
    best_ev, _, _ = V(start, 2)
    return best_ev

#main run - user input run
def user_main():
    roll_dice()
    for i in range (2):
        change_state()
    scores = category_selection()
    print('Your score is: ', scores)

#choice = input('Would you like an automated run or manual? (a/m)')
#if choice == 'a':
    #simulation()
#elif choice == 'm':
    #user_main()

import multiprocessing as mp

if __name__ == '__main__':
    num_games = 1000000

    with mp.Pool() as pool:
        game_scores = pool.map(simulation, range(num_games))

    # score for score unpacks each tuple so score is the float EV and _ discards category
    average_ev = sum(game_scores) / len(game_scores)
    print(f'Average game EV due to optimal re-rolling: {round(average_ev, 2)}')





