# stock.py

import csv

class Stock:
    _types = (str, int, float)
    __slots__ = ('name', '_shares', '_price')
    def __init__(self, name, shares, price):
        self.name = name
        self._shares = shares
        self._price = price

    @property
    def cost(self):
        return self.shares * self.price

    @property
    def shares(self):
        return self._shares
    @shares.setter
    def shares(self, n):
        if n > 0 and isinstance(n, self._types[1]):     # if n > 0 and isinstance(n, int):
            self._shares = n                #TypeError: '>' not supported between instances of 'str' and 'int'
        else:
            raise Exception('Must be a non-negative integer value')

    @property
    def price(self):
        return self._price
    @price.setter
    def price(self, p):
        if p > 0 and isinstance(p, self._types[2]):
            self._price = p
        else:
            raise Exception('Must be non-negative float value')

    def __repr__(self):
        return(f'Stock(\'{self.name}\',{self._shares},{self._price})')

    def __eq__(self, other):
        return isinstance(other, Stock) and ((self.name, self.shares, self.price) ==
                                             (other.name, other.shares, other.price))


    def sell(self, num:int):
        if not self.shares < num:
            self.shares -= num
        else:
            print('not enough shares for' + self.name)

    @classmethod
    def from_row(cls, row):
        values = [func(val) for func, val in zip(cls._types, row)]
        return cls(*values)

def read_portfolio(fname:str):
    data = []
    with open(fname) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            data.append(Stock.from_row(row))
    return data

def print_portfolio(p:list):
    print('%10s %10s %10s' % ('name', 'shares', 'price'))
    print(('-'*10+' ')*3)
    for stock in p[1:]:
        print(f'{stock.name:>10s} {stock.shares:>10d} {stock.price:>10.2f}')



