# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License

from __future__ import print_function

import os
import random

import numpy as np

WALL_TYPE = np.int8
WALL = 0
EMPTY = 1

class WallNode:
    def __init__(self, x, y, parent = None, height = 0):
        self.x = x
        self.y = y
        self.dx = 0
        self.dy = 0
        self.height = height
        self.parent = parent
        
    def show_node(self): 
      return [self.x, self.y, self.dx, self.dy, self.height]

    def find_child(self, rows, columns, X = False, Y = False, rat = 0):
      """
      TODO: Think about the method of X and Y and return. 
      
      args: 

      rows: the rows of the maze. 
      columns: the columns of the maze. 
      X and Y: whether the wall point of that direction will be generate
      rat: the possibility to change the wall height. 
      
      return: child node. 
      """
      self.dx = random.randint(self.x, columns)
      self.dy = random.randint(self.y, rows)
      #print("dx, dy: ", self.dx, self.dy)
      #print(self.show_node())
      if X != False: 
        n = WallNode(self.x, self.dy, self, self.height)
        if random.random() < rat:
          n.height = random.randint(0, 10)
      if Y != False: 
        m = WallNode (self.dx, self.y, self, self.height)
        if random.random() < rat:
          m.height = random.randint(0, 10)
      return n, m




  
def generate_maze_A (rows=20, columns=20, numOfNodes=20):
    
    """
    TODO: Count is now counting the nodes of the corner. 
    need to be change to the number of total walls. 
    """
    
    maze = list()
    count = 1
      
    x = random.randint(0, columns)
    y = random.randint(0, rows)
      
    node = WallNode(x, y, height = 10)
    maze.append(node)
      
    while count < numOfNodes: 
        child1, child2 = node.find_child(rows, columns, X = True, Y = True, rat = 0.1)
        maze.append(child1)
        maze.append(child2)
        count += 2
        node = child1
        
    
    return maze


