import pygame
import heapq
import random
import os
import time
import pandas as pd

pygame.init()

width, height = 600, 600
tile_size = 30
rows, cols = height // tile_size, width // tile_size
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
navy_blue = (0, 0, 128)  # Navy blue color
green = (0, 255, 0)
FPS = 18

# Game states
STATE_START = 0
STATE_COUNTDOWN = 1
STATE_PLAYING = 2
STATE_GAME_OVER = 3
STATE_PAUSED = 4
STATE_NAME_INPUT = 5

# Initialize screen
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pac-Man Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

score = 0
high_score = 0
start_button_rect = None
countdown_start = 0
countdown_duration = 5
game_state = STATE_NAME_INPUT  # Start with name input
start_time = 0  
survival_time = 0
button_rect = None
level = 1
player_name = ""

# Heuristic function for A*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* Pathfinding
def astar(start, goal, maze):
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]
        
        x, y = current
        neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        
        for neighbor in neighbors:
            nx, ny = neighbor
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] in ["0", "2"]:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return []

# Pac-Man class
class PacMan:
    def __init__(self):
        self.x, self.y = 1, 1
        self.next_dx, self.next_dy = 0, 0
    
    def move(self, maze):
        keys = pygame.key.get_pressed()
        # Use next_dx, next_dy from KEYDOWN if set, otherwise check held keys
        if (self.next_dx, self.next_dy) == (0, 0):
            if keys[pygame.K_UP]:
                self.next_dx, self.next_dy = 0, -1
            elif keys[pygame.K_DOWN]:
                self.next_dx, self.next_dy = 0, 1
            elif keys[pygame.K_LEFT]:
                self.next_dx, self.next_dy = -1, 0
            elif keys[pygame.K_RIGHT]:
                self.next_dx, self.next_dy = 1, 0

        # Attempt to move in the current direction
        new_x, new_y = self.x + self.next_dx, self.y + self.next_dy
        if 0 <= new_x < cols and 0 <= new_y < rows and maze[new_y][new_x] in ["0", "2"]:
            global score
            if maze[new_y][new_x] == "2":
                score += 10
                maze[new_y] = maze[new_y][:new_x] + "0" + maze[new_y][new_x+1:]
            self.x, self.y = new_x, new_y
    
    def draw(self, screen):
        pygame.draw.circle(screen, yellow, (self.x * tile_size + tile_size//2, self.y * tile_size + tile_size//2), tile_size//2 - 2)

# Ghost class
class Ghost:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.path = []
    
    def move(self, pacman, maze):
        if not self.path or random.random() < 0.1:  # Reduced from 0.2
            self.path = astar((self.x, self.y), (pacman.x, pacman.y), maze)
        if self.path:
            self.x, self.y = self.path.pop(0)
    
    def draw(self, screen):
        pygame.draw.circle(screen, red, (self.x * tile_size + tile_size//2, self.y * tile_size + tile_size//2), tile_size//2 - 2)

# Load high score
def load_high_score():
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def save_high_score(score):
    with open("high_score.txt", "w") as f:
        f.write(str(score))

# Save game data to Excel
def save_game_data():
    try:
        data = {
            "PlayerName": [player_name],
            "Score": [score],
            "HighScore": [high_score],
            "SurvivalTime": [survival_time],
            "Level": [level]
        }
        df = pd.DataFrame(data)
        excel_file = "game_data.xlsx"
        if os.path.exists(excel_file):
            with pd.ExcelWriter(excel_file, engine="openpyxl", mode="a", if_sheet_exists="overlay") as writer:
                df.to_excel(writer, sheet_name="GameData", startrow=writer.sheets["GameData"].max_row, index=False, header=False)
        else:
            df.to_excel(excel_file, sheet_name="GameData", index=False)
    except Exception as e:
        print(f"Error saving to Excel: {e}")

# Generate random maze
def generate_maze():
    while True:  # Keep generating until a valid maze is created
        maze = []
        # Step 1: Generate walls and open spaces
        for y in range(rows):
            row = ""
            for x in range(cols):
                if y == 0 or x == 0 or y == rows - 1 or x == cols - 1:
                    row += "1"  # Borders are walls
                else:
                    row += "1" if random.random() < 0.25 else "0"  # 25% chance of inner wall
            maze.append(row)
        
        # Step 2: Place Pac-Man and ghost in open spaces
        maze[1] = maze[1][:1] + "0" + maze[1][2:]  # Pac-Man start at (1, 1)
        maze[rows-2] = maze[rows-2][:cols-2] + "0" + maze[rows-2][cols-1:]  # Ghost start at (cols-2, rows-2)
        
        # Step 3: Place pellets only in open spaces
        for y in range(1, rows-1):
            for x in range(1, cols-1):
                if maze[y][x] == "0" and random.random() < 0.3:  # 30% chance for pellet in open space
                    maze[y] = maze[y][:x] + "2" + maze[y][x+1:]
        
        # checks pacman and ghost are not blocked
        pacman_pos = (1, 1)
        ghost_pos = (cols-2, rows-2)
        def has_adjacent_open(pos):
            x, y = pos
            neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
            for nx, ny in neighbors:
                if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] in ["0", "2"]:
                    return True
            return False
        
        #Check if Pac-Man and ghost have adjacent open tiles and a valid path
        if (has_adjacent_open(pacman_pos) and has_adjacent_open(ghost_pos) and
            astar(pacman_pos, ghost_pos, maze)):  # Ensure a path exists
            return maze
        #if validation fails, loop and generate a new maze

#draw screens (displaying)
def draw_name_input_screen():
    screen.fill(black)
    prompt_text = font.render("Enter Your Name:", True, white)
    name_text = font.render(player_name, True, yellow)
    screen.blit(prompt_text, (width//2 - prompt_text.get_width()//2, height//2 - 50))
    screen.blit(name_text, (width//2 - name_text.get_width()//2, height//2))

def draw_start_screen():
    screen.fill(black)
    title = font.render("Pac-Man Game", True, yellow)
    screen.blit(title, (width//2 - title.get_width()//2, height//2 - 100))
    global start_button_rect
    button_text = font.render("Start Game", True, white)
    start_button_rect = button_text.get_rect(center=(width//2, height//2))
    pygame.draw.rect(screen, blue, start_button_rect.inflate(20, 10), 2)
    screen.blit(button_text, start_button_rect.topleft)

def draw_game_over_screen():
    global button_rect
    screen.fill(black)
    game_over_text = font.render("Game Over!", True, red)
    screen.blit(game_over_text, (width//2 - game_over_text.get_width()//2, height//2 - 100))
    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (width//2 - score_text.get_width()//2, height//2 - 50))
    high_score_text = font.render(f"High Score: {high_score}", True, white)
    screen.blit(high_score_text, (width//2 - high_score_text.get_width()//2, height//2))
    survival_text = font.render(f"Survival Time: {survival_time:.1f}s", True, white)
    screen.blit(survival_text, (width//2 - survival_text.get_width()//2, height//2 + 50))
    play_again = font.render("Play Again", True, white)
    button_rect = play_again.get_rect(center=(width//2, height//2 + 100))
    pygame.draw.rect(screen, blue, button_rect, 2)
    screen.blit(play_again, button_rect.topleft)

def draw_game():
    screen.fill(black)
    for y, row in enumerate(maze):
        for x, col in enumerate(row):
            if col == "1":
                pygame.draw.rect(screen, white, (x * tile_size, y * tile_size, tile_size, tile_size))
            elif col == "2":
                pygame.draw.circle(screen, white, (x * tile_size + tile_size//2, y * tile_size + tile_size//2), 4)
    pacman.draw(screen)
    ghost.draw(screen)
    score_text = font.render(f"Score: {score}  High Score: {high_score}  Level: {level}", True, navy_blue)
    screen.blit(score_text, (10, 10))
    # Display survival time only if start_time is set (i.e., in STATE_PLAYING)
    survival_text = font.render(f"Time: {time.time() - start_time:.1f}s" if start_time > 0 else "Time: 0.0s", True, navy_blue)
    screen.blit(survival_text, (width - survival_text.get_width() - 10, 10))

def draw_countdown():
    remaining = max(0, countdown_duration - int(time.time() - countdown_start))
    draw_game()
    countdown_text = font.render(f"Starting in {remaining}...", True, green)
    screen.blit(countdown_text, (width//2 - countdown_text.get_width()//2, height//2))

def draw_pause_screen():
    screen.fill(black)
    draw_game()
    pause_text = font.render("Paused", True, white)
    screen.blit(pause_text, (width//2 - pause_text.get_width()//2, height//2))

#game loop
maze = generate_maze()
initial_maze = [row[:] for row in maze]
pacman = PacMan()
ghost = Ghost(cols - 2, rows - 2)
high_score = load_high_score()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and game_state == STATE_NAME_INPUT:
            if event.key == pygame.K_RETURN and player_name.strip():
                game_state = STATE_START
            elif event.key == pygame.K_BACKSPACE:
                player_name = player_name[:-1]
            elif event.unicode.isalnum() and len(player_name) < 20:
                player_name += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == STATE_START:
            if start_button_rect and start_button_rect.collidepoint(event.pos):
                game_state = STATE_COUNTDOWN
                countdown_start = time.time()
                start_time = 0  # Reset start time to ensure timer starts at 0.0

        elif event.type == pygame.KEYDOWN and game_state == STATE_PLAYING:
            if event.key == pygame.K_UP:
                pacman.next_dx, pacman.next_dy = 0, -1
            elif event.key == pygame.K_DOWN:
                pacman.next_dx, pacman.next_dy = 0, 1  
            elif event.key == pygame.K_LEFT:
                pacman.next_dx, pacman.next_dy = -1, 0
            elif event.key == pygame.K_RIGHT:
                pacman.next_dx, pacman.next_dy = 1, 0
            elif event.key == pygame.K_ESCAPE:
                game_state = STATE_PAUSED

        elif event.type == pygame.KEYUP and game_state == STATE_PLAYING:
            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                pacman.next_dx, pacman.next_dy = 0, 0

        elif event.type == pygame.KEYDOWN and game_state == STATE_PAUSED:
            if event.key == pygame.K_ESCAPE:
                game_state = STATE_PLAYING

        elif event.type == pygame.MOUSEBUTTONDOWN and game_state == STATE_GAME_OVER:
            if button_rect and button_rect.collidepoint(event.pos):
                save_game_data()  # Save data before restarting
                game_state = STATE_COUNTDOWN
                countdown_start = time.time()
                start_time = 0  # Reset start_time for new game
                level = 1
                score = 0
                pacman = PacMan()
                ghost = Ghost(cols - 2, rows - 2)
                maze = [row[:] for row in initial_maze]

    if game_state == STATE_NAME_INPUT:
        draw_name_input_screen()

    elif game_state == STATE_START:
        draw_start_screen()

    elif game_state == STATE_COUNTDOWN:
        if time.time() - countdown_start >= countdown_duration:
            game_state = STATE_PLAYING
            start_time = time.time()  # Set start_time when gameplay starts
        else:
            draw_countdown()

    elif game_state == STATE_PLAYING:
        pacman.move(maze)
        ghost.move(pacman, maze)
        draw_game()

        if (pacman.x, pacman.y) == (ghost.x, ghost.y):
            game_state = STATE_GAME_OVER
            survival_time = time.time() - start_time
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            save_game_data()

        elif all("2" not in row for row in maze):
            level += 1
            maze = generate_maze()
            initial_maze = [row[:] for row in maze]
            pacman = PacMan()
            ghost = Ghost(cols - 2, rows - 2)

    elif game_state == STATE_GAME_OVER:
        draw_game_over_screen()

    elif game_state == STATE_PAUSED:
        draw_pause_screen()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()