import models.cell as cell
import models.backbone as backbone
import models.solution as solution
import numpy as np
from models.cell import Cell


class Map:
  def __init__(self, 
              rows : int, 
              columns : int, 
              backbone: tuple, 
              budget: int, 
              rtPrice: int, 
              bbPrice: int,
              rRange: int,
              matrix: np.ndarray):
      self.rows = rows
      self.columns = columns
      self.backbone = backbone
      self.budget = budget
      self.rtPrice = rtPrice
      self.bbPrice = bbPrice
      self.rRange = rRange
      self.backbone = backbone
      self.matrix = matrix
      
  def get_path_cost(self, path: list):
    return len(path) * self.bbPrice + self.rtPrice
      
  def computeRouterTargets(self, routerCell: tuple):
    x, y = routerCell
    
    targets = set()
    rules = getWallRules(self, routerCell)
    
    for i in range(max(0, x - self.rRange), min(self.rows, x + self.rRange + 1)):
      for j in range(max(0, y - self.rRange), min(self.columns, y + self.rRange + 1)):
        newCell = (i, j)
        if not checkOutsideWallArea(cell=newCell, rules=rules) and self.matrix[newCell] == Cell.TARGET: # not n^3 as len(rules) is not that big
          targets.add(newCell)

    return targets
  ####################### old stuff

  def __str__(self):
    return "[" + str(self.rows) + ", " + str(self.columns) + ", " + str(self.backbone) + ", " + str(self.walls) + ", " + str(self.voids) + ", " + str(self.targets) + "," + str(self.budget) +  "]"

  def get_cost(self, solution: solution.Solution) -> int:
    return len(solution.getBackboneCellsInSet()) * self.bbPrice + len(solution.routers) * self.rtPrice

  def evaluate(self, solution: solution.Solution) -> int:
    #print("Routers:", solution.routers)
    #print("BB cells:", solution.backbone_cells)

    cost = self.get_cost(solution)

    return 1000 * len(solution.computeCoverage()) + (self.budget - cost)

  
def checkOutsideWallArea(cell: tuple, rules: list[tuple]):
  # (1, 2, 3, 4) for a cell to be hided in the wall area, it must have:

  # 1 < x < 2
  # 3 < y < 4

  x, y = cell

  check = False

  for rule in rules:
      check = (rule[0] <= x <= rule[1] and rule[2] <= y <= rule[3])
      if check is True:
        return True
      
  return check

def getWallRules(m: Map, router: tuple):
  x, y = router
  
  rules = []
  
  for i in range(max(0, x - m.rRange), min(m.rows, x + m.rRange + 1)):
      for j in range(max(0, y - m.rRange), min(m.columns, y + m.rRange + 1)):
          if i == x and j == y:
              continue
          newCell = (i, j)
          if m.matrix[newCell] == Cell.WALL:
              rules.append(createWallArea(router, newCell))

  return rules
  
def createWallArea(router: tuple, wall: tuple):
  # each wall will protect from internet a specific "area". target cells won't be in any of those areas
  # (1, 2, 3, 4) for a cell to be hided in the wall area, it must have:

  # 1 < x < 2
  # 3 < y < 4
  
  x, y = wall
  rx, ry = router
  
  inf = float('inf')

  if y == ry:
     if x > rx:
        return (x, inf, 0, inf)
     elif x < rx:
        return (0, x, 0, inf)
     
  if x == rx:
    if y > ry:
      return (0, inf, y, inf)
    elif y < ry:
      return (0, inf, 0, y)

  # Left up
  if y <= ry and x <= rx:
    return (0, x, 0, y)
  # Right up
  if y <= ry and x >= rx:
    return (x, inf, 0, y)
  # Left down
  if y >= ry and x <= rx:
    return (0, x, y, inf)
  # Right down
  if x >= rx and y >= ry:
    return (x, inf, y, inf)
    

  return ()