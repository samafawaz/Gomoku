import pygame
import sys
import time
from gui.board import Board


def run_game_loop(player1_type="human", player2_type="ai", ai1=None, ai2=None):
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
        current_player = board.current_turn
        is_ai_turn = (current_player == "red" and player1_type == "ai") or (
            current_player == "blue" and player2_type == "ai"
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over and not is_ai_turn:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    status, player = board.select_cell(pos)

                    if status == "win":
                        result_text = f"Game Over! {player.capitalize()} wins!"
                        game_over = True
                    elif status == "draw":
                        result_text = "Game Over! It's a draw!"
                        game_over = True
                    elif status == "invalid":
                        print("Invalid move! Cell already occupied.")

                elif event.type == pygame.KEYDOWN:
                    if game_over and event.key == pygame.K_r:
                        board = Board()
                        game_over = False
                        result_text = ""

        # Handle AI move
        if not game_over and is_ai_turn:
            pygame.display.flip()
            pygame.time.wait(400)  # Small delay for realism
            ai = ai1 if current_player == "red" else ai2
            if ai is not None:
                move = ai.get_move(board.grid)
                if move is not None:
                    row, col = move
                    print(f"AI ({current_player}) chooses move: row={row}, col={col}")  # print ai move
                    # Convert to pixel position for select_cell
                    pos = (
                        board.margin + col * board.cell_size,
                        board.margin + row * board.cell_size,
                    )
                    status, player = board.select_cell(pos)
                    if status == "win":
                        result_text = f"Game Over! {player.capitalize()} wins!"
                        game_over = True
                    elif status == "draw":
                        result_text = "Game Over! It's a draw!"
                        game_over = True

        board.draw(screen)

        if game_over:
            text_surface = font.render(result_text, True, (255, 255, 255))
            rect = text_surface.get_rect(center=(board.width // 2, board.height // 2))
            screen.blit(text_surface, rect)

            # First line
            instr_surface1 = font.render(
                "Click or press 'R' to restart", True, (200, 200, 200)
            )
            instr_rect1 = instr_surface1.get_rect(
                center=(board.width // 2, board.height // 2 + 50)
            )
            screen.blit(instr_surface1, instr_rect1)

            # Second line, just below the first
            instr_surface2 = font.render(
                "Press 'Esc' to return to main menu", True, (200, 200, 200)
            )
            instr_rect2 = instr_surface2.get_rect(
                center=(
                    board.width // 2,
                    board.height // 2 + 50 + instr_surface1.get_height() + 5,
                )
            )
            screen.blit(instr_surface2, instr_rect2)

        pygame.display.flip()
        clock.tick(60)

        # Reset game if game over and user clicks, presses R, or presses Escape

        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_r
                ):
                    board = Board()
                    game_over = False
                    result_text = ""
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Return to main menu
                    return  # This exits the game loop and returns control to main.py

    pygame.quit()
    sys.exit()
