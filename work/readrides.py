# readrides.py

import csv
import tracemalloc
import collections


def test(func, filename):
    tracemalloc.start()
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = func(route, date, daytype, rides)
            records.append(record)
    print(func.__name__)
    print('Memory Use: Current %d, Peak %d' % tracemalloc.get_traced_memory())
    tracemalloc.stop()

def read_rides_as_dicts(fname):
    records = []
    with open(fname) as f:
        rows = csv.reader(f)
        headings = next(rows)
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = dic(route, date, daytype, rides)
            records.append(record)
    return records


# A tuple
def tup(a,b,c,d):
    return((a,b,c,d))

# A dictionary
def dic(a,b,c,d):
    return {'route': a, 'date': b, 'daytype': c, 'rides': d}

# A class
class Row:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

# A class with __slots__
class Row_s:
    __slots__ = ['route', 'date', 'daytype', 'rides']
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides

# A custom container
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

def read_rides_as_ridedata(filename):
    '''
    Read the bus ride data as a list of dicts
    '''
    records = RideData()      # <--- CHANGE THIS
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            route = row[0]
            date = row[1]
            daytype = row[2]
            rides = int(row[3])
            record = {
                'route': route,
                'date': date,
                'daytype': daytype,
                'rides' : rides
                }
            records.append(record)
    return records


if __name__ == '__main__':
    for f in [tup, dic, Row, Row_s]:
        test(f, 'Data/ctabus.csv')
    rows = read_rides_as_dicts('Data/ctabus.csv')
    print(len({s['route'] for s in rows}))
    print([r['rides'] for r in rows if r['route'] == '22' and r['date'] == '02/02/2011'])
    rides = {r['route']:0 for r in rows}
    for r in rows:
        rides[r['route']] += r['rides']
