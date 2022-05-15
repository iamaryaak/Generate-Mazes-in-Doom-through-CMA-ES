# Generating-Interesting-Maps-in-Doom using Evolutionary Algorithms
### Libraries used:
ViZDoom, MazeExplorer, Omgifol, Numpy


### To Run:
a. cd into ~/MazeExplorer

b. python3 gen_maze_sandbox.py


### Changes to make per individual:
a. Replace ~/MazeExplorer/mazeexplorer/maze.py with attached file (change line 163 to match your own path based on you local filesystem)

b. Replace ~/MazeExplorer/mazeexplorer/mazeexploreer.py with attached file (change line 82 to match your own path based on you local filesystem)


### Evolutionary Algorithm: CMA-ES
We create a Vector of random points for the healthpacks (5) and random points for the wall verticies (15 points) and send that vector through CMA-ES to return multiple new vectors. 
