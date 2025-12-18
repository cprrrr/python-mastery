# reader.py

import csv
import collections

def read_csv_as_dicts(fname:str, type:list):
    with open(fname) as f:
        rows = csv.reader(f)
        headers = next(rows)
        data = [{name:func(val) for name, func, val in zip(headers, type, row)}for row in rows]

    return data

class RideData(collections.abc.Sequence):
    def __init__(self):
        # Each value is a list with all the values (a column)
        self.routes = []
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self):
        # All lists assumed to have the same length
        return len(self.routes)

    def __getitem__(self, index):
        if isinstance(index, int):
            res = {'route': self.routes[index],
                   'date': self.dates[index],
                   'daytype': self.daytypes[index],
                   'rides': self.numrides[index]}

        elif isinstance(index, slice):
            start, stop, step = index.start, index.stop, index.step
            start = start if start is not None else 0
            stop = stop if stop is not None else len(self.routes)
            step = step if step is not None else 1
            lis = range(start, stop, step)
            res = [{'route': self.routes[i],
                'date': self.dates[i],
                'daytype': self.daytypes[i],
                'rides': self.numrides[i]} for i in lis]
        else:
            raise TypeError('only accept an int or a slice')
        return res

    def append(self, d):
        self.routes.append(d['route'])
        self.dates.append(d['date'])
        self.daytypes.append(d['daytype'])
        self.numrides.append(d['rides'])

def read_csv_as_columns(fname, types):
    data = RideData()
    with open(fname) as f:
        rows = csv.reader(f)
        headers = next(rows)
        for row in rows:
            data.append({n:t(d) for n, t, d in zip(headers, types, row) })
    return data

