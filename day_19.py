"""
--- Day 19: A Series of Tubes ---

Somehow, a network packet got lost and ended up here. It's trying to follow a routing diagram (your puzzle input),
but it's confused about where to go.

Its starting point is just off the top of the diagram. Lines (drawn with |, -, and +) show the path it needs to take,
starting by going down onto the only line connected to the top of the diagram. It needs to follow this path until it
reaches the end (located somewhere within the diagram) and stop there.

Sometimes, the lines cross over each other; in these cases, it needs to continue going the same direction,
and only turn left or right when there's no other option. In addition, someone has left letters on the line; these
also don't change its direction, but it can use them to keep track of where it's been. For example:

     |
     |  +--+
     A  |  C
 F---|----E|--+
     |  |  |  D
     +B-+  +--+

Given this diagram, the packet needs to take the following path:

Starting at the only line touching the top of the diagram, it must go down, pass through A, and continue onward to
the first +.

Travel right, up, and right, passing through B in the process.
Continue down (collecting C), right, and up (collecting D).
Finally, go all the way left through E and stopping at F.
Following the path to the end, the letters it sees on its path are ABCDEF.

The little packet looks up at you, hoping you can help it find the way. What letters will it see (in the order it
would see them) if it follows the path? (The routing diagram is very wide; make sure you view it without line
wrapping.)
"""


def read_file(path):
    matrix = []
    with open(path) as file:
        for line in file:
            line = line[:-1] if line[-1] == "\n" else line
            matrix.append([' ']+list(line)+[' '])
    max_len = max([len(l) for l in matrix])
    matrix = [l+([' ']*(max_len-len(l))) for l in matrix]
    matrix.insert(0, [' ']*max_len)
    matrix.append([' ']*max_len)
    return matrix


def find_direction(matrix, pos, d):
    if matrix[pos[0]+1][pos[1]] != ' ' and not (d == (1, 0) or d == (-1, 0)):
        return 1, 0
    elif matrix[pos[0]-1][pos[1]] != ' ' and not (d == (1, 0) or d == (-1, 0)):
        return -1, 0
    elif matrix[pos[0]][pos[1]+1] != ' ' and not (d == (0, 1) or d == (0, -1)):
        return 0, 1
    elif matrix[pos[0]][pos[1]-1] != ' ' and not (d == (0, 1) or d == (0, -1)):
        return 0, -1


def go(matrix):
    alpha, packet = "", 0
    i, j = 1, matrix[1].index('|')
    # down - (1,0), up - (-1,0), left - (0,-1), right - (0,1)
    di, dj = (1, 0)
    while True:
        if matrix[i][j] == ' ':
            break
        elif matrix[i][j] == '+':
            di, dj = find_direction(matrix, (i, j), (di, dj))
            i, j = i + di, j + dj
        elif matrix[i][j] == '|':
            if dj == 0:
                i, j = i + di, j
            else:
                i, j = i, j + dj
        elif matrix[i][j] == '-':
            if di == 0:
                i, j = i, j + dj
            else:
                i, j = i + di, j
        elif matrix[i][j].isalpha():
            alpha += matrix[i][j]
            i, j = i + di, j + dj
        packet += 1
    return alpha, packet


matrix = read_file("tests/day_19_test")
print(go(matrix)[0])

"""
--- Part Two ---
The packet is curious how many steps it needs to go.

For example, using the same routing diagram from the example above...

     |          
     |  +--+    
     A  |  C    
 F---|--|-E---+ 
     |  |  |  D 
     +B-+  +--+ 

...the packet would go:

6 steps down (including the first line at the top of the diagram).
3 steps right.
4 steps up.
3 steps right.
4 steps down.
3 steps right.
2 steps up.
13 steps left (including the F it stops on).
This would result in a total of 38 steps.

How many steps does the packet need to go?
"""

print(go(matrix)[1])

