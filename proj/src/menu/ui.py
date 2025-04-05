import pygame

def display(screen, state, title, font, texts, choice_map, algorithms, choice_alg, seed_input):
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
    
    elif state == 'NOT_IMPLEMENTED':
      screen.fill((0, 0, 0))
      text = font.render('Not implemented yet', True, (255, 0, 0))
      screen.blit(text, (10, 50))

    elif state == 'SEED':
        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the seed input box
        seed_text = font.render('Enter seed:', True, (255, 255, 255))
        screen.blit(seed_text, (10, 150))

        # Draw the seed input
        seed_input = font.render(seed_input, True, (255, 255, 255))
        screen.blit(seed_input, (10, 200))

    
    pygame.display.flip()