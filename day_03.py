"""
--- Day 3: Spiral Memory ---

You come across an experimental new kind of memory stored on an infinite two-dimensional grid.

Each square on the grid is allocated in a spiral pattern starting at a location marked 1 and then counting up while
spiraling outward. For example, the first few squares are allocated like this:

17  16  15  14  13
18   5   4   3  12
19   6   1   2  11
20   7   8   9  10
21  22  23---> ...

While this is very space-efficient (no squares are skipped), requested data must be carried back to square 1 (the
location of the only access port for this memory system) by programs that can only move up, down, left,
or right. They always take the shortest path: the Manhattan Distance between the location of the data and square 1.

For example:

Data from square 1 is carried 0 steps, since it's at the access port.
Data from square 12 is carried 3 steps, such as: down, left, left.
Data from square 23 is carried only 2 steps: up twice.
Data from square 1024 must be carried 31 steps.

How many steps are required to carry the data from the square identified in your puzzle input all the way to the
access port?
"""


def distance(x):
    s = 1
    i = 0
    # find s which is in a right-down corner (1 -> 9 -> 25 -> 49 -> ...)
    while x > s:
        i = i + 1
        s = s + 8*i
    # print(s, i)
    m = 3 + 2*(i-1)
    # print(m)
    # find points on a correct layer (circle) which are the closest to 1 (eg. for 2th layer - 23, 19, 15, 11)
    # +1, +2, +3 for west, north, east because we subtract corner points more that once
    south = s - m//2
    west = s - m - m//2 + 1
    north = s - 2*m - m // 2 + 2
    east = s - 3*m - m // 2 + 3
    # print(south, west, north, east)
    j = min([abs(j-x) for j in [south, west, north, east]])
    # print(i, j)
    return i+j


print(distance(265149))


"""
--- Part Two ---

As a stress test on the system, the programs here clear the grid and then store the value 1 in square 1. Then, 
in the same allocation order as shown above, they store the sum of the values in all adjacent squares, 
including diagonals. 

So, the first few squares' values are chosen as follows:

Square 1 starts with the value 1.
Square 2 has only one adjacent filled square (with value 1), so it also stores 1.
Square 3 has both of the above squares as neighbors and stores the sum of their values, 2.
Square 4 has all three of the aforementioned squares as neighbors and stores the sum of their values, 4.
Square 5 only has the first and fourth squares as neighbors, so it gets the value 5.
Once a square is written, its value does not change. Therefore, the first few squares would receive the following values

147  142  133  122   59
304    5    4    2   57
330   10    1    1   54
351   11   23   25   26
362  747  806--->   ...

What is the first value written that is larger than your puzzle input?
"""


def sum_neigh(pos, spiral):
    ox, oy = pos
    points = [(x, y) for x in range(ox-1, ox+2) for y in range(oy-1, oy+2) if not (x == ox and y == oy)]
    sum = 0
    for p in points:
        if p in spiral.keys():
            sum = sum + spiral[p]
    return sum


def spiral(x):
    spiral = {(0, 0): 1}
    actual_pos = [0, 0]

    # 0 - right, 1 - up, 2 - left, 3 - down
    direction = 0
    actual_one_way_moves = 1

    one_way_iterator = 2
    one_way_moves = 1

    while spiral[tuple(actual_pos)] <= x:
        if direction == 0:
            actual_pos[0] = actual_pos[0] + 1
        elif direction == 1:
            actual_pos[1] = actual_pos[1] + 1
        elif direction == 2:
            actual_pos[0] = actual_pos[0] - 1
        elif direction == 3:
            actual_pos[1] = actual_pos[1] - 1

        tup_actual_pos = tuple(actual_pos)
        spiral[tup_actual_pos] = sum_neigh(tup_actual_pos, spiral)
        # print(actual_pos, spiral[tup_actual_pos])

        one_way_moves = one_way_moves - 1
        if one_way_moves == 0:
            direction = (direction + 1) % 4
            one_way_iterator = one_way_iterator - 1
            one_way_moves = actual_one_way_moves
        if one_way_iterator == 0:
            one_way_iterator = 2
            actual_one_way_moves = actual_one_way_moves + 1
            one_way_moves = actual_one_way_moves

    return spiral[tup_actual_pos]


print(spiral(265149))