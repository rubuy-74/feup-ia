import copy
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
      self.original = copy.deepcopy(matrix)
      self.coverage = set()
      
  def __str__(self):
    return (f"Map(rows={self.rows}, columns={self.columns}, backbone={self.backbone}, "
      f"budget={self.budget}, rtPrice={self.rtPrice}, bbPrice={self.bbPrice}, "
      f"rRange={self.rRange}, coverage={len(self.coverage)})")
      
  def isWall(self, coords: tuple):
    return self.original[coords] == Cell.WALL
  
  def isBackBone(self, coords: tuple):
    return coords == self.backbone

  def isCable(self, coords: tuple):
    return self.matrix[coords] == Cell.CABLE
  
  def isRouter(self, coords: tuple):
    return self.matrix[coords] in [Cell.ROUTER, Cell.CONNECTED_ROUTER, Cell.AFFECTED_ROUTER]
  
  def isVoid(self, coords: tuple):
    return self.original[coords] == Cell.VOID
  
  def get_path_cost(self, path: list):
    return len(path) * self.bbPrice + self.rtPrice - self.bbPrice
    
  def evaluate(self, remaining_budget: int):
    return 1000 * len(self.coverage) + remaining_budget
  
  def computeRouterTargets(self, routerCell: tuple):
    x, y = routerCell
    
    targets = set()
    rules = getWallRules(self, routerCell)
    
    for i in range(max(0, x - self.rRange), min(self.rows, x + self.rRange + 1)):
      for j in range(max(0, y - self.rRange), min(self.columns, y + self.rRange + 1)):
        newCell = (i, j)
        if not checkOutsideWallArea(cell=newCell, rules=rules): # not n^3 as len(rules) is not that big
          targets.add(newCell)

    return targets
  
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
          if m.original[newCell] == Cell.WALL:
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