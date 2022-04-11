# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License

from __future__ import print_function

import os
import random

import numpy as np

WALL_TYPE = np.int8
WALL = 0
EMPTY = 1

"""
TODOs: 
    1. Direction of each corner: X and Y, which way to go? how much ways to go? 
    2. make the 
"""

class WallNode:
    def __init__(self, x, y, parent = None, height = 1):
        self.x = x
        self.y = y
        self.dx = -1
        self.dy = -1
        self.height = height
        self.parent = parent
        
    def show_node(self): 
      return [self.x, self.y, self.dx, self.dy, self.height]

    def find_child(self, rows, columns, X = False, Y = False, rat = 0):
        """
          TODO:
              1. Think about the method of X and Y and return.
              2. Let the method able to go upward or downward. 
          
          args: 
    
          rows: the rows of the maze. 
          columns: the columns of the maze. 
          X and Y: whether the wall point of that direction will be generate
          rat: the possibility to change the height of the wall. 
          
          return: child node. 
        """
        n, m = None, None
        #print("Which one to generate? ", X, Y)
        if X: 
            self.dy = random.randint(0, rows)
            #yp = min(self.y+self.dy, rows)
            n = WallNode(self.x, self.dy, self, self.height)
            if random.random() < rat:
                n.height = random.randint(0, 10)
            #print("Child Node X: ", n.show_node())
            
        if Y: 
            self.dx = random.randint(0, columns)
            #xp = min(self.x+self.dx, columns)
            m = WallNode (self.dx, self.y, self, self.height)
            if random.random() < rat:
                m.height = random.randint(0, 10)
            #print("Child Node Y: ", m.show_node())
        
        #print("dx, dy: ", self.dx, self.dy)
        #print("Parent Node: ", self.show_node())
        #print("Child Nodes: ", n.show_node(), m.show_node())
        
        
        return [n, m]
  
    def rec_generator(self, maze, rows, columns, X = False, Y = False, rat = 0):
        """
        TODO: Try recursive function. 
        """
        return 


def original_node(rows = 0, columns = 0, h = 1):
    x = random.randint(0, columns)
    y = random.randint(0, rows)
    
    return WallNode(x, y, None, h)
        

  
def generate_maze_A (rows=20, columns=20, numOfNodes=20):
    
    """
    TODO: 
        1. Count is now counting the nodes of the corner. 
            need to be change to the number of total walls. 
        2. Last point should be the original node, 
            or last two points should be connected. 
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




def rec_maze_A(node, maze,  rows=20, columns=20, numOfNodes=20, prob = 0.5): 
    child1, child2 = None, None
    
    #Start of the process. 
    if node == None: 
        #node = original_node(rows, columns)
        #node = WallNode(0, 0)
        return
    
    maze.append(node)
    #print(maze)
    
    #print(node.show_node())
    #End of the process
    if len(maze) > numOfNodes:
        return 
    
    if random.random() < prob: 
        child1 = node.find_child(rows, columns, X = True, rat = 0.1)[0]
        print("         Child1 generated!!!")
        rec_maze_A(child1, maze, rows, columns, numOfNodes)
       
    if random.random() < prob: 
        child2 = node.find_child(rows, columns, Y = True, rat = 0.1)[1]
        print("         Child2 generated!!!")
        rec_maze_A(child2, maze, rows, columns, numOfNodes)
        
        
    #child1, child2 = node.find_child(rows, columns, X = True, Y = True, rat = 0.1)
    
    ##PROBLEM: Only returns child1 result. 
    #return rec_maze_A(child1, maze, rows, columns, numOfNodes) and rec_maze_A(child2, maze, rows, columns, numOfNodes)
    ##OR
    # if child1 and child2: 
    #     return rec_maze_A(child1, maze, rows, columns, numOfNodes) and rec_maze_A(child2, maze, rows, columns, numOfNodes)
    # else: 
    #     return rec_maze_A(child1, maze, rows, columns, numOfNodes) or rec_maze_A(child2, maze, rows, columns, numOfNodes)
    ##OR
    # if child1 != [None]: 
    #     rec_maze_A(child1, maze, rows, columns, numOfNodes)
    # if child2 != [None]: 
    #     rec_maze_A(child2, maze, rows, columns, numOfNodes)
