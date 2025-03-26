from models.solution import Solution
from models.map import Map
from algorithms.functions import evaluation_func,mutation_func

#TODO: Change number of iterations to time
def hillclimb(solution: Solution, m: Map, it: int):
  for _ in range(it):
    new_solution = mutation_func(m,solution)
    new_solution_value = evaluation_func(m,new_solution)
    solution_value = evaluation_func(m,solution)
    if(new_solution_value >= solution_value):
      solution = new_solution
  return solution