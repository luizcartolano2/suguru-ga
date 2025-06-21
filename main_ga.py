""" This script solves Suguru puzzles using a Genetic Algorithm (GA) with multiple configurations.

"""
import json
import time

from suguru.parser import Parser
from solver.ga import SuguruGa
from suguru.stats import Stats


def solve_with_multiple_configs(puzzle, puzzle_idx):
    """
    Tries to solve a Suguru puzzle using various configurations of the Genetic Algorithm.
    :param puzzle: a Suguru puzzle instance to solve.
    :param puzzle_idx: an index of the puzzle for logging purposes.
    :return: a tuple containing the time taken to solve, the best configuration used, and a boolean indicating if the puzzle was solved.
    """
    mutation_rates = [0.1, 0.2, 0.3]
    populations = [200, 500, 1000]
    generations_list = [300, 600, 1000]
    mutation_types = ['swap', 'smart', 'both']
    crossover_types = ['row', 'group', 'random']

    best_attempt = None
    best_time = float('inf')
    best_config = None

    for pop in populations:
        for gens in generations_list:
            for mut_rate in mutation_rates:
                for mut_type in mutation_types:
                    for cross_type in crossover_types:
                        solver = SuguruGa(
                            puzzle,
                            population_size=pop,
                            generations=gens,
                            mutation_rate=mut_rate,
                            mutation_type=mut_type,
                            crossover_type=cross_type
                        )
                        start_time = time.time()
                        solved_puzzle = solver.solve()
                        elapsed = time.time() - start_time

                        if solved_puzzle.validate():
                            solved_puzzle.display(f"outputs/ga/solved_{puzzle_idx + 1}.png")
                            return_config = {
                                "population": pop,
                                "generations": gens,
                                "mutation_rate": mut_rate,
                                "mutation_type": mut_type,
                                "crossover_type": cross_type
                            }
                            return elapsed, return_config, True

                        if elapsed < best_time:
                            best_attempt = solved_puzzle
                            best_time = elapsed
                            best_config = {
                                "population": pop,
                                "generations": gens,
                                "mutation_rate": mut_rate,
                                "mutation_type": mut_type,
                                "crossover_type": cross_type
                            }

    if best_attempt:
        best_attempt.display(f"outputs/ga/unsolved_{puzzle_idx + 1}.png")

    return best_time, best_config, False


if __name__ == "__main__":
    puzzles = Parser.load_puzzles("instances/easy.json")
    cells_to_fill_list = [sum(row.count(False) for row in puzzle.fixed) for puzzle in puzzles]

    config_log = []
    list_of_times = []
    solved_puzzles = 0
    non_solved_puzzles = 0

    for idx, puzzle in enumerate(puzzles):
        duration, config, solved = solve_with_multiple_configs(puzzle, idx)
        list_of_times.append(duration)
        config_log.append({
            "puzzle": idx + 1,
            "cells_to_fill": cells_to_fill_list[idx],
            "puzzle_size": f'{puzzle.rows} x {puzzle.cols}',
            **config
        })
        if solved:
            solved_puzzles += 1
        else:
            non_solved_puzzles += 1

    # statistics
    average_time = sum(list_of_times) / len(list_of_times) if list_of_times else 0
    print(f"Average time for solving a puzzle: {average_time:.2f} seconds")
    print(f"Highest time for a single puzzle: {max(list_of_times):.2f} seconds")
    print(f"Solved {solved_puzzles} puzzles, did not solve {non_solved_puzzles} puzzles.")
    stats = Stats(times=list_of_times, cells_to_fill=cells_to_fill_list, solver_name="ga")
    stats.plot_all()

    with open("outputs/stats/best_configs_ga.json", "w") as f:
        json.dump(config_log, f, indent=2)
