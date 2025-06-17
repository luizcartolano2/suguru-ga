import time

from suguru.parser import SuguruParser
from solver.backtracking import SuguruBacktracking

if __name__ == '__main__':
    puzzles = SuguruParser.load_puzzles("instances/easy.json")

    list_of_times = []
    solved_puzzles = 0
    non_solved_puzzles = 0

    for idx, puzzle in enumerate(puzzles):
        start_time = time.time()
        solver = SuguruBacktracking(puzzle)
        if solver.solve():
            # puzzle.display()
            end_time = time.time()
            if puzzle.validate():
                solved_puzzles += 1
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
