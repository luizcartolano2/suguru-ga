# model.py
import colorsys

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional

from matplotlib import patches


class Suguru:
    def __init__(self, rows: int, cols: int, grid: List[List[Optional[int]]], fixed: List[List[bool]], groups: List[List[tuple[int, int]]]):
        self.rows = rows
        self.cols = cols
        self.grid = grid
        self.fixed = fixed
        self.groups = groups

    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import numpy as np
    import colorsys

    def display(self):
        fig, ax = plt.subplots(figsize=(self.cols, self.rows))
        ax.set_xticks(np.arange(self.cols + 1))
        ax.set_yticks(np.arange(self.rows + 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_xlim(0, self.cols)
        ax.set_ylim(0, self.rows)
        ax.grid(True)
        ax.invert_yaxis()

        # Gerar uma cor única para cada grupo com base no HSV
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
        plt.show()

    def validate(self) -> bool:
        # 1. All groups must contain unique values from 1 to len(group)
        for group in self.groups:
            values = [self.grid[r][c] for r, c in group]
            if None in values:
                return False
            if sorted(values) != list(range(1, len(values) + 1)):
                return False

        # 2. No adjacent (even diagonal) duplicates
        for r in range(self.rows):
            for c in range(self.cols):
                val = self.grid[r][c]
                if val is None:
                    return False
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.rows and 0 <= nc < self.cols:
                            if self.grid[nr][nc] == val:
                                return False
        return True
