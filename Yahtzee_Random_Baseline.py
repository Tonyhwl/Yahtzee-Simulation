import random
from collections import Counter

mean_average_ev = []
def roll_dice():
    return [random.randint(1, 6) for _ in range(5)]

def score_roll(dice):
    counts = Counter(dice)
    values = list(counts.values())
    score = sum(dice)  # Chance is always available

    if max(values) >= 3:
        score = max(score, sum(dice))
    if max(values) >= 4:
        score = max(score, sum(dice))
    if sorted(values) == [2, 3]:
        score = max(score, 25)
    unique = set(dice)
    if any(s.issubset(unique) for s in [{1,2,3,4},{2,3,4,5},{3,4,5,6}]):
        score = max(score, 30)
    if any(s.issubset(unique) for s in [{1,2,3,4,5},{2,3,4,5,6}]):
        score = max(score, 40)
    if max(values) == 5:
        score = max(score, 50)

    return score

def play_one_round_random():
    dice = roll_dice()
    # 2 re-rolls with random keep decisions
    for _ in range(2):
        new_dice = []
        for d in dice:
            if random.choice([True, False]):  # randomly keep or reroll
                new_dice.append(d)
            else:
                new_dice.append(random.randint(1, 6))
        dice = new_dice
    return score_roll(dice)

for i in range(20):
    simulation_score = []
    for j in range(10000):
        simulation_score.append(play_one_round_random())
        average_ev = (sum(simulation_score) / len(simulation_score))
    print(f'Average game EV due to random_rerolling: {round(average_ev, 2)}')
    mean_average_ev.append(average_ev)
print(sum(mean_average_ev) / len(mean_average_ev))
