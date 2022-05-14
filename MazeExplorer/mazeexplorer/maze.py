# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License

from __future__ import print_function

import os
import random

import numpy as np

WALL_TYPE = np.int8
WALL = 0
EMPTY = 1


class Maze:
    def __init__(self, rows, columns):
        if rows < 1 or columns < 1:
            raise ValueError("Invalid number rows or columns, must be greater than 1.")

        self.nrows = rows
        self.ncolumns = columns
        self.board = np.zeros((rows, columns), dtype=WALL_TYPE)
        self.board.fill(EMPTY)

    def __str__(self):
        return os.linesep.join(''.join('X' if self.is_wall(i, j) else ' '
                                       for j in range(self.ncolumns))
                               for i in range(self.nrows))

    def __hash__(self):
        return hash(self.board.tostring())

    def __eq__(self, other):
        return np.array_equal(self.board, other.board)

    def set_borders(self):
        self.board[0, :] = self.board[-1, :] = WALL
        self.board[:, 0] = self.board[:, -1] = WALL

    def is_wall(self, x, y):
        assert self.in_maze(x, y)
        return self.board[x][y] == WALL

    def set_wall(self, x, y):
        assert self.in_maze(x, y)
        self.board[x][y] = WALL

    def remove_wall(self, x, y):
        assert self.in_maze(x, y)
        self.board[x][y] = EMPTY

    def in_maze(self, x, y):
        return 0 <= x < self.nrows and 0 <= y < self.ncolumns

    def write_to_file(self, filename):
        f = open(filename, 'w')
        f.write(str(self))
        f.close()

    @staticmethod
    def create_maze(rows, columns, seed=None, complexity=.7, density=.8):
        rows = (rows // 2) * 2 + 1
        columns = (columns // 2) * 2 + 1

        directions = []

        if seed is not None:
            np.random.seed(seed)

        # Adjust complexity and density relative to maze size
        complexity = int(complexity * (5 * (rows + columns)))
        density = int(density * ((rows // 2) * (columns // 2)))

        maze = Maze(rows, columns)
        maze.set_borders()

        # check if wallpoints are used more than 2 times
        wall_points = set()

        # Make aisles
        for i in range(density):
            x = np.random.random_integers(0, rows // 2) * 2
            y = np.random.random_integers(0, columns // 2) * 2
            maze.set_wall(x, y)

            for j in range(complexity):
                neighbours = []
                direction = []

                if maze.in_maze(x - 2, y):
                    neighbours.append((x - 2, y))
                    direction.append("L")

                if maze.in_maze(x + 2, y):
                    neighbours.append((x + 2, y))
                    direction.append("R")


                if maze.in_maze(x, y - 2):
                    neighbours.append((x, y - 2))
                    direction.append("U")


                if maze.in_maze(x, y + 2):
                    neighbours.append((x, y + 2))
                    direction.append("D")


                if maze.in_maze(x + 2, y + 2):
                    neighbours.append((x + 2, y + 2))
                    direction.append("UR")

                if maze.in_maze(x - 2, y - 2):
                    neighbours.append((x - 2, y - 2))
                    direction.append("LD")

                if maze.in_maze(x - 2, y + 2):
                    neighbours.append((x - 2, y + 2))
                    direction.append("LR")

                if maze.in_maze(x + 2, y - 2):
                    neighbours.append((x + 2, y - 2))
                    direction.append("UD")


                # find neighbors and add specific wall (only 1 wall per point)
                #print(len(neighbours))
                if len(neighbours):
                    index = np.random.randint(0, len(neighbours) - 1)
                    next_x, next_y = neighbours[index]
                    direction_choosen = direction[index]
                    #print("next X: ", next_x, " next Y: ", next_y, "direction: ", direction_choosen)

                    if not maze.is_wall(next_x, next_y) and (next_x, next_y) not in wall_points:
                        maze.set_wall(next_x, next_y)
                        maze.set_wall(next_x + (x - next_x) // 2,
                                      next_y + (y - next_y) // 2)
                        x, y = next_x, next_y
                        wall_points.add((x, y))
        print(wall_points)

        return maze

    @staticmethod
    def get_maze(path_to_maze):
        # new_maze = []
        max_txt = []
        with open(path_to_maze) as f:
            maze = f.readlines()#[1:10]
            for row in maze:
                new_row = []
                for col in row:
                    if col != '\n':
                        new_row.append(col)
                max_txt.append(new_row)
        print(max_txt)

        new_board = np.zeros((len(max_txt), len(max_txt[0])), dtype=WALL_TYPE)

        for i, maze_row in enumerate(max_txt):
            for j, element in enumerate(maze_row):
                if maze[i][j] == 'X':
                    new_board[i][j] = 1
                elif maze[i][j] == ' ':
                    new_board[i][j] = 0

        a_maze = Maze(len(max_txt),len(max_txt[0]))
        a_maze.board = new_board
        return a_maze



def generate_mazes(maze_id, num, rows, columns, seed=None, complexity=.7, density=.7):
    """
    args: 

    maze_id: 
    num: (int) number of maps to generate (default: 10)
    rows: (int) maps row size (default: 9)
    columns: (int) maps column size (default: 9)
    seed: seed of the maze to generate
    """
    counter = 0
    mazes = set()

    if seed:
        random.seed(seed)

    while len(mazes) < num:
        if counter > 5:
            raise ValueError('Unable to create the desired number of unique maps')

        map_seed = random.randint(0, 2147483647)

        #maze = Maze.create_maze(columns + 1, rows + 1, map_seed, complexity=complexity, density=density)
        #print(maze)
        maze = Maze.get_maze("/Users/aryakulkarni/Downloads/Generating-Interesting-Maps-in-Doom/MazeExplorer/my_maze_inputs/doomMap_15.txt")

        if maze in mazes:
            counter += 1
        else:
            counter = 0
            mazes.add(maze)

    for idx, maze in enumerate(sorted(mazes, key=lambda x: hash(x))):
        # prefix = 'TRAIN' if idx in train_indices else 'TEST'

        maze.write_to_file("{}_MAP{:02d}.txt".format(
            maze_id, idx + 1))

    return mazes
