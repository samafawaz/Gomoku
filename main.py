import pygame
import sys
from gui.main_menu import MainMenu
from gui.board import Board
from game.game_loop import run_game_loop

def human_vs_ai():
    #lesa
    print("Starting Human vs AI mode")
    run_game_loop()

def ai_vs_ai(): #not implemented yet
    print("Starting AI vs AI mode")
    run_game_loop()

def main():
    pygame.init()
    menu = MainMenu()
    choice = menu.run()

    if choice == 0:
        human_vs_ai()
    elif choice == 1:
        ai_vs_ai()

if __name__ == "__main__":
   run_game_loop()