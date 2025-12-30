# reader.py

import csv
import collections
from abc import ABC, abstractmethod


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

def read_csv_as_instances(filename, cls):
    parser = InstanceCSVParser(cls)
    return parser.parse(filename)

def read_csv_as_dicts(filename, types):
    parser = DictCSVParser(types)
    return parser.parse(filename)


class CSVParser(ABC):

    def parse(self, filename):
        records = []
        with open(filename) as f:
            rows = csv.reader(f)
            headers = next(rows)
            for row in rows:
                record = self.make_record(headers, row)
                records.append(record)
        return records

    @abstractmethod
    def make_record(self, headers, row):
        pass

class DictCSVParser(CSVParser):
    def __init__(self, types):
        self.types = types

    def make_record(self, headers, row):
        return { name: func(val) for name, func, val in zip(headers, self.types, row) }

class InstanceCSVParser(CSVParser):
    def __init__(self, cls):
        self.cls = cls

    def make_record(self, headers, row):
        return self.cls.from_row(row)

