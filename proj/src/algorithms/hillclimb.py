from models.solution import Solution
from models.map import Map
from algorithms.functions import mutation_func

#TODO: Change number of iterations to time
def hillclimb(solution: Solution, m: Map, it: int):
  for _ in range(it):
    new_solution = mutation_func(m,solution)
    new_solution_value = m.evaluate(new_solution)
    solution_value = m.evaluate(solution)

    print(solution_value, new_solution_value)

    # if(new_solution_value >= solution_value):
    solution = new_solution
    m.backbone.connections = solution.backbone_cells
    m.routers = solution.routers

  return solution