from models.cell import Cell
import models.map as mapClass
import numpy as np


def parse(file):
  with open(file, "r") as f:
    lines = f.readlines()
  
    rows, columns, range_ = lines[0].split(" ")
    bb_cost, rt_cost, budget = lines[1].split(" ")
    bx, by = lines[2].split(" ")
    
    b = (int(by), int(bx))
    
    matrix = np.zeros((int(rows), int(columns)), dtype=np.int8)
    
    for i, line in enumerate(lines[3:]):
      for j, c in enumerate(line):
        match c:
          case ".":
            matrix[i, j] = Cell.TARGET
          case "-":
            matrix[i, j] = Cell.VOID
          case "#":
            matrix[i, j] = Cell.WALL
          case "r":
            matrix[i, j] = Cell.CONNECTED_ROUTER
          case "o":
            matrix[i, j] = Cell.CABLE

    return mapClass.Map(
      rows=int(rows),
      columns=int(columns),
      backbone=b,
      budget=int(budget),
      rtPrice=int(rt_cost),
      bbPrice=int(bb_cost),
      rRange=int(range_),
      matrix=matrix
    )

def dump_solution(file_name  : str,m : mapClass,remaining_budget: int,it: int, time_spent):
  output_path = f"../output/out/{file_name}"

  rows, columns, range_ = m.rows,m.columns,m.rRange
  bb_cost, rt_cost, budget = m.bbPrice,m.rtPrice, m.budget
  bx, by = m.backbone[0],m.backbone[1]

  output = list()
  for line in m.matrix:
    output_line = []
    for elem in line:
      match elem:
        case Cell.TARGET:
          value = "."
        case Cell.VOID:
          value = "-"
        case Cell.WALL:
          value = "#"
        case Cell.CONNECTED_ROUTER:
          value = "r"
        case Cell.CABLE:
          value = "o"
      output_line.append(value)
    output.append(output_line)
  with open(output_path,'w+') as output_file:
    output_file.write(f'{time_spent} {it}\n')
    print(m.evaluate(remaining_budget))
    print(remaining_budget)
    output_file.write(f'{m.evaluate(remaining_budget)}\n')
    output_file.write(f'{rows} {columns} {range_}\n')
    output_file.write(f'{bb_cost} {rt_cost} {budget}\n')
    output_file.write(f'{bx} {by}\n')

    for line in output:
      output_file.write(f"{"".join(line)}\n")

def convertDictToSet(d):
  result = set()
  
  for item in d.values():
    result.update(item)

  return result

def computeAdjacents(coords: tuple):
  x, y = coords
  
  adjXpos = x + 1
  adjXneg = x - 1
  adjYpos = y + 1
  adjYneg = y - 1
  
  # adjacent cells in clockwise order starting from top-left corner
  return [
    (adjXneg, y),
    (adjXpos, y),
    (x, adjYneg), 
    (x, adjYpos),
    (adjXneg, adjYneg),
    (adjXpos, adjYneg), 
    (adjXpos, adjYpos), 
    (adjXneg, adjYpos), 
  ]