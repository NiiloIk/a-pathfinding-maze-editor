# -*- coding: utf-8 -*-
"""

This code is from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
Except the Maze is now for the Labyrinth task for Tekniska Museet case

"""

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None, directions=[(1, 0), (-1, 0), (0, 1), (0, -1)]): # Initially all directions are allowed
        self.parent = parent
        self.position = position
        self.directions = directions

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position and self.directions == other.directions


def astar(maze, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    def getRightDirection(position): # gets the right direction depending on your current direction 
        match position:
            case (1, 0):
                return (0, -1)
            case (0, -1):
                return (-1, 0)
            case (-1, 0):
                return (0, 1)
            case (0, 1):
                return (1, 0)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node.position == end_node.position:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        
        for new_position in current_node.directions: # Checks for the allowed directions for new positions
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] != 0:
                continue
                    
            directions = [new_position, getRightDirection(new_position)] # only allowed to go straight or right.

            # Create new node
            new_node = Node(current_node, node_position, directions)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:
            
            # Child is on the visited list (search entire visited list)
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            # Heuristic costs calculated here, this is using eucledian distance
            child.h = (((child.position[0] - end_node.position[0]) ** 2) + 
                       ((child.position[1] - end_node.position[1]) ** 2)) 

            child.f = child.g + child.h

            # Child is already in the yet_to_visit list and f cost is already lower
            if len([open_node for open_node in open_list if child == open_node and child.f > open_node.f]) > 0:
                continue

            # Add the child to the yet_to_visit list
            open_list.append(child)


def main():
    maze1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0 ,1, 1, 1, 0, 1, 1, 1, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0 ,1, 1, 1, 1, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0],
            [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]]

    start1 = (11, 10)
    end1 = (11, 2)

    maze2 = [[1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
             [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
             [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
             [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
             [0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
             [0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1],
             [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
             [0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    
    start2 = (0, 2)
    end2 = (2, 12)

    maze3 = [[1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
             [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
             [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
             [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1],
             [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
             [0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1],
             [0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1],
             [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
             [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
             [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
             [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1]]

    start3 = (0, 2)
    end3 = (9, 11)

    # We define a reusable function.

    def printPath(maze, start, end, name):
        path = astar(maze, start, end) # Get the path using astar function
        print(f"The path for maze {name}:\n{path}\n")

    printPath(maze1, start1, end1, "1")
    printPath(maze2, start2, end2, "2")
    printPath(maze3, start3, end3, "3")

if __name__ == '__main__':
    main()