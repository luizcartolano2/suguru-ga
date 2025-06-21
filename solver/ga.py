""" Suguru Genetic Algorithm Solver.

"""
import random
import copy
import matplotlib.pyplot as plt
from typing import List
from suguru.board import Board


class SuguruGa:
    """
    Suguru Genetic Algorithm Solver.
    This class implements a genetic algorithm to solve Suguru puzzles.
    It initializes a population of candidate solutions, evaluates their fitness,
    applies selection, crossover, and mutation to evolve the population over
    a number of generations, and returns a valid solution if found.

    Attributes:
        suguru (Board): The Suguru puzzle to solve, represented as a Board object.
        population_size (int): The number of candidate solutions in the population.
        generations (int): The number of generations to evolve the population.
        mutation_rate (float): The probability of mutating an individual.
        mutation_type (str): The type of mutation to apply ('swap', 'smart').
        crossover_type (str): The type of crossover to apply ('random', 'row', 'group', 'repair').
    """
    def __init__(self, suguru: Board, population_size=100, generations=500, mutation_rate=0.1, mutation_type="swap", crossover_type="random"):
        self.original = suguru
        self.rows = suguru.rows
        self.cols = suguru.cols
        self.groups = suguru.groups
        self.fixed = suguru.fixed
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.mutation_type = mutation_type
        self.crossover_type = crossover_type
        self.elitism_rate = max(1, population_size // 10)
        self.selection_rate = 5

    def initialize_population(self) -> List[List[List[int]]]:
        """
        Initializes the population with random individuals based on the Suguru groups.
        :return: a list of individuals, where each individual is a grid representing a candidate solution.
        """
        population = []

        for _ in range(self.population_size):
            individual = [[None for _ in range(self.cols)] for _ in range(self.rows)]
            for group in self.groups:
                group_values = list(range(1, len(group) + 1))
                random.shuffle(group_values)
                for (r, c), val in zip(group, group_values):
                    if self.fixed and self.fixed[r][c]:
                        individual[r][c] = self.original.grid[r][c]
                    else:
                        individual[r][c] = val
            population.append(individual)
        return population

    def fitness(self, grid: List[List[int]]) -> int:
        """
        Calculates the fitness of a given grid.
        :param grid: a 2D list representing the Suguru grid.
        :return: an integer representing the number of violations in the grid.
        """
        violations = 0

        # Check adjacent cells for duplicate values
        for r in range(self.rows):
            for c in range(self.cols):
                val = grid[r][c]
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if grid[nr][nc] == val:
                                violations += 10

        # Check groups for uniqueness and correct value range
        for group in self.groups:
            seen = set()
            expected_values = set(range(1, len(group) + 1))
            group_values = []

            for r, c in group:
                val = grid[r][c]
                group_values.append(val)

                # Penalize if value already seen in this group (duplicates)
                if val in seen:
                    violations += 10  # heavy penalty for duplicate in group
                else:
                    seen.add(val)

            # Penalize missing or out-of-range values
            group_value_set = set(group_values)
            missing_values = expected_values - group_value_set
            extra_values = group_value_set - expected_values

            violations += 5 * len(missing_values)  # penalty per missing expected value
            violations += 5 * len(extra_values)  # penalty per out-of-range value

        return violations

    def smart_mutate(self, grid: List[List[int]]):
        """
        Applies a smart mutation to the grid. A random group is selected, and if there are duplicates,
        it replaces one of the duplicates with a missing value from the group.
        :param grid: a 2D list representing the Suguru grid.
        :return: a mutated grid.
        """
        for group in self.groups:
            if random.random() < self.mutation_rate:
                # Extract values from the group
                cells = [(r, c) for (r, c) in group if not self.fixed[r][c]]
                values = [grid[r][c] for (r, c) in cells if grid[r][c] is not None]

                # Determine missing and duplicate values
                n = len(group)
                expected = set(range(1, n + 1))
                present = set(values)
                duplicates = [v for v in values if values.count(v) > 1]
                missing = list(expected - present)

                if duplicates and missing:
                    for (r, c) in cells:
                        if grid[r][c] in duplicates:
                            new_value = random.choice(missing)
                            grid[r][c] = new_value
                            break

    def swap_mutate(self, grid: List[List[int]]):
        """
        Applies a swap mutation to the grid. A random pair of non-fixed cells in each group is swapped.
        :param grid: a 2D list representing the Suguru grid.
        :return: a mutated grid.
        """
        for group in self.groups:
            if random.random() < self.mutation_rate:
                if self.fixed:
                    non_fixed = [(r, c) for (r, c) in group if not self.fixed[r][c]]
                else:
                    non_fixed = [(r, c) for (r, c) in group]
                if len(non_fixed) >= 2:
                    (r1, c1), (r2, c2) = random.sample(non_fixed, 2)
                    grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]

    def mutate(self, grid: List[List[int]], mutation_type: str = "swap"):
        """
        Applies mutation to the grid based on the specified mutation type.
        :param grid: a 2D list representing the Suguru grid.
        :param mutation_type: a string indicating the type of mutation to apply ('swap', 'smart', or 'both').
        :return: a mutated grid.
        """
        if mutation_type == "swap":
            self.swap_mutate(grid)
        elif mutation_type == "smart":
            self.smart_mutate(grid)
        else:
            self.swap_mutate(grid)
            self.smart_mutate(grid)

    def crossover(self, parent1, parent2, crossover_type='random'):
        """
        Applies crossover between two parent grids to create a child grid.
        :param parent1: a 2D list representing the first parent grid.
        :param parent2: a 2D list representing the second parent grid.
        :param crossover_type: a string indicating the type of crossover to apply ('row', 'group', 'repair', or 'random').
        :return: a 2D list representing the child grid created from the parents.
        """
        if crossover_type == 'row':
            return self.crossover_by_row(parent1, parent2)
        elif crossover_type == 'group':
            return self.crossover_by_group(parent1, parent2)
        elif crossover_type == 'repair':
            return self.crossover_with_repair(parent1, parent2)
        else:
            p = random.random()
            if p < 0.5:
                return self.crossover_by_row(parent1, parent2)
            else:
                return self.crossover_by_group(parent1, parent2)

    def crossover_by_row(self, parent1, parent2):
        """
        Applies row-wise crossover between two parent grids to create a child grid. At each row, it randomly selects
        one of the parents to copy the row from.
        :param parent1: a 2D list representing the first parent grid.
        :param parent2: a 2D list representing the second parent grid.
        :return: a 2D list representing the child grid created from the parents.
        """
        # Row-wise crossover
        child = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            source = parent1 if random.random() < 0.5 else parent2
            child[r] = source[r][:]
        return child

    def crossover_by_group(self, parent1, parent2):
        """
        Applies group-wise crossover between two parent grids to create a child grid. For each group, it randomly selects
        one of the parents to copy the values from.
        :param parent1: a 2D list representing the first parent grid.
        :param parent2: a 2D list representing the second parent grid.
        :return: a 2D list representing the child grid created from the parents.
        """
        child = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for group in self.groups:
            source = parent1 if random.random() < 0.5 else parent2
            for r, c in group:
                child[r][c] = source[r][c]
        return child

    def crossover_with_repair(self, parent1, parent2):
        """
        Applies crossover between two parent grids and repairs the child grid to ensure all values are valid.
        :param parent1: a 2D list representing the first parent grid.
        :param parent2: a 2D list representing the second parent grid.
        :return: a 2D list representing the child grid created from the parents, with repairs applied.
        """
        child = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            source = parent1 if random.random() < 0.5 else parent2
            child[r] = source[r][:]

        # Repair the child grid to ensure all values are valid
        for group in self.groups:
            values = [child[r][c] for r, c in group]
            n = len(group)
            used = set()
            duplicates = []
            for i, v in enumerate(values):
                if v in used or not (1 <= v <= n):
                    duplicates.append(i)
                else:
                    used.add(v)

            missing = list(set(range(1, n + 1)) - used)
            random.shuffle(missing)

            for idx, i in enumerate(duplicates):
                r, c = group[i]
                child[r][c] = missing[idx]

        return child

    def solve(self):
        """
        Solves the Suguru puzzle using a genetic algorithm. A population of candidate solutions is initialized,
        and the algorithm iteratively evaluates their fitness, applies selection, crossover, and mutation
        to evolve the population over a number of generations. If a valid solution is found, it is returned.
        :return: a Board object representing the solved Suguru puzzle, or the best candidate solution if no perfect solution is found.
        """
        population = self.initialize_population()
        elite_count = self.elitism_rate

        # Fitness tracking
        best_fitness_over_time = []
        avg_fitness_over_time = []

        for gen in range(self.generations):
            scored = [(self.fitness(ind), ind) for ind in population]
            scored.sort(key=lambda x: x[0])
            fitness_scores = [score for score, _ in scored]

            best_score = fitness_scores[0]
            avg_score = sum(fitness_scores) / len(fitness_scores)
            best_grid = scored[0][1]

            best_fitness_over_time.append(best_score)
            avg_fitness_over_time.append(avg_score)

            print(f"Generation {gen:3} | Best Score: {best_score:3} | Avg Score: {avg_score:.2f}")

            if best_score == 0:
                candidate = self.set_solution(best_grid)
                if candidate.validate():
                    print(f"Valid solution found in generation {gen}")
                    self.plot_fitness(best_fitness_over_time, avg_fitness_over_time)
                    return candidate
                else:
                    print(f"Fitness is 0 but solution is invalid. Restarting population...")
                    self.initialize_population()
                    best_fitness_over_time.clear()
                    avg_fitness_over_time.clear()
                    continue

            # Elitism
            elites = [ind for (_, ind) in scored[:elite_count]]

            # Selection pool (top 20%)
            selection_pool = [ind for (_, ind) in scored[:self.population_size // self.selection_rate]]

            # Generate offspring
            new_population = elites[:]
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(selection_pool, 2)
                child = self.crossover(parent1, parent2, self.crossover_type)
                self.mutate(child, self.mutation_type)
                new_population.append(child)

            population = new_population

        print("No perfect solution found")
        self.plot_fitness(best_fitness_over_time, avg_fitness_over_time)
        return self.set_solution(best_grid)

    def set_solution(self, grid: List[List[int]]) -> Board:
        """
        Sets the solution grid into a Board object, preserving fixed cells.
        :param grid: a 2D list representing the Suguru grid.
        :return: a Board object representing the solved Suguru puzzle.
        """
        solved = copy.deepcopy(self.original)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.fixed and not self.fixed[r][c]:
                    solved.grid[r][c] = grid[r][c]
        return solved

    @staticmethod
    def plot_fitness(best_fitness, avg_fitness):
        """
        Plots the best and average fitness over generations.
        :param best_fitness: a list of the best fitness scores over generations.
        :param avg_fitness: a list of average fitness scores over generations.
        :return: a plot showing the fitness evolution.
        """
        plt.figure(figsize=(10, 5))
        plt.plot(best_fitness, label="Best fitness")
        plt.plot(avg_fitness, label="Average fitness", linestyle="--")
        plt.xlabel("Generation")
        plt.ylabel("Fitness (violations)")
        plt.title("Fitness over Generations")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
