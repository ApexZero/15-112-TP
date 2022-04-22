from cmu_112_graphics import *
import math
from queue import PriorityQueue

def heuristic(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

#Structure taken from Wikipedia
def reconstructPath(previous, current):
    while current in previous:
        current = previous[current]
        previous.prepend(current)
    return previous

#Structure taken from Wikipedia
def AStar(grid, start, goal):
    openSet = PriorityQueue
    previous = dict()
    gScore = {location: float('inf') for row in grid for location in row}
    gScore[start] = 0
    fScore = {location: float('inf') for row in grid for location in row}
    fScore[start] = heuristic(start, goal)
    openSetCheck = set(start)
    while openSet.empty() != True:
        current = openSet.get()[2]
        openSetCheck.remove(current)
        if current == goal:
            reconstructPath(previous, goal)
            return True
        for neighbor in current:
            tempGScore = gScore[current] + 1
            if tempGScore < gScore[neighbor]:
                previous[neighbor] = current
                gScore[neighbor] = tempGScore
                fScore[neighbor] = tempGScore + heuristic(neighbor, goal)
                if neighbor not in openSetCheck:
                    openSetCheck.add(neighbor)
    return False