# Suguru Genetic Algorithm Solver

This repository contains a Python implementation of a Genetic Algorithm to solve the Suguru puzzle. The Suguru puzzle is a logic-based number placement game that involves filling a grid with numbers according to specific rules.

## Suguru Puzzle Rules
1. The grid is divided into regions, each containing a specific number of cells.
2. Each region must be filled with numbers from 1 to the number of cells in that region, without repeating any number within the region.
3. Adjacent cells (horizontally and vertically) must not contain the same number.
4. The puzzle is solved when all cells are filled according to these rules.
5. The puzzle can have multiple solutions, but the goal is to find at least one valid solution.

## Features
Automatic generation of Suguru puzzles with varying difficulty levels.
- Implementation of a Genetic Algorithm to solve Suguru puzzles.
- Support for different grid sizes and region configurations.
- Visualization of the puzzle and the solution process.
- Extensive documentation and examples to help users understand the code and how to use it.

## Installation
To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage
To use the Suguru solver, you can run the main script:

```bash
python main_backtracking.py
```
You can also run the Genetic Algorithm solver:

```bash
python main_ga.py
```

## Solution
The solution is implemented using a Genetic Algorithm that evolves a population of candidate solutions over generations. The algorithm includes:
- **Initialization**: Randomly generate an initial population of candidate solutions.
- **Selection**: Select the best candidates based on fitness, which is determined by how well they satisfy the Suguru rules.
- **Crossover**: Combine pairs of candidates to create new candidates.
- **Mutation**: Introduce random changes to candidates to maintain genetic diversity.
- **Termination**: The algorithm runs until a solution is found or a maximum number of generations is reached.
