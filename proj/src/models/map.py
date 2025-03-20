import models.cell as cell
import models.backbone as backbone
import models.solution as solution


class Map:
  def __init__(self, 
              rows : int, 
              columns : int, 
              walls : list[cell.Cell], 
              voids : list[cell.Cell], 
              targets: list[cell.Cell], 
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
    print("Targeted cells: " + str(solution.t))
    print("BB cells: " + str(solution.m))
    print("Cost: " + str(solution.m * self.bbPrice + solution.n * self.rtPrice))
    print("Router cells: " + str(solution.n))
    return 1000 * solution.t + ( self.budget - ( solution.m * self.bbPrice + solution.n * self.rtPrice ) )
