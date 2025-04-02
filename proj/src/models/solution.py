import utils as utils

class Solution:
  def __init__(self, backbone_cells: dict, routers: set):
    self.routers = routers
    self.backbone_cells = backbone_cells

  def __str__(self):
    return f"[{str(self.routers)},{str(self.backbone_cells)}]"

  def computeCoverage(self):
    coverage = set()
    for r in self.routers:
        coverage.update(r.coverage)
    return coverage
  
  def getBackboneCellsInSet(self):
    # return all backbone cells and also the routers, as they can serve as connections as well
    result = utils.convertDictToSet(self.backbone_cells)
    result.update({r.cell for r in self.routers})
    return result 
