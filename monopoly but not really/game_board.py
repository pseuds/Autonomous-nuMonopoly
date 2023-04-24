from properties import Property, Utility, Transport
from player import Player
from dice import Dices
import string, random
import random

class Game:
    def __init__(self):
        self._board = Board()
        self._round_count = 0 
        self._player_list = []

        self._current_player = None

        self._loser_seq = []

    @property
    def board(self):
        return self._board
    @board.setter
    def board(self, new):
        if isinstance(new, Board):
            self._board = new

    @property
    def round_no(self):
        return self._round_count
    @round_no.setter
    def round_no(self, new):
        self._round_count = new

    @property
    def player_list(self):
        return self._player_list
    @player_list.setter
    def player_list(self, new):
        self._player_list = new

    @property
    def get_next_player(self):
        if self._current_player == None:
            self._current_player = self.player_list[0]
        else:
            new_idx = self.player_list.index(self._current_player) +1
            try:
                self._current_player = self.player_list[new_idx]
            except:
                self._current_player = self.player_list[0]
        return self._current_player

    @property
    def get_prev_player(self):
        if self._current_player == None:
            self._current_player = self.player_list[0]
        else:
            new_idx = self.player_list.index(self._current_player) -1
            try:
                self._current_player = self.player_list[new_idx]
            except:
                self._current_player = self.player_list[-1]
        return self._current_player

    def check_valid_name(self, inp):
        valid_char = string.ascii_letters
        existing_players = [p.name.lower() for p in self.player_list]

        if len(inp) > 16:
            print('Invalid name. Your name should be less than 16 characters long.')
            return False
        
        if inp.lower() in existing_players:
            print('Name already exists. Please input a unique name.')
            return False

        if inp == '':
            print('Empty input.')
            return False
        
        for i in inp:
            if not i in valid_char:
                print('Invalid name. Please only use letters.')
                return False

        return True

    def add_to_player_list(self, new):
        if isinstance(new, Player):
            self._player_list.append(new)
        else:
            print('Input is not a player.')

    def add_to_losers(self, loser):
        self._loser_seq.append(loser)
        self._player_list.remove(loser)

    def setup(self):
        print("Setting up...\n")
        # initialise players
        while True:
            no_of_players = input('How many players? \n>>')
            if no_of_players in [str(i) for i in range(2,41)]:
                no_of_players = int(no_of_players)
                break
            else:
                print('Invalid input. Please only input numbers between 2 to 40.')
                
        f = open('names.txt', 'r')
        s = f.read()
        namels = s.split('\n')

        for n in range(no_of_players):
            while True:
                # inp_name = input(f"Player {n+1}'s name: \n>>")
                inp_name = random.choice(namels)
                if self.check_valid_name(inp_name) == True:
                    self.add_to_player_list(Player(inp_name, self.board.max_pos))
                    break
        
        # determine who goes first
        random.shuffle(self.player_list)
        name_ls = [p.name for p in self.player_list]
        print(f'The order of play is:', end=' \n')
        for name in name_ls:
            print(name, end=' --> ')
        
        print("\nSet up complete.")

    def main_game(self):
        while True:
            self.round_no = self.round_no + 1
            print(f"------------------\nRound {self.round_no}\n------------------")
            current_player = self.get_next_player
            bankrupt_bool = current_player.take_turn(self.board)
            if bankrupt_bool == True:
                print(f"{current_player.name} has gone bankrupt. They have been removed from the game.")
                self._current_player = self.get_prev_player
                self.add_to_losers(current_player)
                if self.check_end_game == True:
                    self.conclude()
                    break

    def conclude(self):
        print(f'Only {self.player_list[0].name} remain.')
        print(f'{self.player_list[0].name} is victorious.')
        self.add_to_losers(self.player_list[0])
        print('Rank: ')
        self._loser_seq.reverse()
        for index, player in enumerate(self._loser_seq):
            print(f"{index+1}. {player.name} - {player.wallet}")

    @property
    def check_end_game(self):
        if len(self.player_list) > 1:
            return False
        elif len(self.player_list) == 1:
            return True

class Board:

    def __init__(self):
        self._max_pos = 39
        self._tiles = self.init_tiles()

        self._go_income = 200
        self._jail_bail = 50

    def init_tiles(self):
        tiles = {i:None for i in range(self.max_pos+1)}

        # initialise properties
        f = open('init_properties.txt', 'r')
        s = f.read()
        ls_lines = s.split('\n')
        # each line is one property
        for l in ls_lines[1:]:
            info = l.split(',')
            for index, i in enumerate(info):
                info[index] = i.strip()
            tiles[int(info[0])] = Property(int(info[0]),info[1],int(info[2]),int(info[3]),int(info[4]),int(info[5]),int(info[6]),int(info[7]),int(info[8]),int(info[9]),int(info[10]))
            
        # initialise utilities
        f = open('init_utilities.txt', 'r')
        s = f.read()
        ls_lines = s.split('\n')
        for l in ls_lines:
            info = l.split(',')
            tiles[int(info[0])] = Utility(int(info[0]), info[1], 150, 75)
        
        # initialise transport
        f = open('init_transport.txt', 'r')
        s = f.read()
        ls_lines = s.split('\n')
        for l in ls_lines:
            info = l.split(',')
            tiles[int(info[0])] = Transport(int(info[0]), info[1], 200, 100)
        
        # initialise others
        tiles[0] = 'Go'
        tiles[10] = 'Just Visiting/Jail'
        tiles[20] = 'Free Parking'
        tiles[30] = 'Go To Jail'

        for i in [7,22,36]:
            tiles[i] = 'Chance'

        for i in [2,17,33]:
            tiles[i] = 'Community Chest'

        tiles[4] = 'Income Tax'
        tiles[38] = 'Luxury Tax'

        return tiles
    
    @property
    def max_pos(self):
        return self._max_pos
    
    @property
    def tiles(self):
        return self._tiles

    @property
    def go_income(self):
        return self._go_income

    @property
    def jail_bail(self):
        return self._jail_bail

    def get_tile(self, pos):
        t = self.tiles
        return t[pos]

    def get_name_pos(self, pos):
        t = self.tiles
        if isinstance(t[pos], Property) or isinstance(t[pos], Property) or isinstance(t[pos], Property):
            return t[pos].name
        else:
            return t[pos]