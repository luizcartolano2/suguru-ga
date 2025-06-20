""" Board class for Suguru puzzle representation and visualization.

"""
import colorsys
from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches


class Board:
    """
    Board class for Suguru puzzles.
    It represents the grid, fixed cells, and groups of cells.
    It provides methods to display the board and validate the puzzle.

    Attributes:
        rows (int): Number of rows in the grid.
        cols (int): Number of columns in the grid.
        grid (List[List[Optional[int]]]): 2D list representing the grid, where each cell can be a number or None.
        fixed (List[List[bool]]): 2D list indicating whether a cell is fixed (True) or not (False).
        groups (List[List[tuple[int, int]]]): List of groups, where each group is a list of tuples representing cell coordinates.
    """
    def __init__(self, rows: int, cols: int, grid: List[List[Optional[int]]], fixed: List[List[bool]], groups: List[List[tuple[int, int]]]):
        self.rows = rows
        self.cols = cols
        self.grid = grid
        self.fixed = fixed
        self.groups = groups

    def display(self, path: Optional[str] = None):
        """
        Display the Suguru board using matplotlib.
        :param path: Optional[str]: Path to save the figure. If None, it will display the figure.
        :return: a matplotlib figure showing the Suguru board with groups colored and numbers displayed.
        """
        fig, ax = plt.subplots(figsize=(self.cols, self.rows))
        ax.set_xticks(np.arange(self.cols + 1))
        ax.set_yticks(np.arange(self.rows + 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xlim(0, self.cols)
        ax.set_ylim(0, self.rows)
        ax.grid(True)
        ax.invert_yaxis()

        def get_unique_colors(n):
            hues = np.linspace(0, 1, n, endpoint=False)
            return [colorsys.hsv_to_rgb(h, 0.5, 1.0) for h in hues]

        group_colors = get_unique_colors(len(self.groups))

        # Color each group
        for group_index, group in enumerate(self.groups):
            color = group_colors[group_index]
            for r, c in group:
                rect = patches.Rectangle((c, r), 1, 1, linewidth=0, facecolor=color)
                ax.add_patch(rect)

        # Overlay the numbers
        for r in range(self.rows):
            for c in range(self.cols):
                value = self.grid[r][c]
                if value is not None:
                    ax.text(
                        c + 0.5, r + 0.5, str(value),
                        ha='center', va='center',
                        fontsize=14,
                        color='black' if self.fixed[r][c] else 'dimgray',
                        fontweight='bold' if self.fixed[r][c] else 'normal'
                    )

        plt.tight_layout()
        if path:
            plt.savefig(path)
        else:
            plt.show()
        plt.close(fig)

    def validate(self) -> bool:
        """
        Validate the Suguru board according to the following rules:
        1. All groups must contain unique values from 1 to len(group).
        2. No adjacent (even diagonal) duplicates.
        :return: bool: True if the board is valid, False otherwise.
        """
        # 1. All groups must contain unique values from 1 to len(group)
        for group in self.groups:
            values = [self.grid[r][c] for r, c in group]
            if None in values:
                print("Validation failed: Group contains None values.")
                return False
            if sorted(values) != list(range(1, len(values) + 1)):
                print("Validation failed: Group values are not unique or out of range.")
                return False

        # 2. No adjacent (even diagonal) duplicates
        for r in range(self.rows):
            for c in range(self.cols):
                val = self.grid[r][c]
                if val is None:
                    print(f"Validation failed: Grid contains None values at ({r}, {c}).")
                    return False
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.grid[nr][nc] == val:
                                print(f"Validation failed: Duplicate value {val} found at ({r}, {c}) and ({nr}, {nc}).")
                                return False
        return True
