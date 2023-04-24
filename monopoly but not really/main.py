from properties import Property, Utility, Transport
from game_board import Game, Board
from player import Player
from random import seed

def main(seed_no):
    seed(seed_no)
    g = Game()
    print('--------------------------------------------------------')
    g.setup()
    print('--------------------------------------------------------')
    g.main_game()
    return

main(100)