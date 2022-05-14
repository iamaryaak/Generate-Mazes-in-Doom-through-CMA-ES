from omg import *
from maze import *
from wad import *
import numpy
import cma

# Global Variables
WALL = 1
EMPTY = 0

# print map 
def print_map(board):
	# Print the rows
	for r in board:
		#print(r)
		rowprint = ""
		for c in r:
			if c == WALL:
				rowprint = rowprint + "X"
			else:
				rowprint = rowprint + " "
		print(rowprint)


## TO DO
#  find representations for enemies and keys
##

# make sure to add floor/ceiling
def create_map():
	# create clear map 11x11
	base_map = [[WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL],
		[WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL]]
	
	print_map(base_map)

	nodes = []
	node_element = []
	# find appropriate wall points with direction (wall will be 2 spaces long)
	wall_points = []
	for i in range(20):
		x = random.randint(1, 9)
		y = random.randint(1, 9)
		wall_points.append((x,y))
		#print(wall_points)
		node_element = (x,y)
		nodes.append(wall_points)
		node_element = []

	for point in wall_points:
		#print(point)
		#print(base_map[point[0]][point[1]])
		base_map[point[0]][point[1]] = WALL
	
	# add a wall that goes up or right at these points
	prob = 0.3
	ct = 0
	for point in wall_points:
		print(nodes[ct])
		if type(point[0]) == int and type(point[1]) == int:
			probCompare = random.random()
			if probCompare < prob:
				# add wall that goes up
				#print("Wall faces up")
				nodes[ct].append("Up")
				base_map[point[0]-1][point[1]] = WALL
			elif probCompare > 0.3 and probCompare < 0.6:
				# add wall that goes right
				#print("Wall faces right")
				nodes[ct].append("Right")
				base_map[point[0]][point[1]+1] = WALL
			else:
				# add wall that goes diagonal Up
				#print("Wall faces Diagonal")
				nodes[ct].append("Diagonal Up")
				base_map[point[0]+1][point[1]+1] = WALL
		ct = ct + 1
	#print(nodes)

	# print map
	print_map(base_map)

	# save map as a .txt file
	with open('testMap1.txt', 'w') as output_file:
		for row in base_map:
			rowprint = ""
			for c in row:
				if c == WALL:
					rowprint = rowprint + "X"
				else:
					rowprint = rowprint + " " 
			output_file.write(rowprint)
			output_file.write("\n")
	output_file.close()
	print(output_file, " is created!")
	return output_file

# main
maze_path = "tempfile"
maze_id = 3
# mazes = generate_mazes(maze_path, maze_id)

# create .txt representation of this
testMap1 = create_map()


