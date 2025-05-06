import pygame
import sys
from gui.main_menu import MainMenu
from gui.board import Board

def human_vs_ai():
    # Placeholder: Replace with your actual Human vs AI game loop
    print("Starting Human vs AI mode")
    run_game_loop()

def ai_vs_ai():
    # Placeholder: Replace with your actual AI vs AI game loop
    print("Starting AI vs AI mode")
    run_game_loop()

def run_game_loop():
    board = Board()
    screen = pygame.display.set_mode((board.width, board.height))
    pygame.display.set_caption("Gomoku")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                board.select_cell(pos)

        board.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

def main():
    pygame.init()
    menu = MainMenu()
    choice = menu.run()

    if choice == 0:
        human_vs_ai()
    elif choice == 1:
        ai_vs_ai()

if __name__ == "__main__":
    main()
