import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple City Builder")

# Create a 2D grid to represent the map
city_map = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Building types
EMPTY = 0
HOUSE = 1
SHOP = 2
FACTORY = 3

# Main game loop
running = True
current_building = HOUSE

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position and convert it to grid coordinates
            mouse_pos = pygame.mouse.get_pos()
            grid_x = mouse_pos[0] // GRID_SIZE
            grid_y = mouse_pos[1] // GRID_SIZE
            
            # Place the current building type on the map
            city_map[grid_y][grid_x] = current_building
        elif event.type == pygame.KEYDOWN:
            # Change the current building type
            if event.key == pygame.K_1:
                current_building = HOUSE
            elif event.key == pygame.K_2:
                current_building = SHOP
            elif event.key == pygame.K_3:
                current_building = FACTORY

    # Clear the screen
    screen.fill(WHITE)

    # Draw the grid and buildings
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            
            if city_map[y][x] == HOUSE:
                pygame.draw.rect(screen, GREEN, rect)
            elif city_map[y][x] == SHOP:
                pygame.draw.rect(screen, BLUE, rect)
            elif city_map[y][x] == FACTORY:
                pygame.draw.rect(screen, RED, rect)

    # Display current building type
    font = pygame.font.Font(None, 36)
    if current_building == HOUSE:
        text = font.render("Current: House (1)", True, BLACK)
    elif current_building == SHOP:
        text = font.render("Current: Shop (2)", True, BLACK)
    else:
        text = font.render("Current: Factory (3)", True, BLACK)
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()