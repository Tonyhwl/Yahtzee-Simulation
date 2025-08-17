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

## Timeline
26/07/25 Created Yahtzee Simulation
#Added re-rolling, score categories
29/07/2025
Added category verification
30/07/2025 - 5/08/2025
Implemented Markov Decision Processes and Dynamic Programming to efficiently automate an optimal re-roll
Finished 1-round game of Yahtzee (Automated and Manual)
5/08/2025-7/08/2025
Finished adding heatmap visualisation for EV while keeping dice 1,2,5 fixed.
8/08/2025 - 14/08/2025
Imported multiprocessing for faster run time
Implemented proper bellman backup for full dynamic programming instead of Monte Carlo approximation
15/08/2025
Implemented a random baseline strategy for benchmarking


