from omg import *
from maze import *
from wad import *
import numpy

# Global Variables
WALL = 1
EMPTY = 0

maze = []

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


# make sure to add floor/ceiling and angel
# [x, y, up/right OR (0 < angle < 45)]
def create_map():

	# Nodes
	nodes = []
	node_element = []
	
	# create clear map 9x9
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


    
	# find appropriate wall points with direction (wall will be 2 spaces long)
	wall_points = []
	for i in range(20):
		x = random.randint(1, 9)
		y = random.randint(1, 9)
		wall_points.append((x, y))
		node_element.append(x)
		node_element.append(y)
		nodes.append(node_element)
		node_element = []
	
	for point in wall_points:
		print(point)
		#print(base_map[point[0]][point[1]])
		base_map[point[0]][point[1]] = WALL
		        
	# add a wall that goes up or right at these points or diagonal
	prob = 0.5
	prob_up_right = 0.5
	ct = 0
	for point in wall_points:
		if random.random() < prob_up_right:
			if random.random() < prob:
				# add wall that goes up
				#print("Wall faces up")
				nodes[ct].append("up")
				base_map[point[0]-1][point[1]] = WALL
			else:
				# add wall that goes right
				#print("Wall faces right")
				nodes[ct].append("right")
				base_map[point[0]+1][point[1]] = WALL
		else:
			#print("Wall is diagonal 45  degrees")
			nodes[ct].append("diagonal")
			base_map[point[0]+1][point[1]+1] = WALL
		ct = ct + 1

	print_map(base_map)
	
	# print nodes for walls
	print("\n")
	print("Nodes: ")
	for n in nodes:
		print(n)

    
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

###
# TODO: 
# create config file
# create WAD file
###
