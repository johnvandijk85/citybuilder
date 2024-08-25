import pygame
import time

# Initialize Pygame
pygame.init()

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# --- Building Colors ---
BUILDING_COLORS = {
    "House": GREEN,
    "Store": RED,
    "Office": BLUE,
    "Factory": YELLOW,
}

# --- Building Class ---
class Building:
    def __init__(self, name, cost, tax_revenue):
        self.name = name
        self.cost = cost
        self.tax_revenue = tax_revenue

# --- City Class ---
class City:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.map = [[' ' for _ in range(width)] for _ in range(height)]
        self.money = 1000
        self.screen = screen  # Pygame screen

    def display_map(self):
        tile_size = 20  # Size of each tile on the map
        for y in range(self.height):
            for x in range(self.width):
                cell = self.map[y][x]
                rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
                if cell != ' ':
                    color = BUILDING_COLORS.get(
                        next((b.name for b in building_types if b.name[0] == cell), None),
                        WHITE  # Default color if not found
                    )
                    pygame.draw.rect(self.screen, color, rect)
                else:
                    pygame.draw.rect(self.screen, WHITE, rect, 1)  # Draw white grid

    def build(self, building, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            print("Invalid coordinates.")
            return

        if self.map[y][x] != ' ':
            print("Space already occupied.")
            return

        if self.money < building.cost:
            print("Not enough money.")
            return

        self.map[y][x] = building.name[0]  # Use first letter of name as symbol
        self.money -= building.cost
        print(f"{building.name} built at ({x}, {y}).")

    def collect_taxes(self):
        """Collects taxes from all buildings."""
        total_taxes = 0
        for y in range(self.height):
            for x in range(self.width):
                cell = self.map[y][x]
                if cell != ' ':
                    for building_type in building_types:
                        if building_type.name[0] == cell:
                            total_taxes += building_type.tax_revenue
                            break
        self.money += total_taxes
        print(f"Collected ${total_taxes} in taxes.")

# --- Building Types ---
building_types = [
    Building("House", 100, 10),
    Building("Store", 200, 20),
    Building("Office", 300, 30),
    Building("Factory", 400, 40),
]

# --- Pygame Setup ---
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("City Builder")

# --- Create City ---
city = City(20, 15, screen)

# --- Calendar Variables ---
start_time = time.time()
month = 1
year = 1

# --- Building Selection Variables ---
selected_building_type = None

# --- Game Loop ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid_x = x // 20
            grid_y = y // 20

            # Building Selection
            if y < 50:  # Top 50 pixels reserved for building selection
                for i, building_type in enumerate(building_types):
                    if i * 100 <= x < (i + 1) * 100:
                        selected_building_type = building_type
                        break
            else:  # Building Placement
                if selected_building_type is not None:
                    city.build(selected_building_type, grid_x, grid_y)
                    selected_building_type = None  # Reset after building

    # --- Calendar Logic ---
    elapsed_time = time.time() - start_time
    if elapsed_time >= 10:  # New month every 10 seconds
        month += 1
        start_time = time.time()
        if month > 12:
            month = 1
            year += 1
            # Collect annual taxes
            city.collect_taxes()
            print(f"--- Year {year} ---")

    # --- Display Calendar ---
    font = pygame.font.Font(None, 30)
    calendar_text = font.render(f"Month: {month}, Year: {year}", True, WHITE)
    screen.blit(calendar_text, (10, 10))

    # --- Display Building Selection ---
    for i, building_type in enumerate(building_types):
        rect = pygame.Rect(i * 100, 0, 100, 50)
        pygame.draw.rect(screen, BUILDING_COLORS[building_type.name], rect)
        text = font.render(building_type.name, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    # --- Drawing ---
    screen.fill(BLACK)  # Clear the screen
    city.display_map()
    pygame.display.flip()  # Update the display

pygame.quit()