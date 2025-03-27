from models.solution import Solution
from models.map import Map
from algorithms.functions import mutation_func

#TODO: Change number of iterations to time
def hillclimb(solution: Solution, m: Map, it: int):
  while True:
    new_solution = mutation_func(m,solution)
    new_solution_value = m.evaluate(new_solution)
    solution_value = m.evaluate(solution)

    if(new_solution_value >= solution_value):
      print("New cost:", new_solution_value)
      solution = new_solution
      break
  return solution