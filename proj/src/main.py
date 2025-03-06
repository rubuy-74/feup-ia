import sys
import random
import collections

class Cell:
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y
  
  def __str__(self):
    return "(" + str(self.x) + "," + str(self.y) + ")"
  
  def __repr__(self):
    return str(self)
  
  def __eq__(self, other):
    if isinstance(other, Cell):
        return self.x == other.x and self.y == other.y
    return False
  
  def __hash__(self):
    return hash((self.x, self.y))

class Backbone:
  def  __init__(self, cell, cost, connected_to):
      self.cell = cell
      self.cost = cost
      self.connected_to = connected_to
      
  def __str__(self):
    return "[" + str(self.cell) + ", " + str(self.cost) + ", " + str(self.connected_to) + "]"  
  
class Map:
  def __init__(self, rows, columns, walls, voids, targets, backbone, budget):
      self.rows = rows
      self.columns = columns
      self.walls = walls
      self.voids = voids
      self.targets = targets
      self.wired = set()
      self.backbone = backbone
      self.budget = budget

  def __str__(self):
    return "[" + str(self.rows) + ", " + str(self.columns) + ", " + str(self.backbone) + ", " + str(self.walls) + ", " + str(self.voids) + ", " + str(self.targets) + ", " + str(self.wired) + "," + str(self.budget) +  "]"
  
class Router:
  def __init__(self, cell, range_, cost):
    self.cell = cell
    self.range_ = range_
    self.cost = cost

  def __str__(self):
    return "[" + str(self.cell) + ", " + str(self.cost) + ", " + str(self.range_) + "]"

  def __repr__(self):
    return str(self)  
  
  def __eq__(self, other):
    if isinstance(other, Router):
        return self.cell == other.cell
    return False
  
  def __hash__(self):
    return hash((self.cell, self.range_, self.cost))

class Solution:
  def __init__(self, routers, cost, fiber):
    self.routers = routers
    self.cost = cost
    self.fiber = fiber

  def __str__(self):
    return "[" + str(self.routers) + ", " + str(self.cost) + ", " + str(self.fiber) + "]"

def adjacents(cell: Cell):
  adjXpos = cell.x + 1
  adjXneg = cell.x - 1
  adjYpos = cell.y + 1
  adjYneg = cell.y - 1

  # adjacent cells in clockwise order starting from top-left corner
  return [Cell(adjXneg, adjYneg), Cell(cell.x, adjYneg), Cell(adjXpos, adjYneg), Cell(adjXpos, cell.y), Cell(adjXpos, adjYpos), Cell(cell.x, adjYpos), Cell(adjXneg, adjYpos), Cell(adjXneg, cell.y)]

def is_wall(cell: Cell, map: Map):
  return cell in map.walls

def is_target(cell: Cell, map: Map):
  return cell in map.targets

def is_void(cell: Cell, map: Map):
  return cell in map.voids

def is_wired(cell: Cell, map: Map):
  return cell in map.wired

def is_backbone(cell: Cell, map: Map):
  return cell.x == map.backbone.cell.x and cell.y == map.backbone.cell.y

def parse(file):
  with open(file, "r") as f:
    lines = f.readlines()
  
    rows, columns, range_ = lines[0].split(" ")
    bb_cost, rt_cost, budget = lines[1].split(" ")
    bx, by = lines[2].split(" ")

    targets = set() # testing with sets for O(1)
    voids = set()
    walls = set()
    backbone = Backbone(Cell(int(bx), int(by)), int(bb_cost), [])
    
    for i, line in enumerate(lines[3:]):
      for j, cell in enumerate(line):
        pos = Cell(i, j)
        match cell:
          case ".":
            targets.add(pos)
          case "-":
            voids.add(pos)
          case "#":
            walls.add(pos)

    return Map(int(rows), int(columns), walls, voids, targets, backbone, int(budget)), int(rt_cost), int(range_)
  
def bfs(map: Map, start: Cell, target: Cell):
  queue = collections.deque([(start, [start])])
  visited = set()
  visited.add(start)

  while queue:
    current_cell, path = queue.popleft()
    if current_cell.x == target.x and current_cell.y == target.y:
      return path
    
    for adj in adjacents(current_cell):
      if 0 <= adj.x < map.rows and 0 <= adj.y < map.columns and adj not in visited:
        visited.add(adj)
        queue.append((adj, path + [adj]))      

  return []

def find_nearest_available_cell_to_router(map: Map, routers: list):
  queue = collections.deque([map.backbone.cell])
  visited = set()
  visited.add(map.backbone.cell)

  while queue:
    possible_cell = queue.popleft()

    if not is_wall(possible_cell, map) and not is_backbone(possible_cell, map) and not is_wired(possible_cell, map) and not is_void(possible_cell, map) and possible_cell not in routers:
      return possible_cell
    
    for adj in adjacents(possible_cell):
      if 0 <= adj.x < map.rows and 0 <= adj.y < map.columns and adj not in visited:
        visited.add(adj)
        queue.append(adj)
  
  return None

def compute_targets(map: Map, router: Router):
  targets = set()
  range_ = router.range_
  rx, ry = router.cell.x, router.cell.y

  for x in range(max(0, rx - range_), min(map.rows, rx + range_ + 1)):
    for y in range(max(0, ry - range_), min(map.columns, ry + range_ + 1)):
      if abs(rx - x) <= range_ and abs(ry - y) <= range_:
        if not any(is_wall(Cell(w, v), map) for w in range(min(rx, x), max(rx, x)) for v in range(min(ry, y), max(ry, y))):
          possible_target = Cell(x, y)
          
          if is_target(possible_target, map):
            targets.add(possible_target)

  return targets

def greedy(map: Map, router_cost, router_range):
  solution = Solution([], 0, set())

  while True:
    # find the closest available cell of the backbone to place a router
    cell_to_router = find_nearest_available_cell_to_router(map, [router.cell for router in solution.routers])

    if(cell_to_router is None):
      break

    # create the router
    router = Router(cell_to_router, router_cost, router_range)
    
    # find the shortest path between the router and the backbone
    path = bfs(map, map.backbone.cell, router.cell)

    # update cost
    new_cost = solution.cost + router_cost + map.backbone.cost * (len(path)-1)

    if new_cost <= map.budget:
      solution.cost = new_cost
      solution.routers.append(router)
      solution.fiber.update(path)

      # update targets based on the new router
      map.wired.update(compute_targets(map, router))

      # update the backbone connections
      map.backbone.connected_to.extend(path)
    else:
      break
   
  return solution


def main():
  map, router_cost, router_range = parse(sys.argv[1])
  
  sol = greedy(map, router_cost, router_range)
  
  print(sol)


if __name__ == "__main__":
  main()
