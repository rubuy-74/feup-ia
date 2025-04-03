import pygame

from models.solution import Solution

def draw_pixel(screen, x, y, color, size):
    pygame.draw.rect(screen, color, (x * size, y * size, size, size))

def draw_map(screen, m, size):
    colors = {
        'void': (255, 255, 255),
        'wall': (128, 128, 128),
        'target': (255, 255, 0),
    }

    for cell in m.walls:
        draw_pixel(screen, cell.x, cell.y, colors['wall'], size)
    for cell in m.voids:
        draw_pixel(screen, cell.x, cell.y, colors['void'], size)
    for cell in m.targets:
        draw_pixel(screen, cell.x, cell.y, colors['target'], size)
    
    pygame.display.flip()

def draw_solution(screen, m, sol: Solution, size):
    colors = {
        'target_router': (0, 255, 0),
        'backbone': (255, 0, 0),
        'router': (0, 0, 255),
        'path': (157, 0, 255),
    }

    for cell in sol.computeCoverage():
        draw_pixel(screen, cell.x, cell.y, colors['target_router'], size)
    for cell in m.walls:
        draw_pixel(screen, cell.x, cell.y, (128, 128, 128), size)
    for path in sol.backbone_cells.values():
        for cell in path:
            draw_pixel(screen, cell.x, cell.y, colors['path'], size)
    for cell in sol.routers:
        draw_pixel(screen, cell.cell.x, cell.cell.y, colors['router'], size)
    
    draw_pixel(screen, m.backbone.cell.x, m.backbone.cell.y, colors['backbone'], size)
    pygame.display.flip()
