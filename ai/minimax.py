import copy
import random
from ai.base_ai import BaseAI
from game.logic import is_winner, is_draw


class MiniMaxAI(BaseAI):
    def __init__(self, color, max_depth=2):
        super().__init__(color)
        self.opponent = "red" if color == "blue" else "blue"
        self.max_depth = max_depth

    def get_candidate_moves(self, grid):
        size = len(grid)
        candidates = set()
        for row in range(size):
            for col in range(size):
                if grid[row][col] is not None:
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            r, c = row + dr, col + dc
                            if 0 <= r < size and 0 <= c < size:
                                if grid[r][c] is None:
                                    candidates.add((r, c))
        if not candidates:
            # If the board is empty, start in the center
            candidates.add((size // 2, size // 2))
        return candidates

    def get_move(self, grid):
        best_score = float("-inf")
        best_moves = []
        size = len(grid)

        # for row in range(size):
        #     for col in range(size):
        for row, col in self.get_candidate_moves(grid):
            if grid[row][col] is None:
                new_grid = copy.deepcopy(grid)
                new_grid[row][col] = self.color
                score = self.minimax(new_grid, self.max_depth - 1, False, row, col)
                if score > best_score:
                    best_score = score
                    best_moves = [(row, col)]
                elif score == best_score:
                    best_moves.append((row, col))

        if best_moves:
            return random.choice(best_moves)
        return None

    def minimax(self, grid, depth, maximizing, last_row, last_col):
        size = len(grid)
        if is_winner(grid, size, last_row, last_col):
            return 1000 if grid[last_row][last_col] == self.color else -1000
        if is_draw(grid) or depth == 0:
            return self.evaluate(grid)

        if maximizing:
            max_eval = float("-inf")
            # for row in range(size):
            #     for col in range(size):
            for row, col in self.get_candidate_moves(grid):
                if grid[row][col] is None:
                    grid[row][col] = self.color
                    eval = self.minimax(grid, depth - 1, False, row, col)
                    grid[row][col] = None
                    max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float("inf")
            # for row in range(size):
            #     for col in range(size):
            for row, col in self.get_candidate_moves(grid):
                if grid[row][col] is None:
                    grid[row][col] = self.opponent
                    eval = self.minimax(grid, depth - 1, True, row, col)
                    grid[row][col] = None
                    min_eval = min(min_eval, eval)
            return min_eval

    def evaluate(self, grid):
        # If opponent has a win next move, return a very negative score
        for row, col in self.get_candidate_moves(grid):
            grid[row][col] = self.opponent
            if is_winner(grid, len(grid), row, col):
                grid[row][col] = None
                return float("-inf")
            grid[row][col] = None
        # Otherwise, simple piece count
        # Simple evaluation: count difference in stones
        my_count = sum(row.count(self.color) for row in grid)
        opp_count = sum(row.count(self.opponent) for row in grid)
        return my_count - opp_count
