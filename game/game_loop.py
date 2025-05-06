import pygame
import sys
from gui.board import Board

def run_game_loop():
    pygame.init()
    board = Board()
    screen = pygame.display.set_mode((board.width, board.height))
    pygame.display.set_caption("Gomoku")

    clock = pygame.time.Clock()
    running = True
    game_over = False
    result_text = ""
    font = pygame.font.SysFont(None, 48)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    pos = pygame.mouse.get_pos()
                    status, player = board.select_cell(pos)

                    if status == 'win':
                        result_text = f"Game Over! {player.capitalize()} wins!"
                        print(result_text)
                        game_over = True

                    elif status == 'draw':
                        result_text = "Game Over! It's a draw!"
                        print(result_text)
                        game_over = True

                    elif status == 'invalid':
                        print("Invalid move! Cell already occupied.")

                else:
                    #reset game after its over
                    board = Board() 
                    game_over = False
                    result_text = ""
                    print("Game restarted.")

            elif event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_r:
                    #restart
                    board = Board()
                    game_over = False
                    result_text = ""
                    print("Game restarted.")

        board.draw(screen)

        if game_over:
            
            text_surface = font.render(result_text, True, (255, 255, 255))
            rect = text_surface.get_rect(center=(board.width // 2, board.height // 2))
            screen.blit(text_surface, rect)

            
            instr_surface = font.render("Click or press 'R' to restart", True, (200, 200, 200))
            instr_rect = instr_surface.get_rect(center=(board.width // 2, board.height // 2 + 50))
            screen.blit(instr_surface, instr_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()