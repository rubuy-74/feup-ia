import models.backbone as backbone
from models.cell import Cell
import models.map as mapClass
import numpy as np

def parse(file):
  with open(file, "r") as f:
    lines = f.readlines()
  
    rows, columns, range_ = lines[0].split(" ")
    bb_cost, rt_cost, budget = lines[1].split(" ")
    bx, by = lines[2].split(" ")
    
    b = (int(bx), int(by))
    
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