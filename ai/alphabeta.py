import copy
import random
from ai.base_ai import BaseAI
from game.logic import is_winner, is_draw

class AlphaBetaAI(BaseAI):
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
                            if 0 <= r < size and 0 <= c < size and grid[r][c] is None:
                                candidates.add((r, c))
        if not candidates:
            candidates.add((size // 2, size // 2))  # start center if empty
        return candidates

    def get_move(self, grid):
        best_score = float("-inf")
        best_moves = []
        size = len(grid)

        for row, col in self.get_candidate_moves(grid):
            if grid[row][col] is None:
                new_grid = copy.deepcopy(grid)
                new_grid[row][col] = self.color
                score = self.alphabeta(new_grid, self.max_depth - 1, float("-inf"), float("inf"), False, row, col)
                if score > best_score:
                    best_score = score
                    best_moves = [(row, col)]
                elif score == best_score:
                    best_moves.append((row, col))

        if best_moves:
            return random.choice(best_moves)
        return None

    def alphabeta(self, grid, depth, alpha, beta, maximizing, last_row, last_col):
        size = len(grid)
        if is_winner(grid, size, last_row, last_col):
            return 1000 if grid[last_row][last_col] == self.color else -1000
        if is_draw(grid) or depth == 0:
            return self.evaluate(grid)

        if maximizing:
            max_eval = float("-inf")
            for row, col in self.get_candidate_moves(grid):
                if grid[row][col] is None:
                    grid[row][col] = self.color
                    eval = self.alphabeta(grid, depth - 1, alpha, beta, False, row, col)
                    grid[row][col] = None
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # beta cut-off
            return max_eval
        else:
            min_eval = float("inf")
            for row, col in self.get_candidate_moves(grid):
                if grid[row][col] is None:
                    grid[row][col] = self.opponent
                    eval = self.alphabeta(grid, depth - 1, alpha, beta, True, row, col)
                    grid[row][col] = None
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # alpha cut-off
            return min_eval

    def evaluate(self, grid):
        # Defensive check: if opponent can win next move, return very negative score
        for row, col in self.get_candidate_moves(grid):
            grid[row][col] = self.opponent
            if is_winner(grid, len(grid), row, col):
                grid[row][col] = None
                return float("-inf")
            grid[row][col] = None

        # Simple heuristic: difference in stone counts
        my_count = sum(row.count(self.color) for row in grid)
        opp_count = sum(row.count(self.opponent) for row in grid)
        return my_count - opp_count
