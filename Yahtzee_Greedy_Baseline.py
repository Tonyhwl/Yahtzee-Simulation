import random

# Score the final hand (same as your version but I’ll leave it)
def score_hand(dice):
    counts = [dice.count(i) for i in range(1, 7)]
    scores = []

    # upper section
    for i in range(1, 7):
        scores.append(i * counts[i-1])

    if max(counts) >= 3:  # three of a kind
        scores.append(sum(dice))
    if max(counts) >= 4:  # four of a kind
        scores.append(sum(dice))
    if sorted(counts)[-2:] == [2, 3]:  # full house
        scores.append(25)
    if any(all(x in dice for x in seq) for seq in ([1,2,3,4],[2,3,4,5],[3,4,5,6])):
        scores.append(30)  # small straight
    if set(dice) in (set([1,2,3,4,5]), set([2,3,4,5,6])):
        scores.append(40)  # large straight
    if max(counts) == 5:  # yahtzee
        scores.append(50)

    scores.append(sum(dice))  # chance
    return max(scores)


def greedy_keep(dice):
    # start from face 1 so we never compare against None
    best_num = 1
    best_count = dice.count(1)

    for num in range(2, 7):
        count = dice.count(num)
        # tie-break: prefer the higher face
        if count > best_count or (count == best_count and num > best_num):
            best_num = num
            best_count = count

    # keep all dice equal to best_num
    keep = []
    for d in dice:
        if d == best_num:
            keep.append(d)
    return keep


def simulate_one_round():
    # roll 5 dice
    dice = [random.randint(1, 6) for _ in range(5)]

    # you get 2 re-rolls
    for _ in range(2):
        keep = greedy_keep(dice)
        reroll = 5 - len(keep)
        new_dice = [random.randint(1, 6) for _ in range(reroll)]
        dice = keep + new_dice

    # return score at the end
    return score_hand(dice)


# Run 1000 games to test
scores = []
for _ in range(1000000):
    scores.append(simulate_one_round())

print("Average score:", sum(scores)/len(scores))

