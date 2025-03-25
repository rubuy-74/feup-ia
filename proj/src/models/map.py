import models.cell as cell
import models.backbone as backbone
import models.solution as solution


class Map:
  def __init__(self, 
              rows : int, 
              columns : int, 
              walls : set[cell.Cell], 
              voids : set[cell.Cell], 
              targets: set[cell.Cell], 
              backbone: backbone.Backbone, 
              budget: int, 
              rtPrice: int, 
              bbPrice: int,
              rRange: int):
      self.rows = rows
      self.columns = columns
      self.walls = walls
      self.voids = voids
      self.targets = targets
      self.routers = set()
      self.wired = set()
      self.backbone = backbone
      self.budget = budget
      self.rtPrice = rtPrice
      self.bbPrice = bbPrice
      self.rRange = rRange

  def __str__(self):
    return "[" + str(self.rows) + ", " + str(self.columns) + ", " + str(self.backbone) + ", " + str(self.walls) + ", " + str(self.voids) + ", " + str(self.targets) + ", " + str(self.wired) + "," + str(self.budget) +  "]"

  def isWall(self,cell: cell.Cell):
    return cell in self.walls

  def isTarget(self,cell: cell.Cell):
    return cell in self.targets

  def isVoid(self,cell: cell.Cell):
    return cell in self.voids

  def isWired(self,cell: cell.Cell):
    return cell in self.wired

  def isBackbone(self,cell: cell.Cell):
    return cell == self.backbone.cell

  def evaluate(self,solution: solution.Solution) -> int:
    print("Routers:", solution.routers)
    print("BB cells:", solution.backbone_cells)

    cost = len(solution.backbone_cells) * self.bbPrice + len(solution.routers) * self.rtPrice

    print("Cost:", cost)
    return 1000 * len(solution.getTargets()) + ( self.budget - cost )

  def computeRouterTargets(self, routerCell:cell.Cell) -> list[cell.Cell]:
    targets = []
    rules = getWallRules(self, routerCell)
    
    for i in range(max(0, routerCell.y - self.rRange), min(self.rows, routerCell.y + self.rRange + 1)):
          for j in range(max(0, routerCell.x - self.rRange), min(self.columns, routerCell.x + self.rRange + 1)):
              newCell = cell.Cell(j, i)
              if not checkOutsideWallArea(cell=newCell, rules=rules): # not n^3 as len(rules) is not that big
                  targets.append(newCell)
                  self.wired.add(newCell)            

    return targets
  
def checkOutsideWallArea(cell: cell.Cell, rules: list[tuple]):
   # (1, 2, 3, 4) for a cell to be hided in the wall area, it must have:

    # 1 < x < 2
    # 3 < y < 4

    check = False

    for rule in rules:
       check = (rule[0] <= cell.x <= rule[1] and rule[2] <= cell.y <= rule[3])
       if check is True:
          return True
       
    return check

def getWallRules(m: Map, router: cell.Cell) -> list[tuple]:
  rules = []
  for i in range(max(0, router.y - m.rRange), min(m.rows, router.y + m.rRange + 1)):
      for j in range(max(0, router.x - m.rRange), min(m.columns, router.x + m.rRange + 1)):
          if i == router.y and j == router.x:
              continue
          newCell = cell.Cell(j, i)
          if m.isWall(newCell):
              rules.append(createWallArea(router, newCell))

  return rules
  
def createWallArea(router: cell.Cell, wall: cell.Cell) -> tuple:
  # each wall will protect from internet a specific "area". target cells won't be in any of those areas
  # (1, 2, 3, 4) for a cell to be hided in the wall area, it must have:

  # 1 < x < 2
  # 3 < y < 4
  
  inf = float('inf')

  if wall.y == router.y:
     if wall.x > router.x:
        return (wall.x, inf, 0, inf)
     elif wall.x < router.x:
        return (0, wall.x, 0, inf)
     
  if wall.x == router.x:
    if wall.y > router.y:
      return (0, inf, wall.y, inf)
    elif wall.y < router.y:
      return (0, inf, 0, wall.y)

  # Left up
  if wall.y <= router.y and wall.x <= router.x:
    return (0, wall.x, 0, wall.y)
  # Right up
  if wall.y <= router.y and wall.x >= router.x:
    return (wall.x, inf, 0, wall.y)
  # Left down
  if wall.y >= router.y and wall.x <= router.x:
    return (0, wall.x, wall.y, inf)
  # Right down
  if wall.x >= router.x and wall.y >= router.y:
    return (wall.x, inf, wall.y, inf)
    

  return ()