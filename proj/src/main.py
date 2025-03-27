import sys
import pygame
import ctypes
import utils as utils
import algorithms.randomSolution as randomSolution
import algorithms.greedySolution as greedySolution
import algorithms.hillclimb as hillClimb
import models.solution as solution
import models.cell as cell
import models.map as mapClass
import models.router as router
import time

def draw_pixel(screen, x, y, color, size):
    pygame.draw.rect(screen, color, (x*size, y*size, size, size))


def draw_map(screen, m: mapClass.Map, size):
  void = (0, 0, 0)
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

  for t in m.targets:
    draw_pixel(screen, t.x, t.y, target, size)
  for n in targets:
    draw_pixel(screen, n.x, n.y, target_router, size)
  for w in m.walls:
    draw_pixel(screen, w.x, w.y, wall, size)
  for v in m.voids:
    draw_pixel(screen, v.x, v.y, void, size)
  for w in sol.backbone_cells:
    draw_pixel(screen, w.x, w.y, (157, 0, 255), size)
  for r in routerCells:
    draw_pixel(screen, r.x, r.y, router, size)

  draw_pixel(screen, m.backbone.cell.x, m.backbone.cell.y, backbone, size)

  pygame.display.flip()


def main():
  pygame.init()

  out = open("output.txt", "w")

  size = 1

  m : mapClass.Map
  state = 'MENU'
  title_text = 'Hello, choose the file!'
  texts = ['Simple Example', 'Charleston Road', 'Lets Go Higher', 'Opera', 'Rue De Londres']
  file_options = ['example.in', 'charleston_road.in', 'lets_go_higher.in', 'opera.in', 'rue_de_londres.in']
  algorithms = ['Random', 'Greedy', 'Hill Climbing', 'Simulated Annealing', 'Tabu Search', 'Genetic Algorithm']






  choice_map = 0

  choice_alg = 0

  font = pygame.font.SysFont(None, 55)

  screen = pygame.display.set_mode((1000, 900))
  pygame.display.set_caption('Router Placement')

  hwnd = pygame.display.get_wm_info()['window']

  # Move the window to the top-left corner
  # ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0, 0)


  title = font.render(title_text, True, (255, 255, 255))

  

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
              size = 30
            elif choice_map == 1:
             size = 2
            else:
              size = 1
            path = "../maps/"+file_options[choice_map]
            m = utils.parse(path)
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
            screen.fill((0, 0, 0))
            draw_map(screen, m, size)
            pygame.display.flip()
            state = 'ALGORITHM'
      elif state == 'ALGORITHM':
        if(choice_alg == 0):
          sol = randomSolution.randomSolution(m)
          
          print(sol)
          print(m.evaluate(sol))

          draw_solution(screen, m, sol, size)
          
          for i in range(500):
            sol = hillClimb.hillclimb(sol, m, 1)
            time.sleep(1)      
            draw_solution(screen, m, sol, size)

          state = 'FROZEN'
          out.close()

        elif(choice_alg == 1):
          draw_map(screen, m, size)
          sol = greedySolution.greedySolution(m)
          print(sol)
          print(m.evaluate(sol))

          draw_solution(screen, m, sol, size)

          for i in range(500):
            sol = hillClimb.hillclimb(sol, m, 1)
                  
            draw_solution(screen, m, sol, size)
          
          
          state = 'FROZEN'
          print("Done")
          out.close()


        else:
          state = 'NOT_IMPLEMENTED'
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

    
    # print(solGreedy)
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
        pygame.display.flip()

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
        pygame.display.flip()
    
    elif state == 'NOT_IMPLEMENTED':
      screen.fill((0, 0, 0))
      text = font.render('Not implemented yet', True, (255, 0, 0))
      screen.blit(text, (10, 50))
      pygame.display.flip()


    elif state == 'FROZEN':
      pygame.display.flip()
          

if __name__ == "__main__":
  main()
