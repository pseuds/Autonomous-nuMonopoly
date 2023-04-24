from random import randint

class Dices:

    def __init__(self):
        self._dice_values = [randint(1,6), randint(1,6)]

    @property
    def sum_dices(self):
        return sum(self._dice_values)

    @property
    def dice_values(self):
        return (self._dice_values[0], self._dice_values[1])

    @property
    def same_dices(self):
        v = self.dice_values
        return v[0] == v[1] 