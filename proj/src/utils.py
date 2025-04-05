import models.backbone as backbone
import models.cell as cell
import models.map as mapClass
from models.router import Router
from models.solution import Solution

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
    r = set()
    
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
          case "r":
            r.add(Router(pos, range_, rt_cost, []))

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
      rRange=int(range_),
      routers=r
    )

def dump_solution(file_name  : str,solution : Solution):
  input_path = f"../maps/{file_name}"
  output_path = f"../output/{file_name}"
  rows, columns, range_ = ("","","")
  bb_cost, rt_cost, budget = ("","","")
  bx, by = ("","")
  lines = list()
  with open(input_path,'r') as input_file:
    lines = input_file.readlines()
    rows, columns, range_ = lines[0].split(" ")
    bb_cost, rt_cost, budget = lines[1].split(" ")
    bx, by = lines[2].split(" ")
    lines = list(map(lambda x: list(x),lines[3:]))
  for router in solution.routers:
    router_cell = router.cell
    for backbone_cell in solution.backbone_cells[router_cell]:
      lines[backbone_cell.y][backbone_cell.x] = 'o'
    lines[router_cell.y][router_cell.x] = 'r'
  lines = list(map(lambda x: "".join(x),lines))
    
  with open(output_path,'w+') as output_file:
    output_file.write(f'{rows} {columns} {range_}\n')
    output_file.write(f'{bb_cost} {rt_cost} {budget}\n')
    output_file.write(f'{bx} {by}\n')

    for line in lines:
      output_file.write(line)

  
def convertDictToSet(d):
  result = set()
  
  for item in d.values():
    result.update(item)

  return result