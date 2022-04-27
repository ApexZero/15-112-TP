from cmu_112_graphics import *
import math


#Structure taken from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
#yizes/Shawn checked it 
class Node():
    def __init__(self, parent = None, position = None):
        self.parent = parent
        self.position = position
        self.gScore = 0
        self.fScore = 0
        self.hScore = 0
    
    def __eq__(self, other):
        return self.position == other.position
        #give each node a unique identifier, just don't call everything the same


def heuristic(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


#Structure taken from https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
#yizes/Shawn checked it 
def AStar(grid, start, goal):
    # print(start)
    # print(goal)
    rows = len(grid)
    cols = len(grid[0])
    startNode = Node(None, start)
    startNode.gScore = 0
    startNode.fScore = 0
    startNode.hScore = 0
    endNode = Node(None, goal)
    endNode.gScore = 0
    endNode.fScore = 0
    endNode.hScore = 0
    openList = [] #locations that are movable
    closeList = [] #locations that can't move to
    
    openList.append(startNode)
    while len(openList) > 0:
        currentNode = openList[0]
        currentIndex = 0
        for index, item in enumerate(openList):
            if item.fScore < currentNode.fScore:
                currentNode = item
                currentIndex = index
        openList.pop(currentIndex)
        closeList.append(currentNode)

        if currentNode == endNode:
            path = []
            current = currentNode
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        
        children = []
        moves = [(1,0), (0,1), (-1,0), (0,-1)]
        for newPosition in moves:
            newRow = currentNode.position[0] + newPosition[0]
            newCol = currentNode.position[1] + newPosition[1]
            nodePosition = (newRow, newCol)
            nodeRow = nodePosition[0]
            nodeCol = nodePosition[1]
            if nodeRow > rows or nodeRow < 0 or nodeCol > cols or nodeCol < 0:
                continue
            if grid[nodeRow][nodeCol] != 'p':
                continue
            newNode = Node(currentNode, nodePosition)
            children.append(newNode)
        
        for child in children:
            for closeChild in closeList:
                if child == closeChild:
                    continue
            child.gScore = currentNode.gScore + 1
            child.hScore = heuristic(child.position, endNode.position)
            child.fScore = child.gScore + child.hScore

            for openNode in openList:
                if child == openNode and child.gScore > openNode.gScore:
                    continue
            openList.append(child)