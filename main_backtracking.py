""" Main script to solve Suguru puzzles using backtracking algorithm.
    It loads puzzles from a JSON file, solves them, and displays statistics.
"""
import time

from suguru.parser import Parser
from solver.backtracking import SuguruBacktracking
from suguru.stats import Stats

if __name__ == '__main__':
    puzzles = Parser.load_puzzles("instances/easy.json")

    list_of_times = []
    cells_to_fill_list = [sum(row.count(False) for row in puzzle.fixed) for puzzle in puzzles]
    solved_puzzles = 0
    non_solved_puzzles = 0

    for idx, puzzle in enumerate(puzzles):
        start_time = time.time()
        solver = SuguruBacktracking(puzzle)
        if solver.solve():
            end_time = time.time()
            if puzzle.validate():
                solved_puzzles += 1
                puzzle.display(f'outputs/backtracking/solved_{idx + 1}.png')
            else:
                non_solved_puzzles += 1
        else:
            end_time = time.time()
            non_solved_puzzles += 1
        list_of_times.append(end_time - start_time)

    average_time = sum(list_of_times) / len(list_of_times) if list_of_times else 0

    print(f"Average time for solving a puzzle: {average_time:.2f} seconds")
    print(f"Highest time for a single puzzle: {max(list_of_times):.2f} seconds at {list_of_times.index(max(list_of_times)) + 1}th puzzle.")
    print(f"Solved {solved_puzzles} puzzles, did not solve {non_solved_puzzles} puzzles.")

    stats = Stats(times=list_of_times, cells_to_fill=cells_to_fill_list, solver_name="backtracking")
    stats.plot_all()
