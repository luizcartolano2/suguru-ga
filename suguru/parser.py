# parser.py
import json
from typing import List
from .board import Suguru


class SuguruParser:
    @staticmethod
    def parse_obj(data: dict) -> Suguru:
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
        # 00 08 09 10 16 --> celulas 0 8 9 10 16
        groups = []
        for group_str in data["groups"]:
            group = []
            for i in range(0, len(group_str), 2):
                idx = int(group_str[i:i + 2])
                r, c = divmod(idx, cols)
                group.append((r, c))
            groups.append(group)

        return Suguru(rows, cols, grid, fixed, groups)

    @staticmethod
    def load_puzzles(file_path: str) -> List[Suguru]:
        with open(file_path) as f:
            data = json.load(f)  # a list of JSON objects
            return [SuguruParser.parse_obj(obj) for obj in data]

