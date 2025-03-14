import models.backbone as backbone
import models.cell as cell
import models.map as mapClass

def parse(file):
  with open(file, "r") as f:
    lines = f.readlines()
  
    rows, columns, range_ = lines[0].split(" ")
    bb_cost, rt_cost, budget = lines[1].split(" ")
    bx, by = lines[2].split(" ")

    t = set() # testing with sets for O(1)
    v = set()
    w = set()
    b = backbone.Backbone(cell.Cell(int(bx), int(by)), int(bb_cost), [])
    
    for i, line in enumerate(lines[3:]):
      for j, c in enumerate(line):
        pos = cell.Cell(i, j)
        match c:
          case ".":
            t.add(pos)
          case "-":
            v.add(pos)
          case "#":
            w.add(pos)

    return mapClass.Map(
      rows=int(rows),
      columns=int(columns),
      walls=w,
      voids=v,
      targets=t,
      backbone=b,
      budget=int(budget),
      rtPrice=int(rt_cost),
      bbPrice=int(bb_cost),
      rRange=int(range_)
    )

def checkCoverage(w: cell.Cell, routerCell: cell.Cell, compareCell : cell.Cell) -> bool:
  # just to be sure
  if(w.y == routerCell.y and w.x == routerCell.x):
    return False
  # Left up
  if w.y <= routerCell.y and w.x <= routerCell.x:
    result = compareCell.y > w.y or compareCell.x > w.x
    return result
  # Right up
  if w.y >= routerCell.y and w.x <= routerCell.x:
    result = compareCell.y < w.y or compareCell.x > w.x
    return result
  # Left down
  if w.y <= routerCell.y and w.x >= routerCell.x:
    result = compareCell.y > w.y or compareCell.x < w.x
    return result
  # Right down
  if w.y >= routerCell.y and w.y >= routerCell.y:
    result = compareCell.y < w.y or compareCell.x < w.x
    return result

  return True
  
def checkWalls(newCell : cell.Cell,routerCell : cell.Cell, walls: list[cell.Cell]) -> bool:
  for x in walls:
    if(not checkCoverage(x,routerCell,newCell)): 
      return False
  return True

def getTargets(routerCell : cell.Cell,map : mapClass.Map) -> list[cell.Cell]:
  targets = []
  walls = map.getWallRange(routerCell)

  for i in range(-map.rRange,map.rRange+1):
    for j in range(-map.rRange,map.rRange+1):
        newCell = cell.Cell(routerCell.x + i, routerCell.y + j)
        if(checkWalls(newCell,routerCell,walls)):
          targets.append(newCell) 
  return targets
