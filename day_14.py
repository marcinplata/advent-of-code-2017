"""
--- Day 14: Disk Defragmentation ---

Suddenly, a scheduled job activates the system's disk defragmenter. Were the situation different, you might sit and
watch it for a while, but today, you just don't have that kind of time. It's soaking up valuable system resources
that are needed elsewhere, and so the only option is to help it finish its task as soon as possible.

The disk in question consists of a 128x128 grid; each square of the grid is either free or used. On this disk,
the state of the grid is tracked by the bits in a sequence of knot hashes.

A total of 128 knot hashes are calculated, each corresponding to a single row in the grid; each hash contains 128
bits which correspond to individual grid squares. Each bit of a hash indicates whether that square is free (0) or
used (1).

The hash inputs are a key string (your puzzle input), a dash, and a number from 0 to 127 corresponding to the row.
For example, if your key string were flqrgnkx, then the first row would be given by the bits of the knot hash of
flqrgnkx-0, the second row from the bits of the knot hash of flqrgnkx-1, and so on until the last row, flqrgnkx-127.

The output of a knot hash is traditionally represented by 32 hexadecimal digits; each of these digits correspond to 4
bits, for a total of 4 * 32 = 128 bits. To convert to bits, turn each hexadecimal digit to its equivalent binary
value, high-bit first: 0 becomes 0000, 1 becomes 0001, e becomes 1110, f becomes 1111, and so on; a hash that begins
with a0c2017... in hexadecimal would begin with 10100000110000100000000101110000... in binary.

Continuing this process, the first 8 rows and columns for key flqrgnkx appear as follows, using # to denote used
squares, and . to denote free ones:

##.#.#..-->
.#.#.#.#
....#.#.
#.#.##.#
.##.#...
##..#..#
.#...#..
##.#.##.-->
|      |
V      V
In this example, 8108 squares are used across the entire 128x128 grid.

Given your actual key string, how many squares are used?
"""
from functools import reduce


def make_hash(numbers, moves, actual_pos=0, skip_size=0):
    n = len(numbers)
    for m in moves:
        # swap first and last and so on
        for j, k in enumerate(range(actual_pos, actual_pos+(m//2))):
            numbers[k % n], numbers[(k+(m-1-2*j)) % n] = numbers[(k+(m-1-2*j)) % n], numbers[k % n]
        actual_pos += (m + skip_size) % n
        skip_size += 1
    return numbers, actual_pos, skip_size


def reduce_numbers(numbers):
    numbers = [numbers[16*i:16*i+16] for i in range(16)]
    numbers = [("%0.2x" % reduce(lambda x, y: x ^ y, n)) for n in numbers]
    return "".join(numbers)


def run_hashing_loop(string):
    # to ascii + add tail
    ascii = [ord(c) for c in string] + [17, 31, 73, 47, 23]
    numbers = list(range(0, 256))
    actual_pos, skip_size = 0, 0
    for _ in range(0, 64):
        numbers, actual_pos, skip_size = make_hash(numbers, ascii, actual_pos, skip_size)
    return reduce_numbers(numbers)


def get_defragmentation_info(string):
    ones = 0
    for s in [run_hashing_loop(string+"-"+str(i)) for i in range(128)]:
        binary = bin(int(s, 16))[2:]    # .zfill(128)
        ones += sum(map(int, binary))
    return ones


print(get_defragmentation_info("stpzcrnm"))

"""
--- Part Two ---

Now, all the defragmenter needs to know is the number of regions. A region is a group of used squares that are all 
adjacent, not including diagonals. Every used square is in exactly one region: lone used squares form their own 
isolated regions, while several adjacent squares all count as a single region. 

In the example above, the following nine regions are visible, each marked with a distinct digit:

11.2.3..-->
.1.2.3.4   
....5.6.   
7.8.55.9   
.88.5...   
88..5..8   
.8...8..   
88.8.88.-->
|      |   
V      V   

Of particular interest is the region marked 8; while it does not appear contiguous in this small view, all of the 
squares marked 8 are connected when considering the whole 128x128 grid. In total, in this example, 1242 regions are 
present. 

How many regions are present given your key string?
"""


def mark_regions(string):
    ones = {}
    for i, s in enumerate([run_hashing_loop(string+"-"+str(i)) for i in range(128)]):
        for j, b in enumerate(list(map(int, bin(int(s, 16))[2:].zfill(128)))):
            if b == 1:
                ones[(i, j)] = b

    group_count = 0
    while ones.keys():
        group_count += 1
        group = [list(ones.keys())[0]]
        ones.pop(group[0])
        while group:
            x, y = group.pop(0)
            if (x-1, y) in ones.keys():
                group.append((x-1, y))
                ones.pop((x-1, y))
            if (x+1, y) in ones.keys():
                group.append((x+1, y))
                ones.pop((x+1, y))
            if (x, y-1) in ones.keys():
                group.append((x, y-1))
                ones.pop((x, y-1))
            if (x, y+1) in ones.keys():
                group.append((x, y+1))
                ones.pop((x, y+1))
    return group_count


print(mark_regions("stpzcrnm"))
