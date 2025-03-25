import sys
import pygame
import ctypes
import utils as utils
import algorithms.randomSolution as randomSolution
import algorithms.greedySolution as greedySolution
import models.solution as solution
import models.cell as cell
import models.map as mapClass
import models.router as router
import math
import yaml
import time



def draw_pixel(screen, x, y, color, size):
    pygame.draw.rect(screen, color, (x*size, y*size, size, size))


def draw_map(screen, m: mapClass.Map, size):
  void = (255, 255, 255)
  wall = (128, 128, 128)
  target = (255, 255, 0)

  for i in m.walls:
    draw_pixel(screen, i.x, i.y, wall, size)
  for i in m.voids:
    draw_pixel(screen, i.x, i.y, void, size)
  for i in m.targets:
    draw_pixel(screen, i.x, i.y, target, size)
  pygame.display.flip()
  print("Map Drawn")


def draw_solution(screen, m: mapClass.Map, sol: solution.Solution, size):
  void = (255, 255, 255)
  wall = (128, 128, 128)
  target = (255, 255, 0)
  target_router = (0, 255, 0)
  backbone = (255, 0, 0)
  router = (0, 0, 255)
  targets = sol.getTargets()
  routerCells = list(map(lambda router: router.cell, sol.routers))
  print("Screen Blackout")
  screen.fill((0, 0, 0))
  print("Drawing")

  
  bb_cells = set(path for paths in sol.paths.values() for path in paths)

  for t in m.targets:
    draw_pixel(screen, t.x, t.y, target, size)
  for n in targets:
    draw_pixel(screen, n.x, n.y, target_router, size)
  for w in m.walls:
    draw_pixel(screen, w.x, w.y, wall, size)
  for v in m.voids:
    draw_pixel(screen, v.x, v.y, void, size)
  for w in bb_cells:
    draw_pixel(screen, w.x, w.y, (157, 0, 255), size)
  for r in routerCells:
    draw_pixel(screen, r.x, r.y, router, size)

  draw_pixel(screen, m.backbone.cell.x, m.backbone.cell.y, backbone, size)

  pygame.display.flip()


def load_config(config_file):
  with open(config_file) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
  
  print(config)
  return config
  

def main():
  pygame.init()

  m : mapClass.Map

  # Define the states and texts of the game
  state = 'MENU'
  title_text = 'Hello, choose the config!'
  texts = ['Simple Example', 'Charleston Road', 'Lets Go Higher', 'Opera', 'Rue De Londres']
  file_options = ['example.in', 'charleston_road.in', 'lets_go_higher.in', 'opera.in', 'rue_de_londres.in']
  algorithms = ['Random', 'Greedy', 'Hill Climbing', 'Simulated Annealing', 'Tabu Search', 'Genetic Algorithm']
  algorithms_config = ['random', 'greedy', 'hill_climbing', 'simulated_annealing', 'tabu_search', 'genetic_algorithm']

  # Loads the default config with the seed set to the current time in nanoseconds
  config = load_config('configs/default.yaml')
  config['seed'] = int(time.time()*1e9)




  # Initialize the choice variables
  choice_config = 0
  choice_map = 0
  choice_alg = 0

  # Load the config file if it is passed as an argument
  if len(sys.argv) > 1:
        config = load_config("configs/" +sys.argv[1])
        state = 'ALGORITHM'


  # Define the options for the game screen
  font = pygame.font.SysFont(None, 55)
  screen = pygame.display.set_mode((1000, 900))
  pygame.display.set_caption('Router Placement')
  hwnd = pygame.display.get_wm_info()['window']


  # Create the title
  title = font.render(title_text, True, (255, 255, 255))

  # Run the program loop
  running = True
  while running:
    for event in pygame.event.get():
      if state == 'MENU':
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False
          elif event.key == pygame.K_DOWN:
            choice_map = (choice_map + 1) % len(texts)
          elif event.key == pygame.K_UP:
            choice_map = (choice_map - 1) % len(texts)
          elif event.key == pygame.K_RETURN:
            pygame.display.set_caption('Router Placement - ' + texts[choice_map])
            if(choice_map == 0):
              config['size'] = 30
            elif choice_map == 1:
             config['size'] = 2
            else:
              config['size'] = 1
            config['map'] = "../maps/" + file_options[choice_map]
            state = 'ALGCHOICE'
      elif state == 'ALGCHOICE':
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            state = 'MENU'
          elif event.key == pygame.K_DOWN:
            choice_alg = (choice_alg + 1) % len(algorithms)
          elif event.key == pygame.K_UP:
            choice_alg = (choice_alg - 1) % len(algorithms)
          elif event.key == pygame.K_RETURN:
            pygame.display.set_caption('Router Placement - ' + texts[choice_map] + ' - ' +algorithms[choice_alg])
            config['algorithm'] = algorithms_config[choice_alg]
            screen.fill((0, 0, 0))
            pygame.display.flip()
            state = 'ALGORITHM'
      elif state == 'ALGORITHM':
        m = utils.parse("../maps/"+config['map'])
        screen.fill((0, 0, 0))

        if(config['algorithm'] == 'random'):
          print("Random")
          draw_map(screen, m, config['size'])
          sol = randomSolution.randomSolution(m, config['seed'])
          print(sol)
          print(m.evaluate(sol))
          screen.fill((0, 0, 0))

          draw_solution(screen, m, sol, config['size'])

          state = 'FROZEN'
          print("Done")
        elif(config['algorithm'] == 'greedy'):
          print("Greedy")
          draw_map(screen, m, config['size'])
          sol = greedySolution.greedySolution(m)
          print(sol)
          print(m.evaluate(sol))
          screen.fill((0, 0, 0))

          draw_solution(screen, m, sol, config['size'])

          state = 'FROZEN'
          print("Done")
        else:
          state = 'NOT_IMPLEMENTED'
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            running = False
          elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
              running = False
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            running = False
          elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
              running = False
      elif state == 'NOT_IMPLEMENTED':
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            state = 'ALGCHOICE'
      elif state == 'FROZEN':
        if event.type == pygame.QUIT:
          running = False
        elif event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False

    if state == 'MENU':
        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the title on the screen
        screen.blit(title, (10, 50))

        # Draw the options on the screen
        y = 150
        for i, text in enumerate(texts):
            color = (255, 255, 255) if i != choice_map else (255, 0, 0)
            rendered_text = font.render(text, True, color)
            screen.blit(rendered_text, (10, y))
            y += 60  # Adjust the y position for the next text

        # Update the display

    elif state == 'ALGCHOICE':
        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the title on the screen
        screen.blit(title, (10, 50))

        # Draw the options on the screen
        y = 150
        for i, text in enumerate(algorithms):
            color = (255, 255, 255) if i != choice_alg else (255, 0, 0)
            rendered_text = font.render(text, True, color)
            screen.blit(rendered_text, (10, y))
            y += 60  # Adjust the y position for the next text

        # Update the display
    
    elif state == 'NOT_IMPLEMENTED':
      screen.fill((0, 0, 0))
      text = font.render('Not implemented yet', True, (255, 0, 0))
      screen.blit(text, (10, 50))



    elif state == 'FROZEN':
      continue

    elif state == 'LOADCONFIG':
      print("Loading config")
      filename = 'configs/'
      if choice_config == 0:
        filename += 'default.yaml'
      elif choice_config == 1:
        filename += 'custom.yaml'
      else:
        filename += 'config'+str(choice_config-1)+'.yaml'
      config = load_config(filename)
      state = 'ALGORITHM'
    
    pygame.display.flip()

        


  

if __name__ == "__main__":
  main()
