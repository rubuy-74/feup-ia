import utils as utils
import models.router as router

class Solution:
  def __init__(self, backbone_cells: set, routers: set):
    self.routers = routers
    self.backbone_cells = backbone_cells

  def __str__(self):
    return f"[{str(self.routers)},{str(self.backbone_cells)}]"

  def getTargets(self):
    targets = map(lambda router: router.coverage, self.routers)
    return {x for xs in targets for x in xs}
