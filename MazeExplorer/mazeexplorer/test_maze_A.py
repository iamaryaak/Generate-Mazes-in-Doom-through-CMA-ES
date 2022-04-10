# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License

from __future__ import print_function

import os
import random
from maze_gene_A import generate_maze_A, WallNode

import numpy as np

test_maze = generate_maze_A()
#print(test_maze)

for m in test_maze: 
   print(m.show_node())