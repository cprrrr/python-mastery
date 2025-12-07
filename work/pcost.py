# pcost.py
import sys

def cost(fname):
    with open(fname) as f:
        tcost = sum(float(lines.split()[1]) * float(lines.split()[2]) for lines in f)
    return tcost

def cost2(fname):
    total_cost = 0.0

    with open(fname, 'r') as f:
        for line in f:
            fields = line.split()
            try:
                nshares = int(fields[1])
                price = float(fields[2])
            except:
                raise TypeError('couldnt parse')
            total_cost = total_cost + nshares * price

    return total_cost


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: pcost.py filename")
    print(cost2(str(sys.argv[1])))
    print(cost(str(sys.argv[1])))

