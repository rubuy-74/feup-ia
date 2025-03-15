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
        pos = cell.Cell(j, i)
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

def getTargets(routerCell : cell.Cell, map : mapClass.Map) -> list[cell.Cell]:
  targets = []
  rules = getWallRules(map, routerCell)
  
  for i in range(max(0, routerCell.y - map.rRange), min(map.rows, routerCell.y + map.rRange + 1)):
        for j in range(max(0, routerCell.x - map.rRange), min(map.columns, routerCell.x + map.rRange + 1)):
            newCell = cell.Cell(j, i)
            if not checkOutsideWallArea(cell=newCell, rules=rules): # not n^3 as len(rules) is not that big
                targets.append(newCell)
                map.wired.add(newCell)

  return targets

def getWallRules(map: mapClass.Map, router: cell.Cell) -> list[tuple]:
  rules = []
  for i in range(max(0, router.y - map.rRange), min(map.rows, router.y + map.rRange + 1)):
      for j in range(max(0, router.x - map.rRange), min(map.columns, router.x + map.rRange + 1)):
          if i == router.y and j == router.x:
              continue
          newCell = cell.Cell(j, i)
          if map.isWall(newCell):
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
