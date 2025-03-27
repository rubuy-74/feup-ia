import utils as utils
import models.router as router

class Solution:
  def __init__(self, backbone_cells: dict, routers: set):
    self.routers = routers
    self.backbone_cells = convertDictToSet(backbone_cells)

  def __str__(self):
    return f"[{str(self.routers)},{str(self.backbone_cells)}]"

  def computeCoverage(self):
    coverage = set()
    for r in self.routers:
        coverage.update(r.cov)
    return coverage

def convertDictToSet(d):
  result = set()
  
  for item in d.values():
    result.update(item)

  return result