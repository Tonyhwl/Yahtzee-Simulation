# Yahtzee Optimal Strategy Simulator

This project models the game of Yahtzee as a Markov Decision Process (MDP) to compute the optimal reroll strategy that maximizes expected score. The implementation uses dynamic programming with memoization to efficiently evaluate all decision paths, and supports large-scale simulation through parallel processing.

## Features

- Full MDP implementation with Bellman backups
- Optimal reroll logic based on expected value
- Manual and automated simulation modes
- Efficient performance via `@lru_cache` and `multiprocessing`

## Technologies

- Python 3.13
- Standard libraries: `itertools`, `collections`, `functools`, `multiprocessing`

## Purpose

Developed as a demonstration of applied probability, optimisation, and algorithmic decision-making, relevant to strategy modeling.

## Sample Output
Average game EV due to optimal re-rolling: 28.5
Average game EV due to random re-rolling: 20.1
Overall increase: +42%


