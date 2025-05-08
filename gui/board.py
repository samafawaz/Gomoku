import pygame
from game.logic import is_winner, is_draw


class Board:
    def __init__(self, size=15, cell_size=40, margin=20):
        self.size = size
        self.cell_size = cell_size
        self.margin = margin
        self.width = size * cell_size + margin * 2
        self.height = self.width
        self.bg_color = (65, 65, 65)
        self.line_color = (255, 255, 255)

        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.selected_cell = None
        self.current_turn = "red"

    def draw(self, screen):
        screen.fill(self.bg_color)

        for i in range(self.size + 1):
            x = self.margin + i * self.cell_size
            pygame.draw.line(
                screen,
                self.line_color,
                (x, self.margin),
                (x, self.height - self.margin),
                2,
            )

        for j in range(self.size + 1):
            y = self.margin + j * self.cell_size
            pygame.draw.line(
                screen,
                self.line_color,
                (self.margin, y),
                (self.width - self.margin, y),
                2,
            )

        for row in range(self.size):
            for col in range(self.size):
                stone = self.grid[row][col]
                if stone is not None:
                    self.draw_stone(screen, row, col, stone)

    def draw_stone(self, screen, row, col, color):
        center_x = self.margin + col * self.cell_size
        center_y = self.margin + row * self.cell_size
        radius = self.cell_size // 2 - 6

        shadow_offset = 4
        shadow_color = (30, 30, 30)

        pygame.draw.circle(
            screen,
            shadow_color,
            (center_x + shadow_offset, center_y + shadow_offset),
            radius,
        )

        if color == "blue":
            pygame.draw.circle(screen, (0, 0, 255), (center_x, center_y), radius)
            pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius, 1)
        elif color == "red":
            pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), radius)
            pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius, 1)

    def get_cell_from_pos(self, pos):
        x, y = pos
        if (
            x < self.margin - self.cell_size // 2
            or x > self.width - self.margin + self.cell_size // 2
        ):
            return None
        if (
            y < self.margin - self.cell_size // 2
            or y > self.height - self.margin + self.cell_size // 2
        ):
            return None

        col = round((x - self.margin) / self.cell_size)
        row = round((y - self.margin) / self.cell_size)

        if 0 <= row < self.size and 0 <= col < self.size:
            return row, col
        return None

    def select_cell(self, pos):
        cell = self.get_cell_from_pos(pos)
        if cell:
            row, col = cell
            if self.grid[row][col] is None:
                self.grid[row][col] = self.current_turn
                self.selected_cell = cell

                if is_winner(self.grid, self.size, row, col):
                    return "win", self.current_turn

                if is_draw(self.grid):
                    return "draw", None

                self.toggle_turn()
                return "continue", None
            else:
                self.selected_cell = None
                return "invalid", None
        else:
            self.selected_cell = None
            return "invalid", None

    def toggle_turn(self):
        self.current_turn = "blue" if self.current_turn == "red" else "red"
