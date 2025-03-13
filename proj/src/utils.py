import models.backbone as backbone
import models.cell as cell
import models.map as mapClass
import models.router as router

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

def getPathsLength(paths : dict) -> int:
  values = []
  for _,v in paths.items():
    values.append(len(v))
  return sum(values)

def getRouterTargets(routerCell: cell.Cell,routerRange: int,walls: list[cell.Cell]) -> list[cell.Cell]:
  # TODO: MISSING IMPLEMENTATION
  targets = []
  for i in range(0,routerRange):
    for j in range(0,routerRange):
      if((i == 0 and j == 0) or i == j): continue
      x = routerCell.x + i
      y = routerCell.y + j
      if cell.Cell(x,y) not in walls:
        targets.append(cell.Cell(x,y))
  return targets

def calculateTargets(routers : list[router.Router]) -> int:
  targetList : list[int] = list(map(lambda router: len(router.targets),routers))
  return sum(targetList)