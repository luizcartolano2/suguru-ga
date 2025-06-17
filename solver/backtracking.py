# backtracking.py
from suguru.board import Suguru


class SuguruBacktracking:
    def __init__(self, puzzle: Suguru):
        self.puzzle = puzzle
        self.rows = puzzle.rows
        self.cols = puzzle.cols
        self.grid = puzzle.grid
        self.fixed = puzzle.fixed
        self.groups = puzzle.groups

    def solve(self) -> bool:
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] is None:
                    group = self._get_group(r, c)
                    n = len(group)
                    for num in range(1, n + 1):
                        if self._is_valid(r, c, num):
                            self.grid[r][c] = num
                            if self.solve():
                                return True
                            self.grid[r][c] = None
                    return False
        return True

    def _get_group(self, row: int, col: int):
        for group in self.groups:
            if (row, col) in group:
                return group
        raise ValueError(f"No group found for cell ({row}, {col})")

    def _is_valid(self, row: int, col: int, num: int) -> bool:
        group = self._get_group(row, col)
        if any(self.grid[r][c] == num for r, c in group):
            return False

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.grid[nr][nc] == num:
                        return False
        return True
