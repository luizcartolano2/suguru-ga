import time

from suguru.parser import Parser
from solver.ga import SuguruGa

# puzzles = SuguruParser.load_puzzles("instances/easy.json")[-1:]
puzzles = Parser.load_puzzles("instances/easy.json")[0:1]
puzzles_5x5 = [p for p in puzzles if p.rows == 5]

list_of_times = []
list_of_times_by_empty_space = []
solved_puzzles = 0
non_solved_puzzles = 0

for idx, puzzle in enumerate(puzzles):
    start_time = time.time()
    solver = SuguruGa(puzzle, population_size=1000, generations=1000, mutation_rate=0.3)
    solved = solver.solve()
    list_of_times.append(time.time() - start_time)

    if solved.validate():
        solved_puzzles += 1
    else:
        non_solved_puzzles += 1

    solved.display()


average_time = sum(list_of_times) / len(list_of_times) if list_of_times else 0

print(f"Average time for solving a puzzle: {average_time:.2f} seconds")
print(f"Highest time for a single puzzle: {max(list_of_times):.2f} seconds")
print(f"Solved {solved_puzzles} puzzles, did not solve {non_solved_puzzles} puzzles.")
