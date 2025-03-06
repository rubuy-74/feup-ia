import sys

class Position:
  def __init__(self, x, y):
    self.x = x
    self.y = y
  
  def __str__(self):
    return "(" + str(self.x) + "," + str(self.y) + ")"
  
  def __repr__(self):
    return str(self)

class Backbone:
  def  __init__(self, pos, cost, connected_to):
      self.position = pos
      self.cost = cost
      self.connected_to = connected_to
    
  def __str__(self):
    return "[" + str(self.position) + ", " + str(self.cost) + ", " + str(self.connected_to) + "]"  
class Map:
  def __init__(self, rows, columns, walls, voids, targets, backbone, budget):
      self.rows = rows
      self.columns = columns
      self.walls = walls
      self.voids = voids
      self.targets = targets
      self.backbone = backbone
      self.budget = budget

  def __str__(self):
    return "[" + str(self.rows) + ", " + str(self.columns) + ", " + str(self.backbone) + ", " + str(self.walls) + ", " + str(self.voids) + ", " + str(self.targets) + ", " + str(self.budget) +  "]"
class Router:
  def __init__(self, pos, range_, cost):
    self.position = pos
    self.range_ = range_
    self.cost = cost

def parse(file):
  with open(file, "r") as f:
    lines = f.readlines()
  
    rows, columns, range_ = lines[0].split(" ")
    bb_cost, rt_cost, budget = lines[1].split(" ")
    bx, by = lines[2].split(" ")

    targets = []
    voids = []
    walls = []
    backbone = Backbone(Position(bx, by), bb_cost, [])
    
    for i, line in enumerate(lines[3:]):
      for j, cell in enumerate(line):
        pos = Position(i, j)
        match cell:
          case ".":
            targets.append(pos)
          case "-":
            voids.append(pos)
          case "#":
            walls.append(pos)

    return Map(rows, columns, walls, voids, targets, backbone, budget)

def main():
  map = parse(sys.argv[1])
  print(map)


if __name__ == "__main__":
  main()