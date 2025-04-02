from models.solution import Solution
from models.map import Map
from algorithms.functions import crossover_func,mutation_func
from algorithms.randomSolution import randomSolution
import random

# CONSTANTS
POPULATION_SIZE = 10
MUTATION_PROBABILITY = 0.05

def most_fit(m: Map,population: list[Solution]) -> Solution:
  return sorted(population, lambda solution : m.evaluate(solution),reverse=True)[0]


def generate_population(m : Map) -> list[Solution]:
  population = []
  for _ in range(POPULATION_SIZE):
    solution = randomSolution(m)
    population.append(solution)
  return population

def genetic_algorithm(m: Map, num_iterations=100) -> Solution:
  population = generate_population(m)
  while(num_iterations > 0):
    # create new children
    new_population = []
    for _ in range(population):
      second_parent = most_fit(m,population)
      first_parent = random.choice(population)
      child = crossover_func(first_parent,second_parent)

      #random mutate
      if(random.random() <= MUTATION_PROBABILITY):
        child = mutation_func(m,child)

      new_population.append(child)
    population = new_population

    num_iterations -= 1
    return most_fit(m,population)
