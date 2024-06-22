import pygame
import sys
import random

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
YELLOW = (255, 255, 0)

# Building types
EMPTY = 0
HOUSE = 1
SHOP = 2
FACTORY = 3

# Building costs
BUILDING_COSTS = {
    HOUSE: 100,
    SHOP: 200,
    FACTORY: 300
}

# Building income
BUILDING_INCOME = {
    HOUSE: 10,
    SHOP: 20,
    FACTORY: 30
}

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple City Builder")

# Create a 2D grid to represent the map
city_map = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

# Player money
money = 1000

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

            # Check if enough money to build
            if money >= BUILDING_COSTS[current_building]:
                # Place the current building type on the map
                city_map[grid_y][grid_x] = current_building
                money -= BUILDING_COSTS[current_building]
        elif event.type == pygame.KEYDOWN:
            # Change the current building type
            if event.key == pygame.K_1:
                current_building = HOUSE
            elif event.key == pygame.K_2:
                current_building = SHOP
            elif event.key == pygame.K_3:
                current_building = FACTORY

    # Calculate income
    income = 0
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if city_map[y][x] != EMPTY:
                income += BUILDING_INCOME[city_map[y][x]]
    money += income

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

    # Display money
    font = pygame.font.Font(None, 36)
    money_text = font.render(f"Money: ${money}", True, BLACK)
    screen.blit(money_text, (10, 10))

    # Display current building type
    if current_building == HOUSE:
        building_text = font.render("Current: House (1)", True, BLACK)
    elif current_building == SHOP:
        building_text = font.render("Current: Shop (2)", True, BLACK)
    else:
        building_text = font.render("Current: Factory (3)", True, BLACK)
    screen.blit(building_text, (10, 50))

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
