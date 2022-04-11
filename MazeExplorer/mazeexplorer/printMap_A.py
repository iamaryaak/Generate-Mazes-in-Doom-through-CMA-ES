# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License

from __future__ import print_function

import os
import random
from maze_gene_A import generate_maze_A, WallNode, rec_maze_A

import numpy as np


def getMap(maze, rows, columns): 
    mapRes = np.zeros((rows, columns))
    
    #[x, y, dx, dy, height]
    
    for m in maze: 
        m = m.show_node()
        print(m)
        mapRes[m[1]][m[0]] = 1
        if m[2] >= 0: 
            wallR = sorted([m[0], m[2]])
            start = wallR[0]
            while start != wallR[1]:
                mapRes[m[1]][start] = 1
                start += 1
                
        if m[3] >= 0: 
            wallC = sorted([m[1], m[3]])
            start = wallC[0]
            while start != wallC[1]:
                mapRes[start][m[0]] = 1
                start += 1
    #print(mapRes)
    return mapRes
            

def printMap (mapG): 
    mapG.tolist()
    for lst in mapG: 
        lst = ['X' if i == 1 else i for i in lst]
        lst = ['_' if i == 0 else i for i in lst]
        stg = ' '.join(map(str,lst))
        print('[', stg, ']')
    #print(mapG)
    return 
        