""" Backtracking solver for Suguru puzzles.
It uses a recursive backtracking algorithm to fill the grid with numbers according to Suguru rules.

"""
from suguru.board import Board


class SuguruBacktracking:
    """
    Backtracking solver for Suguru puzzles.
    It attempts to fill the grid with numbers from 1 to n, where n is the size of the group,
    ensuring that no number repeats in any group or adjacent cells.

    Attributes:
        puzzle (Board): The Suguru puzzle to be solved.
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        grid (List[List[Optional[int]]]): 2D list representing the grid.
        fixed (List[List[bool]]): 2D list indicating whether a cell is fixed or not.
        groups (List[List[tuple[int, int]]]): List of groups, where each group is a list of tuples representing cell coordinates.
    """
    def __init__(self, puzzle: Board):
        self.puzzle = puzzle
        self.rows = puzzle.rows
        self.cols = puzzle.cols
        self.grid = puzzle.grid
        self.fixed = puzzle.fixed
        self.groups = puzzle.groups

    def solve(self) -> bool:
        """
        Solve the Suguru puzzle using backtracking.
        It iterates through each cell in the grid, checks if it is empty,
        and tries to fill it with numbers from 1 to n, where n is the size of the group.
        :return: bool: True if the puzzle is solved, False if no solution exists.
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] is None:
                    group = self.__get_group(r, c)
                    n = len(group)
                    for num in range(1, n + 1):
                        if self.__is_valid(r, c, num):
                            self.grid[r][c] = num
                            if self.solve():
                                return True
                            self.grid[r][c] = None
                    return False
        return True

    def __get_group(self, row: int, col: int):
        """
        Get the group that contains the cell at (row, col).
        :param row: an integer representing the row index of the cell.
        :param col: an integer representing the column index of the cell.
        :return: List[tuple[int, int]]: The group containing the cell, represented as a list of tuples (row, col).
        :raise ValueError: If no group is found for the given cell.
        """
        for group in self.groups:
            if (row, col) in group:
                return group
        raise ValueError(f"No group found for cell ({row}, {col})")

    def __is_valid(self, row: int, col: int, num: int) -> bool:
        """
        Check if placing the number `num` in the cell at (row, col) is valid according to Suguru rules.
        :param row: an integer representing the row index of the cell.
        :param col: an integer representing the column index of the cell.
        :param num: an integer representing the number to be placed in the cell.
        :return: bool: True if placing the number is valid, False otherwise.
        """
        group = self.__get_group(row, col)
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
