class Property():

    def __init__(self, pos, name, price, zero, one, two, three, four, hotel, hotel_cost, sell):
        self._pos = pos
        self._name = name
        self._price = price

        self._rentvalues = [zero, one, two, three, four, hotel]

        self._hotel_cost = hotel_cost
        self._sell = sell

        self._owned_bool = False
        self._owner = None

        self._house_count = 0

    @property
    def pos(self):
        return self._pos

    @property
    def name(self):
        return self._name
    
    @property
    def price(self):
        return self._price

    @property
    def get_rentvalues(self):
        return self._rentvalues
    
    @property
    def rentvalue(self):
        if self.owned_bool == True:
            return self.get_rentvalues[self.house_count]
    
    @property
    def hotel_cost(self):
        return self._hotel_cost
    
    @property
    def sell(self):
        return self._sell
    
    @property
    def sell_house_value(self):
        return self._hotel_cost //2

    @property
    def owned_bool(self):
        return self._owned_bool

    @owned_bool.setter
    def owned_bool(self, new_bool):
        self._owned_bool = new_bool

    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, new):
        self._owner = new
    
    @property
    def house_count(self):
        return self._house_count
    @house_count.setter
    def house_count(self, new):
        self._house_count = new

    def property_rentvalue(self):
        rentvalue = self.rentvalue
        return rentvalue, self.owner
        
    def buy(self, buyer_name):
        if self.owned_bool == False:
            self.owned_bool = True
            self.owner = buyer_name
        else:
            raise AssertionError
    
    def sell_property(self):
        if self.owned_bool == True:
            self.owned_bool = False
            self.owner = None
        else:
            raise AssertionError

    def __str__(self):
        return self.name

class Utility:

    def __init__(self, pos, name, price, sell):
        self._pos = pos
        self._name = name
        self._price = price
        self._sell = sell

        self._owned_bool = False
        self._owner = None

    @property
    def pos(self):
        return self._pos

    @property
    def name(self):
        return self._name
    
    @property
    def price(self):
        return self._price
    
    @property
    def sell(self):
        return self._sell
    
    @property
    def owned_bool(self):
        return self._owned_bool

    @owned_bool.setter
    def owned_bool(self, new_bool):
        self._owned_bool = new_bool

    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, new):
        self._owner = new

    def utilities_rentvalue(self, dice_value, owned_no):
        if not owned_no in [1,2]:
            print('Error invalid value: ', owned_no)
            raise ValueError
        elif owned_no == 1:
            return dice_value * 4
        elif owned_no == 2:
            return dice_value * 10
    
    def buy(self, buyer_name):
        if self.owned_bool == False:
            self.owned_bool = True
            self.owner = buyer_name
        else:
            raise AssertionError
    
    def sell_property(self):
        if self.owned_bool == True:
            self.owned_bool = False
            self.owner = None
        else:
            raise AssertionError

    def __str__(self):
        return self.name

class Transport:

    def __init__(self, pos, name, price, sell):
        self._pos = pos
        self._name = name
        self._price = price
        self._sell = sell

        self._owned_bool = False
        self._owner = None

    @property
    def pos(self):
        return self._pos

    @property
    def name(self):
        return self._name
    
    @property
    def price(self):
        return self._price
    
    @property
    def sell(self):
        return self._sell
    
    @property
    def owned_bool(self):
        return self._owned_bool

    @owned_bool.setter
    def owned_bool(self, new_bool):
        self._owned_bool = new_bool

    @property
    def owner(self):
        return self._owner
    
    @owner.setter
    def owner(self, new):
        self._owner = new

    def transport_rentvalue(self, owned_no):
        if not owned_no in [1,2,3,4]:
            raise ValueError
        else:
            rent_ls = [0,25,50,100,200]
            return rent_ls[owned_no]

    def buy(self, buyer_name):
        if self.owned_bool == False:
            self.owned_bool = True
            self.owner = buyer_name
        else:
            raise AssertionError
    
    def sell_property(self):
        if self.owned_bool == True:
            self.owned_bool = False
            self.owner = None
        else:
            raise AssertionError

    def __str__(self):
        return self.name