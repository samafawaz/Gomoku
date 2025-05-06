import pygame

class Board:
    def __init__(self, size=15, cell_size=40, margin=20):
        self.size = size
        self.cell_size = cell_size
        self.margin = margin
        self.width = size * cell_size + margin * 2
        self.height = self.width  # square board
        self.bg_color = (65, 65, 65)
        self.line_color = (255, 255, 255)         
        # self.highlight_color = (255, 0, 0)  # Red highlight for selected cell
        
        # Board state: None = empty, 'red' or 'blue' for stones
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        
        self.selected_cell = None
        
        # red always starts first in Gomoku
        self.current_turn = 'red'

    def draw(self, screen):
        screen.fill(self.bg_color)
        
        # Draw vertical lines (size + 1 to close grid)
        for i in range(self.size + 1):
            x = self.margin + i * self.cell_size
            pygame.draw.line(screen, self.line_color, (x, self.margin), (x, self.height - self.margin), 2)
        
        # Draw horizontal lines (size + 1 to close grid)
        for j in range(self.size + 1):
            y = self.margin + j * self.cell_size
            pygame.draw.line(screen, self.line_color, (self.margin, y), (self.width - self.margin, y), 2)
        
        # Draw stones on intersections
        for row in range(self.size):
            for col in range(self.size):
                stone = self.grid[row][col]
                if stone is not None:
                    self.draw_stone(screen, row, col, stone)
        
        # Highlight selected cell if any
        # if self.selected_cell:
        #     self.draw_highlight(screen, *self.selected_cell)

    def draw_stone(self, screen, row, col, color):
        center_x = self.margin + col * self.cell_size
        center_y = self.margin + row * self.cell_size
        radius = self.cell_size // 2 - 6

        # Shadow parameters
        shadow_offset = 4
        shadow_color = (30, 30, 30)  # dark gray shadow

        # Draw shadow circle slightly offset
        pygame.draw.circle(screen, shadow_color, (center_x + shadow_offset, center_y + shadow_offset), radius)

        # Draw main stone on top
        if color == 'blue':
            pygame.draw.circle(screen, (0, 0, 255), (center_x, center_y), radius)
            pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius, 1)
        elif color == 'red':
            pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), radius)
            pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius, 1)


    def get_cell_from_pos(self, pos):
        x, y = pos
        # Allow some margin for clicking near intersections
        if x < self.margin - self.cell_size // 2 or x > self.width - self.margin + self.cell_size // 2:
            return None
        if y < self.margin - self.cell_size // 2 or y > self.height - self.margin + self.cell_size // 2:
            return None

        # Find nearest intersection by rounding
        col = round((x - self.margin) / self.cell_size)
        row = round((y - self.margin) / self.cell_size)

        # Check boundaries
        if 0 <= row < self.size and 0 <= col < self.size:
            return row, col
        return None

    # def draw_highlight(self, screen, row, col):
    #     # Highlight the selected intersection with a red square around it
    #     rect_x = self.margin + col * self.cell_size
    #     rect_y = self.margin + row * self.cell_size
    #     rect = pygame.Rect(rect_x - self.cell_size // 2, rect_y - self.cell_size // 2,
    #                        self.cell_size, self.cell_size)
    #     pygame.draw.rect(screen, self.highlight_color, rect, 3)

    def select_cell(self, pos):
        cell = self.get_cell_from_pos(pos)
        if cell:
            row, col = cell
            # Place stone only if cell is empty
            if self.grid[row][col] is None:
                self.grid[row][col] = self.current_turn
                self.selected_cell = cell
                self.toggle_turn()
            else:
                self.selected_cell = None
        else:
            self.selected_cell = None

    def toggle_turn(self):
        self.current_turn = 'blue' if self.current_turn == 'red' else 'red'
