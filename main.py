import pygame
import sys
from gui.main_menu import MainMenu
from gui.board import Board
from game.game_loop import run_game_loop

from ai.minimax import MiniMaxAI

# from ai.alphabeta import AlphaBetaAI


def main():
    pygame.init()
    while True:
        menu = MainMenu()
        choice = menu.run()

        if choice == 0:
            # Human vs AI
            ai = MiniMaxAI("blue", max_depth=3)
            run_game_loop(player1_type="human", player2_type="ai", ai2=ai)
        elif choice == 1:
            # AI vs AI
            ai1 = MiniMaxAI("red", max_depth=2)
            # ai2 = AlphaBetaAI("blue")
            ai2 = MiniMaxAI("blue", max_depth=2)
            run_game_loop(player1_type="ai", player2_type="ai", ai1=ai1, ai2=ai2)


if __name__ == "__main__":
    main()
