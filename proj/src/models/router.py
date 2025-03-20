import models.cell as cell
import utils as utils

class Router:
  def __init__(self, cell, range_, cost, map):
    self.cell = cell
    self.range_ = range_
    self.cost = cost
    self.targets = utils.getTargets(cell,map) 

  def __str__(self):
    return "[" + str(self.cell) + ", " + str(self.cost) + ", " + str(self.range_) + "]"

  def __repr__(self):
    return str(self)  
  
  def __eq__(self, other):
    if isinstance(other, Router):
        return self.cell == other.cell
    return False
  
  def __hash__(self):
    return hash((self.cell, self.range_, self.cost))
