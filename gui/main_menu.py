import pygame
import sys

class MainMenu:
    def __init__(self, width=400, height=300):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Gomoku - Select Mode")
        self.font = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()
        self.options = ["Human vs AI", "AI vs AI"]
        self.selected = 0

    def draw(self):
        self.screen.fill((30, 30, 30))
        title = self.font.render("Select Game Mode", True, (255, 255, 255))
        self.screen.blit(title, (80, 40))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (200, 200, 200)
            text = self.font.render(option, True, color)
            self.screen.blit(text, (100, 120 + i * 50))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        print(f"Selected mode: {self.options[self.selected]}")
                        running = False  # Exit menu to start game mode

            self.draw()
            pygame.display.flip()
            self.clock.tick(30)

        return self.selected

if __name__ == "__main__":
    menu = MainMenu()
    choice = menu.run()
    print(f"User selected option {choice}")
