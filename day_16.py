"""
--- Day 16: Permutation Promenade ---

You come upon a very unusual sight; a group of programs here appear to be dancing.

There are sixteen programs in total, named a through p. They start by standing in a line: a stands in position 0,
b stands in position 1, and so on until p, which stands in position 15.

The programs' dance consists of a sequence of dance moves:

Spin, written sX, makes X programs move from the end to the front, but maintain their order otherwise. (For example,
s3 on abcde produces cdeab).
Exchange, written xA/B, makes the programs at positions A and B swap places.
Partner, written pA/B, makes the programs named A and B swap places.
For example, with only five programs standing in a line (abcde), they could do the following dance:

s1, a spin of size 1: eabcd.
x3/4, swapping the last two programs: eabdc.
pe/b, swapping programs e and b: baedc.
After finishing their dance, the programs end up in order baedc.

You watch the dance for a while and record their dance moves (your puzzle input). In what order are the programs
standing after their dance?
"""


def read_file(path):
    with open(path) as file:
        line = file.read()
        line = line[:-1] if line[-1] == "\n" else line
    return [(m[0], m[1:].split("/")) for m in line.split(",")]


def move(moves, programs='abcdefghijklmnop'):
    programs = list(programs)
    for t, a in moves:
        if t == 's':
            programs = programs[-int(a[0]):] + programs[:-int(a[0])]
        elif t == 'x':
            programs[int(a[0])], programs[int(a[1])] = programs[int(a[1])], programs[int(a[0])]
        elif t == 'p':
            f = programs.index(a[0])
            s = programs.index(a[1])
            programs[f], programs[s] = a[1], a[0]
    return "".join(programs)


moves = read_file("tests/day_16_test")
print(move(moves))

"""
--- Part Two ---

Now that you're starting to get a feel for the dance moves, you turn your attention to the dance as a whole.

Keeping the positions they ended up in from their previous dance, the programs perform it again and again: including 
the first dance, a total of one billion (1000000000) times. 

In the example above, their second dance would begin with the order baedc, and use the same dance moves:

s1, a spin of size 1: cbaed.
x3/4, swapping the last two programs: cbade.
pe/b, swapping programs e and b: ceadb.
In what order are the programs standing after their billion dances?
"""


def run_1000000000(moves):
    programs = 'abcdefghijklmnop'
    occured = ['abcdefghijklmnop']
    for i in range(1000000000):
        programs = move(moves, programs)
        occured.append(programs)
        if programs == 'abcdefghijklmnop':
            return occured[1000000000 % (i+1)]
    return occured[-1]


print(run_1000000000(moves))

