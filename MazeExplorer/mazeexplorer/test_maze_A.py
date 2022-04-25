# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License

from __future__ import print_function

import os
import random
from maze_gene_A import generate_maze_A, WallNode, rec_maze_A, original_node
from printMap_A import printMap, getMap

import numpy as np

# test_maze = generate_maze_A()
#print(test_maze)

# for m in test_maze: 
#     print(m.show_node())

node = original_node(20, 20)
maze = list()
rec_maze_A(node, maze)
#print(test_rec_maze)

##
# for m in test_maze: 
#     print(m.show_node())

#print('maze', maze)
mp = getMap(maze, 21, 21)
printMap(mp)