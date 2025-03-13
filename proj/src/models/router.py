from models import cell
import utils as utils
import math
class Router:
  def __init__(self, cell, range_, cost, rWalls):
    self.cell = cell
    self.range_ = range_
    self.cost = cost
    self.targets = utils.getRouterTargets(routerCell=cell,routerRange=range_,walls=rWalls) 

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
  
""" def getWallRange(range_: int, x:int,y:int, walls: list[cell.Cell], columns,) -> list[cell.Cell]:
  rWalls = []

  for i in range(-range_,range_):
    for j in range(-range_,range_):
      if c(x+i,y+i) and (cell.Cell(x+i,y+j) in walls):
        rWalls.append(cell.Cell(x+i,y+j))
  return rWalls """

def computeRules(router: Router, walls: list[cell.Cell]):
  rules = ((1, 4), (8, 12))
  
  
  min_x = math.inf
  max_x = 0
  min_y = math.inf
  max_y = 0

  for w in walls:
    # ul
    if w.x <= router.x and w.y <= router.y:
      if w.x < min_x:
        min_x = w.x
      if w.y < min_y:
        min_y = w.y
    # ur
    if w.x >= router.x and w.y <= router.y:
      if w.x > max_x:
        max_x = w.x
      if w.y < min_y:
        min_y = w.y
    # dl
    if w.x <= router.x and w.y >= router.y:
      if w.x < min_x:
        min_x = w.x
      if w.y > max_y:
        max_y = w.y
    # dr
    if w.x >= router.x and w.y >= router.y:
      if w.x > max_x:
        max_x = w.x
      if w.y > max_y:
        max_y = w.y