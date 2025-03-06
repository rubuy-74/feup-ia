<!-- # IART 2024 - Router Placement -->
## Specification of the Problem

## Related Work

## Problem Formulation

#### Solution Representation

+ Array of array containing the path for each router
+ Number of non router cells connected to the backbone (N)
+ Number of routers (M)
+ Number of targeted cells (t)

#### Mutation Function

+ For any router, choose one of the adjacent cells or the router itself that are not in the path to the backbone
+ If there is budget available, place the router in the chosen cell and replace the previous with a cell connecting to the backbone or no cell at all
+ If there is budget available for a new router, it may place that router
+ There is also a possibility of removing a router and its path

#### Crossover Function

+ Divide the number of routers by two and choose the first half for each
+ For a solution A with Ra routers and another solution B with Rb routers, the child C will have Ra/2 + Rb/2 routers

#### Hard Constraints

+ A router must be placed within the boundaries of the grid
+ There is no wall inside the smallest enclosing rectangle of a cell with a router and a cell that is covered
+ Routers can only be connected to a cell that is already connected to the fiber backbone
+ The maximum spend on routers and backbone is B
+ Routers cannot be placed on walls, but the initial backbone cell can be of any type (target,void or wall cell)

#### Evalutation Functions

**score = 1000\*t - (B - (N * Pb + M * Pr))**

t  - number of targeted cells \
B  - budget \
N  - Number of cells connected to backbone \
Pb - price of connecting one cell to the backbone \
M  -  Number of routers connected to backbone \
Pr - price of connecting a router to the backbone 

## Implementation

+ The language which will be used is Python
+ The IDE used will be VScode
+ The version control system is Git with Github

### Data Structures

+ Backbone
+ Map
+ Router
+ Solution
+ Position