"""
--- Day 23: Coprocessor Conflagration ---
You decide to head directly to the CPU and fix the printer from there. As you get close, you find an experimental
coprocessor doing so much work that the local programs are afraid it will halt and catch fire. This would cause
serious issues for the rest of the computer, so you head in and see what you can do.

The code it's running seems to be a variant of the kind you saw recently on that tablet. The general functionality
seems very similar, but some of the instructions are different:

set X Y sets register X to the value of Y.
sub X Y decreases register X by the value of Y.
mul X Y sets register X to the result of multiplying the value contained in register X by the value of Y.
jnz X Y jumps with an offset of the value of Y, but only if the value of X is not zero. (An offset of 2 skips the
next instruction, an offset of -1 jumps to the previous instruction, and so on.)
Only the instructions listed above are used. The eight registers here, named a through h, all start at 0.

The coprocessor is currently set to some kind of debug mode, which allows for testing, but prevents it from doing any
meaningful work.

If you run the program (your puzzle input), how many times is the mul instruction invoked?
"""

import numpy as np


def read_file(path):
    instructions = []
    with open(path) as file:
        for line in file:
            line = line[:-1] if line[-1] == "\n" else line
            line = line.split(" ")
            line = line if len(line) == 3 else line + ["_"]
            instructions.append(line)
    return np.array(instructions)


def run_instructions(instructions):
    n = {n: int(n) for n in list(instructions[:, 1]) + list(instructions[:, 2]) if n.lstrip("-").isdigit()}
    r = {n: 0 for n in list(instructions[:, 1]) + list(instructions[:, 2]) if not n.lstrip("-").isdigit()}
    registers = {**n, **r}
    pos = 0
    count = 0
    while pos < len(instructions):
        i, r, v = instructions[pos]
        if i == 'set':
            registers[r] = registers[v]
        elif i == 'sub':
            registers[r] = registers[r] - registers[v]
        elif i == 'mul':
            registers[r] = registers[r] * registers[v]
            count += 1
        elif i == "jnz" and registers[r] != 0:
            pos = pos + registers[v] - 1
        pos += 1
    return count


insts = read_file("tests/day_23_test")
print(run_instructions(insts))

"""
--- Part Two ---
Now, it's time to fix the problem.

The debug mode switch is wired directly to register a. You flip the switch, which makes register a now start at 1 
when the program is executed. 

Immediately, the coprocessor begins to overheat. Whoever wrote this program obviously didn't choose a very efficient 
implementation. You'll need to optimize the program if it has any hope of completing before Santa needs that printer 
working. 

The coprocessor's ultimate goal is to determine the final value left in register h once the program completes. 
Technically, if it had that... it wouldn't even need to run the program. 

After setting register a to 1, if the program were to run to completion, what value would be left in register h?
"""


# assembly interpretation and optimization by CharlieYJH (https://www.reddit.com/user/CharlieYJH)
def interpreted_assembly(input):
    multiplier = 100
    b_adder = 100000
    c_adder = 17000

    b = input * multiplier + b_adder
    c = b + c_adder
    h = 0

    while b <= c:
        d = 2
        while d != b:
            if b % d == 0:
                h += 1
                break
            d += 1
        b += 17
    return h


print(interpreted_assembly(84))
