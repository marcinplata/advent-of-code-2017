"""
--- Day 11: Hex Ed ---

Crossing the bridge, you've barely reached the other side of the stream when a program comes up to you, clearly in
distress. "It's my child process," she says, "he's gotten lost in an infinite grid!"

Fortunately for her, you have plenty of experience with infinite grids.

Unfortunately for you, it's a hex grid.

The hexagons ("hexes") in this grid are aligned such that adjacent hexes can be found to the north, northeast,
southeast, south, southwest, and northwest:

  \ n  /
nw +--+ ne
  /    \
-+      +-
  \    /
sw +--+ se
  / s  \

You have the path the child process took. Starting where he started, you need to determine the fewest number of steps
required to reach him. (A "step" means to move from the hex you are in to any adjacent hex.)

For example:

ne,ne,ne is 3 steps away.
ne,ne,sw,sw is 0 steps away (back where you started).
ne,ne,s,s is 2 steps away (se,se).
se,sw,se,sw,sw is 3 steps away (s,s,sw).
"""


def read_file(path):
    with open(path) as file:
        data = file.read()
    data = data[:-1] if data[-1] == "\n" else data
    return data.split(",")


def go_on_hexgrid(moves):
    p = (0, 0)
    for m in moves:
        if m == "s":
            p = (p[0], p[1]-2)
        elif m == "n":
            p = (p[0], p[1]+2)
        elif m == "ne":
            p = (p[0]+1, p[1]+1)
        elif m == "nw":
            p = (p[0]-1, p[1]+1)
        elif m == "se":
            p = (p[0]+1, p[1]-1)
        elif m == "sw":
            p = (p[0]-1, p[1]-1)
        # print(p, find_distance(p))
    return find_distance(p)


def find_distance(p):
    if abs(p[0]) < abs(p[1]):
        # abs(p[0]) + (abs(p[1])-abs(p[0]))//2
        return abs(p[0])//2 + abs(p[1])//2
    else:
        return abs(p[0])


moves = read_file("tests/day_11_test")
print(go_on_hexgrid(moves))


"""
--- Part Two ---

How many steps away is the furthest he ever got from his starting position?
"""


def go_on_hexgrid_with_farthest(moves):
    p = (0, 0)
    farthest = 0
    for m in moves:
        if m == "s":
            p = (p[0], p[1]-2)
        elif m == "n":
            p = (p[0], p[1]+2)
        elif m == "ne":
            p = (p[0]+1, p[1]+1)
        elif m == "nw":
            p = (p[0]-1, p[1]+1)
        elif m == "se":
            p = (p[0]+1, p[1]-1)
        elif m == "sw":
            p = (p[0]-1, p[1]-1)
        # print(p, find_distance(p))
        farthest = find_distance(p) if farthest < find_distance(p) else farthest
    return farthest


print(go_on_hexgrid_with_farthest(moves))

