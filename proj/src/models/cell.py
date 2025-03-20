class Cell:
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y
  
  def __str__(self):
    return "(" + str(self.x) + "," + str(self.y) + ")"
  
  def __repr__(self):
    return str(self)
  
  def __eq__(self, other):
    if isinstance(other, Cell):
        return self.x == other.x and self.y == other.y
    return False
  
  def __hash__(self):
    return hash((self.x, self.y))

  def adjacents(self) -> list:
    adjXpos = self.x + 1
    adjXneg = self.x - 1
    adjYpos = self.y + 1
    adjYneg = self.y - 1

    # adjacent cells in clockwise order starting from top-left corner
    return [
        Cell(adjXneg, adjYneg),
        Cell(self.x, adjYneg),
        Cell(adjXpos, adjYneg), 
        Cell(adjXpos, self.y), 
        Cell(adjXpos, adjYpos), 
        Cell(self.x, adjYpos), 
        Cell(adjXneg, adjYpos), 
        Cell(adjXneg, self.y)
      ]