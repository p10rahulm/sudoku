import time
import sys

numobjects = 0
from operator import ior
from functools import reduce
from collections import defaultdict

def kthbitofn(n, k):
    return (n & (1 << k)) >> k


def twopowers(x):
    powers = []
    i = 1
    while i <= x:
        if i & x:
            powers.append(i)
        i <<= 1
    return powers


def whichtwopower(x):
    count = 0
    while x > 0:
        x >>= 1
        count += 1
    return count - 1


def is_power2(num):
    # states if a number is a power of two
    return ((num & (num - 1)) == 0) and num != 0


def cross(A, B):
    # "Cross product of elements in A and elements in B."
    return [a + b for a in A for b in B]


digits = '123456789'
bindigits = 511
rows = 'ABCDEFGHI'
cols = digits
squares = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
units = dict((s, [u for u in unitlist if s in u]) for s in squares)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in squares)
twopowerslist = dict((s,twopowers(s)) for s in range(512))
# len of binary using table lookup O(1)
onestable = [bin(i)[2:].count('1') for i in range(512)]
twopowerplusone = [whichtwopower(i) + 1 for i in range(512)]
chartodigit = dict((digits[i], i + 1) for i in range(len(digits)))
twopowernum = dict((digits[i], 2**i) for i in range(len(digits)))

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, bindigits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, twopowernum[d]):
            return False  ## (Fail if we can't assign d to square s.)
    return values


def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 81
    return dict(zip(squares, chars))


def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    # if is_power2(values[s]) and values[s] != d:        print("ok");        return False
    other_values = values[s] & (511 - d)
    if eliminate(values, s, other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d & values[s] == 0:
        return values # Already eliminated
    values[s] &= 511 - d  # .replace(d,'')
    # (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if onestable[values[s]] <= 0:
        return False  ## Contradiction: removed last value
    elif onestable[values[s]] == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            # print("returned false at eliminate peers")
            return False

   # (2) If a unit u is reduced to only one place for a value d, then put it there.
   #  for u in units[s]:
   #      seensofar =0
   #      seensofarlessrepeats =0
   #      repeatedtwiceormore =0
   #      repeatedexactlyoncethistime =0
   #      numsexactlyonce =0
   #      bininitnum =0
   #      binrepeattwice =0
   #      firsttimedigseen =0
   #      num2dict = defaultdict(list)
   #      for s in range(len(u)):
   #          seensofarlessrepeats  = seensofar^values[u[s]]
   #          seensofar |= values[u[s]]
   #          repeatedtwiceormore = seensofar - seensofarlessrepeats
   #          repeatedexactlyoncethistime |=repeatedtwiceormore
   #          numsexactlyonce = seensofar-repeatedexactlyoncethistime
   #
   #          bininitnum = int(bin(values[u[s]])[2:])
   #          binrepeattwice = int(bin(repeatedtwiceormore)[2:])
   #
   #          firsttimedigseen += s*(bininitnum - binrepeattwice)
   #          num2dict[values[u[s]]].append(u[s])
   #      if seensofar != 511: return False
   #
   #
   #
   #
   #
   #
   #      unitlist = [values[s] for s in u]
   #      if onestable[reduce(ior, unitlist)] < 9:
   #          return False
   #      # get dth bit in unitlist
   #      for tupower in twopowers(d):
   #          dplaces = [s for s in u if tupower & values[s] != 0]
   #          if len(dplaces) == 1:
   #              # d can only be in one place in unit; assign it there
   #              if not assign(values, dplaces[0], tupower):
   #                  return False
   #  return values

    # iter4
    # # (2) If a unit u is reduced to only one place for a value d, then put it there.
    # for u in units[s]:
    #     unitlist = [values[s] for s in u]
    #     if onestable[reduce(ior, unitlist)] < 9:
    #         return False
    #     # get dth bit in unitlist
    #     for tupower in twopowers(d):
    #         dplaces = [s for s in u if tupower & values[s] != 0]
    #         if len(dplaces) == 1:
    #             # d can only be in one place in unit; assign it there
    #             if not assign(values, dplaces[0], tupower):
    #                 return False
    # return values

    #     sumdthbit = 0
    #     last1bit = -1
    #     for index,unit in enumerate(unitlist):
    #         kbn = kthbitofn(unit,d)
    #         sumdthbit += kbn
    #         if sumdthbit >1: break
    #         if kbn ==1: last1bit = index
    #     if sumdthbit == 1:
    #         if not assign(values, u[last1bit], d):
    #             print("returning false on assignment. u[last1bit]",u[last1bit],"values[u[last1bit]] = ",values[u[last1bit]],"d = ",d)
    #             return False
    # return values


    # iter 2 (slower thn iter 1
    # for u in units[s]:
    #     dplaces = [(tupower,[s for s in u if tupower & values[s] != 0]) for tupower in twopowers(d)]
    #     if any(len(place[1]) == 0 for place in dplaces):
    #         return False ## Contradiction: no place for this value
    #     if not all(assign(values, place[1][0], place[0]) for place in dplaces if len(place[1]) ==1):
    #         # d can only be in one place in unit; assign it there
    #             return False
    # return values

    # # iter 3
    # for u in units[s]:
    #     dplaces = [s for s in u if d & values[s] != 0]
    #     if len(dplaces) == 0: return False  ## Contradiction: no place for this value
    #     for tupower in twopowers(d):
    #         dplaces = [s for s in u if tupower & values[s] != 0]
    #         # dplaces = [[(s,tupower) for s in u if tupower & values[s] != 0] for tupower in twopowers(d)]
    #         if len(dplaces) == 1:
    #             # d can only be in one place in unit; assign it there
    #             if not is_power2(values[dplaces[0]]):
    #                 if not assign(values, dplaces[0], tupower):
    #                     return False
    # return values

    # iter 2
    for tupower in twopowerslist[d]:
        for u in units[s]:
            dplaces = [s for s in u if tupower & values[s] != 0]
            # dplaces = [[(s,tupower) for s in u if tupower & values[s] != 0] for tupower in twopowers(d)]
            if len(dplaces) == 0:
                return False  ## Contradiction: no place for this value
            elif len(dplaces) == 1:
                # d can only be in one place in unit; assign it there
                if not is_power2(values[dplaces[0]]):
                    if not assign(values, dplaces[0], tupower):
                        return False
    return values

    # # iter 1
    # for tupower in twopowers(d):
    #     for u in units[s]:
    #         dplaces = [s for s in u if tupower & values[s] != 0]
    #         # dplaces = [[(s,tupower) for s in u if tupower & values[s] != 0] for tupower in twopowers(d)]
    #         if len(dplaces) == 0:
    #             return False  ## Contradiction: no place for this value
    #         elif len(dplaces) == 1:
    #             # d can only be in one place in unit; assign it there
    #             if not assign(values, dplaces[0], tupower):
    #                 return False
    # return values


def solve(grid):
    return parsedict2val(search(parse_grid(grid)))


def parsedict2val(input_dict):
    if not input_dict: return input_dict
    for i in input_dict:
        input_dict[i] = str(twopowerplusone[input_dict[i]])
    return input_dict


def search(values):
    global numobjects
    "Using depth-first search and propagation, try all possible values."
    if values is False:
        return False  ## Failed earlier
    if all(is_power2(values[s]) == 1 for s in squares):
        return values  ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n, s = min((onestable[values[s]], s) for s in squares if not is_power2(values[s]))
    numobjects += 1
    return some(search(assign(values.copy(), s, d))
                for d in twopowerslist[values[s]])


def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False


######################################################
# PRETTY DISPLAY FROM NORVIG
######################################################


def display(values):
    "Display these values as a 2-D grid."
    width = 1 + max(len(values[s]) for s in squares)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print([''.join(values[r + c].center(width) + ('|' if c in '36' else '')) for c in cols])
        if r in 'CF': print(line)
    print()


######################################################
# SOME BINDERS
######################################################
def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""

    def time_solve(grid):
        start = time.clock()
        values = solve(grid)
        t = time.clock() - start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print('(%.2f seconds)\n' % t)
        return (t, solved(values))

    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print("Solved %d of %d %s puzzles (avg %.3f secs (%d Hz), max %.3f secs)." % (
            sum(results), N, name, sum(times) / N, N / sum(times), max(times)))


def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."

    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)

    return values is not False and all(unitsolved(unit) for unit in unitlist)


def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    return open(filename).read().strip().split(sep)


######################################################
# GENERATE PUZZLES
######################################################
import random


def random_puzzle(N=17):
    """Make a random puzzle with N or more assignments. Restart on contradictions.
    Note the resulting puzzle is not guaranteed to be solvable, but empirically
    about 99.8% of them are solvable. Some have multiple solutions."""
    values = dict((s, bindigits) for s in squares)
    for s in shuffled(squares):
        if not assign(values, s, random.choice(twopowerslist[values[s]])):
            break
        ds = [values[s] for s in squares if is_power2(values[s])]
        if len(ds) >= N and len(set(ds)) >= 8:
            return ''.join(str(twopowerplusone[values[s]]) if is_power2(values[s]) else '.' for s in squares)
    return random_puzzle(N)  ## Give up and make a new puzzle


def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq


if __name__ == "__main__":
    starttiem = time.time()
    input_string = '48.3............71.2.......7.5....6....2..8.............1.76...3.....4......5....'
    for i in range(1):
        display(solve(input_string))
    print("timetaken = ", time.time() - starttiem)
    print("num objects created = ", numobjects)
    solve_all(from_file("data/toughsudokupuzzles.txt"), "hardest", 1)
    solve_all([random_puzzle() for _ in range(99)], "random", 100.0)
    print("tot obj = ", numobjects)
