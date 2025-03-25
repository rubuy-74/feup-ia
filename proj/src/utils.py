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
    b = backbone.Backbone(cell.Cell(int(bx), int(by)), int(bb_cost))
    
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