# IART 2025 - ROUTER PLACEMENT

## How to Run

Due to the implementation of configuration files, running any map with any algorithm is simpler.

In a configuration file, you can: 
- Set which map and algorithm you want to run.
- Set the probabilites of each operator of the mutation function.
- Set a budget constraint to the naive solution.
- Set the map size inside the GUI.

```yaml
algorithm: <name of the algorithm>
map: <name of the map>
size: 1
seed: <random integer>
probabilities:
  remove: <desired percentage (decimal)>
  add: <desired percentage (decimal)>
  nothing: <desired percentage (decimal)>
constraints:
  budget: <desired percentage (decimal)>
```
Any custom configuration file must be placed inside the <code>configs</code> folder.

It is important to state that the sum of the three probabilities (add, remove and nothing) must add to 1.

To start the program, run on the <code>src</code> directory:

<code>python3 main.py \<config name> </code>

After the command above, a new window will open with the choosen map and the algorithm will start running **indefinetly** (excl. simulated annealing).

To stop the execution, open the map window and press <code>Space</code>. The execution will stop and the last computed solution will be drawn and dumped into a file in the <code>output</code> folder, as well as a plot.



## The Approach
### Heuristics

Heuristics are employed to guide the search for better solutions. Some heuristics that we used to base off our solution are:
+ Coverage Maximization: Prioritize placing routers in positions which maximize the coverage.
+ Minimize Cost: Try to keep routers closer to the backbone to spend less on backbone cells.
+ Avoid walls: Ensure that the router placement algorithm do not position routers within walls, to maintain feasibility.

### Evaluation Function

The evaluation function is used to score potential solutions based on their effectiveness and cost. The function is defined by:

```math
\text{score} = 1000 \cdot t + \left( B - \left( N \cdot P_b + M \cdot P_r \right) \right)
```

t  - number of targeted cells \
B  - budget \
N  - Number of cells connected to backbone \
Pb - price of connecting one cell to the backbone \
M  -  Number of routers connected to backbone \
Pr - price of connecting a router to the backbone 

This function prioritizes the coverage over the price of the final solution. The contribution of the solution cost penalizes excessive resources.

### Operators:

+ **Mutation**: Randomly adjust the placement to explore new solutions.
  + Add: Add a router in a random position if the budget allows
  + Remove: Removes a random router and its associated path until an interception of connections.
+ **Crossover**: Combine two solutions to generate a new one.
  + Chooses a random square in one of the parents and copies all the routers inside of it from that parent to the other. All routers from the second are previously deleted, as their paths.
  + This approach allows the merge of the solutions with a limited amount of calculations for new paths, which simplifies the calculations. 

## Implemented Algorithms 

### Naive Solution

The Naive solution starts by placing a router in a random position that is not yet covered by any other router.

It then connects that router to a backbone connection (which can either be a connected router, a connected cable, or the backbone itself). This connection is calculated using a breadth-first search (BFS), which leverages the main <code>ndarray</code> structure.

After connecting the router, its path is accounted for in the solution budget, and the map's coverage is updated.

At any time, if a router placement or a path creation surpasses the budget, the entire computation is reset, and another iteration starts.

The algorithm continues running while there is still a budget available.

### HillClimb

The HillClimb algorithm starts with an initial solution computed using the naive algorithm.

At each iteration, a mutation is performed on the current solution. The mutation can be one of the following:

+ **Add:** A random router is added, and a BFS is performed to find the shortest path to a connected cell.
+ **Remove:** A random router is removed from the matrix. If the selected router is part of a straight cable, it is replaced by a cable. If it is isolated, its path to a straight cable is removed (using BFS).
+ **Nothing:** The mutation function does nothing to the current solution.
Each operator respects the current remaining budget.

After applying a mutation, the new solution is evaluated against the old one. If the new solution is better, it replaces the old one, and the budget is updated accordingly.

The algorithm continues iterating until the <code>Space</code> key is pressed by the user.

### Simulated Annealing

The Simulated Annealing algorithm starts with an initial solution computed using the naive algorithm. It explores the solution space by applying mutations and uses a probabilistic acceptance criterion to escape local optima.

At each iteration:

A mutation is applied to the current solution, which can add, remove, or do nothing to the placement of routers.

The new solution is evaluated. If it is better than the current solution, it is accepted.
If the new solution is worse, it may still be accepted with a probability proportional to the difference in scores (Δ) and the current temperature (T), calculated as <code>P = exp(Δ / T)</code>. This allows the algorithm to escape local optima.

The temperature decreases over time according to a cooling schedule <code>(T = T * cooling_rate)</code>, and the algorithm stops when the temperature reaches a predefined threshold or until the <code>Space</code> key is pressed by the user.

The algorithm tracks the best solution found during the process and returns it as the final result.

### Genetic Algorithm

The Genetic Algorithm is a population-based optimization technique inspired by natural selection. It starts by creating an initial population of solutions using the naive algorithm (pre-computed for bigger maps).

**Evaluation:** Each individual in the population is evaluated using the scoring function.

**Selection:** A subset of the population is selected as parents based on their fitness scores. A tournament selection process is used to choose the best candidates, creating a pool of 3.

**Crossover:** Pairs of parents are combined to produce a new child solution. A random square region is selected from one parent, and the routers within that region are copied to the other parent. The resulting child inherits characteristics from both parents.

**Mutation:** A mutation function is applied to the child solution, which can add, remove, or do nothing to the placement of routers. This introduces diversity into the population.

**Replacement:** The children replace the old population, and the process repeats.

The algorithm continues iterating until the <code>Space</code> key is pressed by the user. The best solution found during the process is returned as the final result.

## Parameterizations

The comparison between all the algorithms was made with two different parameterizations, both present in the already created configuration files:

```yaml
add: 0.6
remove: 0.2
nothing: 0.2
time: ~60s
```

and

```yaml
add: 0.5
remove: 0.3
nothing: 0.2
time: ~60s
```

Although not very different from one another, each parameterization changed significantly the behaviour of the algorithms, as stated in the plots.

Different budget constraints were also used, varying from map to map and algorithm to algorithm, but always between [0, 0.5, 0.7].

## Specification of the Problem

Typically, buildings are connected to the Internet using a fiber backbone. In order to provide wireless Internet access, wireless routers are placed around the building and connected using fiber cables to the backbone.

Given a building plan, the objective is to decide where to put wireless routers and how to connect them to the fiber backbone to maximize coverage and minimize cost (not surpassing the budget).

### Constraints

The problem is represented as a grid, where each cell can be either a wall cell, a target cell or a void cell. Target cells are cells in which we need to have wireless coverage and the void cells don't need to be covered.

Routers have a limited range and cannot be placed in wall cells. Backbones in the other hand can be placed anywhere on the grid.

### Solution Representation

+ A matrix representing the map. Each entry has a type, possibly being <code>[BACKBONE, VOID, WALL, TARGET, WIRED, ROUTER, CONNECTED_ROUTER, CABLE]</code>.
+ Score of the solution, computed using the formula above
+ Time spent on the algorithm execution
  + In the execution of the algorithms that need a initial solution, its computation time was not taking into account.
+ Number of iterations

### Data Structures

+ Matrix <code>[ndarray from numpy]</code>
+ Cell

## Related Work

These are related research and solutions to the problem at hand:

+ Principled Modeling of the Google Hash Code Problems for Meta-Heuristics
  + https://estudogeral.uc.pt/retrieve/265403/tese_final_pedro_rodrigues.pdf
+ Genetic algorithms and greedy-randomized adaptive search procedure for router placement problem in wireless networks
  + https://journals.sagepub.com/doi/full/10.3233/JHS-190616
+ Teams Gyrating Flibbittygibbitts solution
  + https://github.com/sbrodehl/HashCode
