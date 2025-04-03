from models.map import Map
from models.cell import Cell
from algorithms.naive import connect_to_backbone
import random

def add(m: Map, current_budget: int):
   if current_budget + m.rtPrice > m.budget:
      return m, current_budget
   
   for _ in range(50):
      x = random.randint(0, m.rows - 1)
      y = random.randint(0, m.columns - 1)
      
      if isValid(m, (x, y)):
         type_of_cell_before = m.matrix[x, y]
         m.matrix[x, y] = Cell.ROUTER
         
         temp, passed_budget, cost = connect_to_backbone(m, (x, y), current_budget)
      
         if not passed_budget:
            m.matrix[x, y] = type_of_cell_before
            continue
         
         return temp, current_budget - cost
   
   return m, current_budget
      

def isValid(m: Map, coords: tuple):
   return not m.isBackBone(coords) and not m.isRouter(coords) and not m.isWall(coords) and not m.isVoid(coords) and not m.isCable(coords)