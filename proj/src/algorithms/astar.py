import models.cell as cell
import models.map as classMap
import heapq

class Node:
    def __init__(self, position : cell.Cell, parent=None):
        self.position = position  # (x, y)
        self.parent = parent      # Node

        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost to goal
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f

def heuristic(a : cell.Cell, b : cell.Cell) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)

def nonWallAdjacent(map: classMap.Map,c : cell.Cell) -> list[cell.Cell]:
    return list(filter(lambda adj: not map.isWall(adj),c.adjacents()))

def astar(map : classMap.Map, start : cell.Cell, end : cell.Cell):
    openList = []
    closedSet = set()

    startNode = Node(start)
    endNode = Node(end)

    heapq.heappush(openList,startNode)

    while openList:
        currentNode : Node = heapq.heappop(openList)

        if currentNode.position == endNode.position:
            path = []

            while currentNode:
                path.append(currentNode.position)
                currentNode = currentNode.parent
            return path[::-1]
        
        closedSet.add(currentNode.position)
        for neighbor in nonWallAdjacent(map,currentNode.position):
            if (0 <= neighbor.x < map.columns) and (0 <= neighbor.y < map.rows):
                if neighbor in closedSet:
                    continue

                neighborNode = Node(neighbor,currentNode)
                neighborNode.g = currentNode.g + 1
                neighborNode.h = heuristic(neighbor,endNode.position)
                neighborNode.f = neighborNode.g + neighborNode.h
                if any(openNode.position == neighborNode.position and openNode.f <= neighborNode.f for openNode in openList):
                    continue

                heapq.heappush(openList,neighborNode)
    return None
