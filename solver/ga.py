import random
import copy
import matplotlib.pyplot as plt
from typing import List
from suguru.board import Suguru


class SuguruGa:
    def __init__(self, suguru: Suguru, population_size=100, generations=500, mutation_rate=0.1):
        self.original = suguru
        self.rows = suguru.rows
        self.cols = suguru.cols
        self.groups = suguru.groups
        self.fixed = suguru.fixed
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.elitism_rate = max(1, population_size // 10)
        self.selection_rate = 5

    def initialize_population(self) -> List[List[List[int]]]:
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
                                violations += 1

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

            violations += 10 * len(missing_values)  # penalty per missing expected value
            violations += 5 * len(extra_values)  # penalty per out-of-range value

        return violations

    # TODO: implement a different mutation strategy that fix wrong values in a region
    def mutate(self, grid: List[List[int]]):
        for group in self.groups:
            if random.random() < self.mutation_rate:
                if self.fixed:
                    non_fixed = [(r, c) for (r, c) in group if not self.fixed[r][c]]
                else:
                    non_fixed = [(r, c) for (r, c) in group]
                if len(non_fixed) >= 2:
                    (r1, c1), (r2, c2) = random.sample(non_fixed, 2)
                    grid[r1][c1], grid[r2][c2] = grid[r2][c2], grid[r1][c1]

    def crossover(self, parent1, parent2):
        # Row-wise crossover
        child = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        for r in range(self.rows):
            source = parent1 if random.random() < 0.5 else parent2
            child[r] = source[r][:]
        return child

    def solve(self):
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

            print(f"Generation {gen:3} | Best: {best_score:3} | Avg: {avg_score:.2f}")

            if best_score == 0:
                candidate = self.set_solution(best_grid)
                if candidate.validate():  # ✅ Ensure full puzzle validity
                    print(f"✅ Valid solution found in generation {gen}")
                    self.plot_fitness(best_fitness_over_time, avg_fitness_over_time)
                    return candidate
                else:
                    print(f"⚠️ Fitness is 0 but solution is invalid. Continuing...")

            # Elitism
            elites = [ind for (_, ind) in scored[:elite_count]]

            # Selection pool (top 20%)
            selection_pool = [ind for (_, ind) in scored[:self.population_size // self.selection_rate]]

            # Generate offspring
            new_population = elites[:]
            while len(new_population) < self.population_size:
                parent1, parent2 = random.sample(selection_pool, 2)
                child = self.crossover(parent1, parent2)
                self.mutate(child)
                new_population.append(child)

            population = new_population

        print("⚠️ No perfect solution found")
        self.plot_fitness(best_fitness_over_time, avg_fitness_over_time)
        return self.set_solution(best_grid)

    def set_solution(self, grid: List[List[int]]) -> Suguru:
        solved = copy.deepcopy(self.original)
        for r in range(self.rows):
            for c in range(self.cols):
                if self.fixed and not self.fixed[r][c]:
                    solved.grid[r][c] = grid[r][c]
        return solved

    @staticmethod
    def plot_fitness(best_fitness, avg_fitness):
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
