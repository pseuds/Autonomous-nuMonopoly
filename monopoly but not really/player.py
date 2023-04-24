from dice import Dices
from properties import Property, Utility, Transport

class Player:

    def __init__(self, name, max_pos):
        self._name = name
        self._max_pos = max_pos
        self._wallet = 1500
        self._currentpos = 0

        self._jailed_bool = False
        self._jailed_len_count = 0
        self._max_jail_len = 3

        self._owned_ls = []

    @property
    def name(self):
        return self._name

    @property
    def max_pos(self):
        return self._max_pos

    @property
    def wallet(self):
        return self._wallet
    @wallet.setter
    def wallet(self, new):
        if new < 0:
            raise AssertionError
        else:
            self._wallet = new

    @property
    def current_pos(self):
        return self._currentpos
    @current_pos.setter
    def current_pos(self, new):
        if new > self.max_pos:
            self._currentpos = new - self.max_pos -1
        else:
            self._currentpos = new
    
    @property
    def jailed_bool(self):
        return self._jailed_bool
    @jailed_bool.setter
    def jailed_bool(self, new):
        self._jailed_bool = new

    @property
    def jailed_len_count(self):
        return self._jailed_len_count
    @jailed_len_count.setter
    def jailed_len_count(self, new):
        self._jailed_len_count = new
    @property
    def max_jail_len(self):
        return self._max_jail_len

    @property
    def owned_ls(self):
        return self._owned_ls
    
    def add_to_owned_ls(self, prop):
        self._owned_ls.append(prop)
    def del_from_owned_ls(self, prop):
        self._owned_ls.remove(prop)

    @property
    def sorted_owned_ls(self):
        owned_ls = self.owned_ls
        sorted_owned_ls = sorted(owned_ls, key=lambda x: x.sell)
        return sorted_owned_ls

    def can_buy(self, cost):
        if cost*2 > self.wallet:
            return False
        else:
            return True

    def can_pay(self, cost):
        if cost > self.wallet:
            return False
        else:
            return True
    
    def prop_type_count(self, prop_type):
        count = 0
        for prop in self.owned_ls:
            if isinstance(prop, prop_type):
                count += 1
        return count 

    def take_turn(self, board):
        bankrupt_bool = False
        print(f"{self.name}'s turn.")
        print(f'Current position: {self.current_pos} - {board.get_name_pos(self.current_pos)}')
        if self.jailed_bool == True:
            print(f"{self.name} is in jail.")
            if self.can_pay(board.jail_bail):
                self.jailed_bool = False
                self.jailed_len_count = 0
                old_wallet = self.wallet
                self.wallet = self.wallet - board.jail_bail
                print(f"{self.name} paid ${board.jail_bail} to get out of jail.")
                print(f"{self.name}'s wallet: ${old_wallet} --> ${self.wallet}")
            else:
                if self.jailed_len_count == self.max_jail_len:
                    print(f"{self.name} have stayed for the maximum jail length. They have been kicked from the game.")
                    return True
                else:
                    print(f"{self.name} cannot afford the bail. Their turn has been skipped.")
                    self.jailed_len_count = self.jailed_len_count + 1
                    return bankrupt_bool
        while True:
            d = Dices()
            d_vals = d.dice_values
            extra_turn = d.same_dices
            print(f"{self.name} rolled {d_vals[0]},{d_vals[1]}.")
            pass_go_bool = self.to_move(d.sum_dices)
            print(f'Current position: {self.current_pos} - {board.get_name_pos(self.current_pos)}')
            current_tile = board.get_tile(self.current_pos)
            bankrupt_bool = self.tile_action(self.current_pos, current_tile, board, d.sum_dices, pass_go_bool)
            if extra_turn == False:
                break
            else:
                print(f'Since {self.name} rolled doubles, take another turn.')
        return bankrupt_bool

    def to_move(self, distance):
        new_pos = self.current_pos + distance
        self.current_pos = new_pos
        if new_pos > self.max_pos:
            return True
        else:
            return False
        
    def tile_action(self, pos, current_tile, board, dice_values, pass_go_bool):
        bankrupt_bool = False
        if pass_go_bool == True:
            old_wallet = self.wallet
            self.wallet = self.wallet + board.go_income
            print(f"{self.name} passed GO. Received ${board.go_income}.")
            print(f"{self.name}'s wallet: ${old_wallet} --> ${self.wallet}")
        if isinstance(current_tile, Property) or isinstance(current_tile, Utility) or isinstance(current_tile, Transport):
            # if current tile not owned
            if current_tile.owned_bool == False and self.can_buy(current_tile.price) == True:
                old_wallet = self.wallet
                self.to_buy(pos, current_tile, board)
                print(f"{self.name} bought {current_tile.name} for ${current_tile.price}.")
                print(f"{self.name}'s wallet: ${old_wallet} --> ${self.wallet}")
            # if current tile is owned
            elif current_tile.owned_bool == True:
                # if owner is oneself, buy house at current tile
                if isinstance(current_tile, Property) and current_tile.owner == self:
                    buy_bool = self.can_buy(current_tile.hotel_cost)
                    if buy_bool == True:
                        self.to_buy_house(current_tile)
                # if owner is others
                else:
                    if isinstance(current_tile, Property):
                        bankrupt_bool = self.pay_up_else_sell(current_tile, current_tile.rentvalue)
                    elif isinstance(current_tile, Utility):
                        bankrupt_bool = self.pay_up_else_sell(current_tile, current_tile.utilities_rentvalue(dice_values, current_tile.owner.prop_type_count(Utility)))
                    elif isinstance(current_tile, Transport):
                        bankrupt_bool = self.pay_up_else_sell(current_tile, current_tile.transport_rentvalue(current_tile.owner.prop_type_count(Transport)))
        elif current_tile == 'Go To Jail':
            self.jailed_bool = True
            self.current_pos = 10

        return bankrupt_bool

    def to_buy(self, pos, current_tile, board):
        current_tile.owned_bool = True
        current_tile.owner = self
        self.wallet = self.wallet - current_tile.price
        self.add_to_owned_ls(current_tile)
    
    def to_buy_house(self, current_tile):
        if current_tile.house_count < 5:
            current_tile.house_count = current_tile.house_count + 1
            old_wallet = self.wallet
            self.wallet = self.wallet - current_tile.hotel_cost
            print(f"{self.name} bought a house at {current_tile.name} for ${current_tile.hotel_cost}.")
            print(f"Current number of houses at {current_tile.name}: {current_tile.house_count}")
            print(f"{self.name}'s wallet: ${old_wallet} --> ${self.wallet}")

    def to_sell(self):
        sold_house = False
        # sell houses first 
        for prop in self.sorted_owned_ls:
            if isinstance(prop, Property):
                if prop.house_count > 0:
                    sold_house = True
                    prop.house_count = prop.house_count - 1
                    old_wallet = self.wallet
                    self.wallet = self.wallet + prop.sell_house_value
                    print(f"{self.name} sold a house at {prop.name} for {prop.sell_house_value}.")
                    print(f"Current number of houses at {prop.name}: {prop.house_count}")
                    print(f"{self.name}'s wallet: ${old_wallet} --> ${self.wallet}")
                    break
        # then sell prop
        if sold_house == True:
            return False
        elif len(self.owned_ls) > 0 and sold_house == False:
            prop_to_sell = self.sorted_owned_ls[0]
            prop_to_sell.owned_bool = False
            prop_to_sell.owner = None
            old_wallet = self.wallet
            self.wallet = self.wallet + prop_to_sell.sell
            self.del_from_owned_ls(prop_to_sell)
            print(f'{self.name} sold {prop_to_sell.name} for ${prop_to_sell.sell}.')
            print(f"{self.name}'s wallet: ${old_wallet} --> ${self.wallet}")
            return False
        else:
            return True

    def pay_up_else_sell(self, current_tile, rentvalue):
        owner_of_tile = current_tile.owner
        bankrupt_bool = False
        while True:
            if self.can_pay(rentvalue):
                old_wallet = self.wallet
                receiver_old_wallet = owner_of_tile.wallet
                self.to_pay_rent(rentvalue)
                owner_of_tile.to_receive_rent(rentvalue)
                print(f'{self.name} paid ${rentvalue} to {owner_of_tile.name}.')
                print(f"{self.name}'s wallet: ${old_wallet} --> ${self.wallet}")
                print(f"{owner_of_tile.name}'s wallet: ${receiver_old_wallet} --> ${owner_of_tile.wallet}")
                break
            else:
                print(f"{self.name} cannot afford to pay the rent. \n{self.name}'s wallet: ${self.wallet}, Rent: ${rentvalue}")
                bankrupt_bool = self.to_sell()
                if bankrupt_bool == True:
                    break
        return bankrupt_bool

    def to_pay_rent(self, rent):
        self.wallet = self.wallet - rent
    def to_receive_rent(self, rent):
        self.wallet = self.wallet + rent