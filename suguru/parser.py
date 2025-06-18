""" Parser for Suguru puzzles.
    It reads puzzles from a JSON file and converts them into Board objects.
    Each puzzle consists of a grid of cells and groups of cells.
    The grid is represented as a list of lists, where each cell can be a number or None.
    Fixed cells are marked as True in a separate list.
"""
import json
from typing import List
from .board import Board


class Parser:
    """
    Parser class for Suguru puzzles.
    It provides methods to parse a JSON object into a Board instance and to load puzzles from a file.
    """
    @staticmethod
    def parse_obj(data: dict) -> Board:
        """
        Parse a JSON object into a Board instance.
        :param data: JSON object containing puzzle data.
        :return: Board instance representing the puzzle.
        """
        rows, cols = data["rows"], data["cols"]
        cell_str = data["cells"]
        grid = [[None for _ in range(cols)] for _ in range(rows)]
        fixed = [[False for _ in range(cols)] for _ in range(rows)]

        for i in range(0, len(cell_str), 2):
            index = i // 2
            r, c = divmod(index, cols)
            val1 = int(cell_str[i])
            val2 = int(cell_str[i + 1])
            if val1 == val2 and val1 != 0:
                grid[r][c] = val1
                fixed[r][c] = True
            else:
                grid[r][c] = None
                fixed[r][c] = False

        groups = []
        for group_str in data["groups"]:
            group = []
            for i in range(0, len(group_str), 2):
                idx = int(group_str[i:i + 2])
                r, c = divmod(idx, cols)
                group.append((r, c))
            groups.append(group)

        return Board(rows, cols, grid, fixed, groups)

    @staticmethod
    def load_puzzles(file_path: str) -> List[Board]:
        """
        Load puzzles from a JSON file and return a list of Board instances.
        :param file_path: Path to the JSON file containing puzzles.
        :return: List of Board instances representing the puzzles.
        """
        with open(file_path) as f:
            data = json.load(f)  # a list of JSON objects
            return [Parser.parse_obj(obj) for obj in data]
