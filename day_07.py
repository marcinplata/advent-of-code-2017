"""

--- Day 7: Recursive Circus ---

Wandering further through the circuits of the computer, you come upon a tower of programs that have gotten themselves
into a bit of trouble. A recursive algorithm has gotten out of hand, and now they're balanced precariously in a large
tower.

One program at the bottom supports the entire tower. It's holding a large disc, and on the disc are balanced several
more sub-towers. At the bottom of these sub-towers, standing on the bottom disc, are other programs, each holding
their own disc, and so on. At the very tops of these sub-sub-sub-...-towers, many programs stand simply keeping the
disc below them balanced but with no disc of their own.

You offer to help, but first you need to understand the structure of these towers. You ask each program to yell out
their name, their weight, and (if they're holding a disc) the names of the programs immediately above them balancing
on that disc. You write this information down (your puzzle input). Unfortunately, in their panic, they don't do this
in an orderly fashion; by the time you're done, you're not sure which program gave which information.

For example, if your list is the following:

pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)
...then you would be able to recreate the structure of the towers that looks like this:

                gyxo
              /
         ugml - ebii
       /      \
      |         jptl
      |
      |         pbga
     /        /
tknk --- padx - havc
     \        \
      |         qoyq
      |
      |         ktlj
       \      /
         fwft - cntj
              \
                xhth

In this example, tknk is at the bottom of the tower (the bottom program), and is holding up ugml, padx,
and fwft. Those programs are, in turn, holding up other programs; in this example, none of those programs are holding
up any other programs, and are all the tops of their own towers. (The actual tower balancing in front of you is much
larger.)

Before you're ready to help them, you need to make sure your information is correct. What is the name of the bottom
program?

"""


class Program:
    weight = 0
    name = ""
    parent = None
    children = []
    sum_of_weights = -1

    def __init__(self, name, weight):
        self.name = name
        self.weight = int(weight)
        self.parent = None
        self.children = []
        self.sum_of_weights = -1

    def add_parent(self, parent):
        self.parent = parent

    def add_child(self, child):
        self.children.append(child)

    def print(self):
        print(self.name, end=" ")
        print(self.weight, end=" ")
        if self.parent:
            print(self.parent.name, end=" ")
        else:
            print("I AM THE BOTTOM!", end=" ")
        print([c.name for c in self.children])


def read_file(path):
    rows = []
    with open(path) as file:
        for line in file:
            line = line[:-1] if line[-1] == "\n" else line
            rows.append(line.replace(" ", ""))
    top, bottom = [], []
    for i in range(len(rows)):
        x = rows[i].split("->")
        l = x[0].split("(")
        if len(x) == 1:
            top.append((l[0], l[1][:-1]))
        else:
            r = x[1].split(",")
            bottom.append(((l[0], l[1][:-1]), r))
    return top, bottom


def create_structure(top, bottom):
    elems = {}
    for t in top:
        elems[t[0]] = Program(*t)
    for b in bottom:
        elems[b[0][0]] = Program(*b[0])

    for b in bottom:
        s = elems[b[0][0]]
        for c in b[1]:
            child = elems[c]
            s.add_child(child)
            child.add_parent(s)
    return elems


def find_bottom(elems):
    for e in elems.keys():
        if not elems[e].parent:
            return elems[e]


t, b = read_file("tests/day_07_test")
elems = create_structure(t, b)
bottom = find_bottom(elems)
print(bottom.name)

"""
--- Part Two ---

The programs explain the situation: they can't get down. Rather, they could get down, if they weren't expending all 
of their energy trying to keep the tower balanced. Apparently, one program has the wrong weight, and until it's 
fixed, they're stuck here. 

For any program holding a disc, each program standing on that disc forms a sub-tower. Each of those sub-towers are 
supposed to be the same weight, or the disc itself isn't balanced. The weight of a tower is the sum of the weights of 
the programs in that tower. 

In the example above, this means that for ugml's disc to be balanced, gyxo, ebii, and jptl must all have the same 
weight, and they do: 61. 

However, for tknk to be balanced, each of the programs standing on its disc and all programs above it must each 
match. This means that the following sums must all be the same: 

ugml + (gyxo + ebii + jptl) = 68 + (61 + 61 + 61) = 251
padx + (pbga + havc + qoyq) = 45 + (66 + 66 + 66) = 243
fwft + (ktlj + cntj + xhth) = 72 + (57 + 57 + 57) = 243

As you can see, tknk's disc is unbalanced: ugml's stack is heavier than the other two. Even though the nodes above 
ugml are balanced, ugml itself is too heavy: it needs to be 8 units lighter for its stack to weigh 243 and keep the 
towers balanced. If this change were made, its weight would be 60. 

Given that exactly one program is the wrong weight, what would its weight need to be to balance the entire tower?
"""
from collections import Counter


def calc_sum_of_weights(bottom: Program):
    bottom.sum_of_weights = bottom.weight
    if not bottom.children:
        return bottom.sum_of_weights
    else:
        for child in bottom.children:
            bottom.sum_of_weights += calc_sum_of_weights(child)
        return bottom.sum_of_weights


def find_unbalanced(bottom, difference=0):
    weights = [c.sum_of_weights for c in bottom.children]
    common = Counter(weights).most_common()
    # if children are balanced - len(common)== 1 or no children - len(common)==0
    if len(common) < 2:
        # print("1) unbalanced node:", bottom.name, bottom.weight, difference, bottom.weight+difference)
        return bottom.weight + difference
    else:
        i = weights.index(common[-1][0])
        return find_unbalanced(bottom.children[i], common[0][0] - common[-1][0])


calc_sum_of_weights(bottom)
print(find_unbalanced(bottom))
