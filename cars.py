import pygame, sys, random

def draw_road():
    screen.blit(road_surface, (road_x_pos, 0))  # The road takes up the whole screen
    screen.blit(road_surface, (road_x_pos + 1600, 0))  # Loop the road

def create_obstacle():
    random_lane = random.choice(lane_positions)
    obstacle = obstacle_surface.get_rect(midbottom=(random.randint(1700, 1900), random_lane))  # Spawn offscreen
    return obstacle

def move_obstacles(obstacles):
    global score
    for obstacle in obstacles:
        obstacle.centerx -= obstacle_speed  # Move obstacles left with variable speed
    visible_obstacles = []
    for obstacle in obstacles:
        if obstacle.right > -50:
            visible_obstacles.append(obstacle)
        else:
            score += 1  # Increase score by 1 when an obstacle moves offscreen
    return visible_obstacles

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        screen.blit(obstacle_surface, obstacle)

def check_collision(obstacles):
    for obstacle in obstacles:
        if car_rect.colliderect(obstacle):
            crash_sound.play()
            return False
    return True

def car_movement():
    global car_movement_direction, car_movement_angle
    
    car_movement_direction = 0  # Reset direction before checking input
    
    if keys[pygame.K_UP] and car_rect.top > 150:  # Restrict movement to stay above the top non-playable area
        car_rect.centery -= 10
        car_movement_direction = -1  # Moving up
    if keys[pygame.K_DOWN] and car_rect.bottom < 750:  # Restrict movement to stay below the bottom non-playable area
        car_rect.centery += 10
        car_movement_direction = 1  # Moving down

def rotate_car():
    global car_surface_rotated, car_movement_angle
    
    if car_movement_direction == -1:  # Car is moving up
        car_movement_angle = max(car_movement_angle - 1, -10)  # Tilt up to -10 degrees
    elif car_movement_direction == 1:  # Car is moving down
        car_movement_angle = min(car_movement_angle + 1, 10)  # Tilt down to 10 degrees
    else:
        if car_movement_angle > 0:
            car_movement_angle -= 1  # Gradually return to horizontal position
        elif car_movement_angle < 0:
            car_movement_angle += 1

    # Rotate the car image based on the movement angle
    car_surface_rotated = pygame.transform.rotozoom(car_surface, -car_movement_angle, 1)  # Rotate the car sprite

def display_score():
    score_surface = game_font.render(f'Score: {score}', True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(800, 50))
    screen.blit(score_surface, score_rect)

def display_game_over():
    game_over_surface = game_font.render('Game Over! Press Enter to Restart', True, (255, 255, 255))
    game_over_rect = game_over_surface.get_rect(center=(800, 450))
    screen.blit(game_over_surface, game_over_rect)

def display_start_screen():
    start_surface = game_font.render('Press Enter to Start', True, (255, 255, 255))
    start_rect = start_surface.get_rect(center=(800, 450))
    screen.blit(start_surface, start_rect)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1600, 900))  # Screen size: 1600x900
clock = pygame.time.Clock()
game_font = pygame.font.Font('freesansbold.ttf', 40)  # Font for displaying score and game over text

# Load road background
road_surface = pygame.image.load('assets/road.png').convert()
road_surface = pygame.transform.scale(road_surface, (1600, 900))  # Road image will now take up the entire screen
road_x_pos = 0

# Load player car (120x60 pixels)
car_surface = pygame.image.load('assets/player_car.png').convert_alpha()
car_surface = pygame.transform.scale(car_surface, (120, 60))  # Adjust player car size to 120x60
car_rect = car_surface.get_rect(center=(200, 450))  # Center the car on the road

# Rotation variables
car_surface_rotated = car_surface
car_movement_angle = 0  # Initial angle is 0 (no rotation)
car_movement_direction = 0  # -1 for up, 1 for down, 0 for no vertical movement

# Load obstacle cars (120x60 pixels)
obstacle_surface = pygame.image.load('assets/obstacle_car.png').convert_alpha()
obstacle_surface = pygame.transform.scale(obstacle_surface, (120, 60))  # Adjust obstacle car size to 120x60
obstacle_list = []
SPAWN_OBSTACLE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_OBSTACLE, 1200)

# Lanes (evenly spaced in the 600-pixel road area)
lane_positions = [250, 350, 450, 550, 650]  # Lanes from y=150 to y=750

# Load sounds
crash_sound = pygame.mixer.Sound('sound/crash.wav')
honk_sound = pygame.mixer.Sound('sound/honk.wav')
pygame.mixer.music.load('sound/background_music.wav')
pygame.mixer.music.play(-1)  # Play background music in a loop

# Game variables
game_active = False  # Start with the start screen
keys = pygame.key.get_pressed()
score = 0
obstacle_speed = 5  # Initial speed of obstacles

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if not game_active:  # Start the game from the start screen or after game over
                    game_active = True
                    obstacle_list.clear()
                    car_rect.center = (200, 450)  # Reset car position to the middle lane
                    score = 0  # Reset score
                    obstacle_speed = 5  # Reset speed

            if event.key == pygame.K_h:  # Honk when the 'H' key is pressed
                honk_sound.play()

        if event.type == SPAWN_OBSTACLE and game_active:
            obstacle_list.append(create_obstacle())

    keys = pygame.key.get_pressed()

    if game_active:
        # Move road and obstacles
        road_x_pos -= obstacle_speed  # Speed increases with score
        draw_road()
        if road_x_pos <= -1600:  # Loop the road
            road_x_pos = 0

        # Player car movement
        car_movement()

        # Rotate the car based on its movement
        rotate_car()
        screen.blit(car_surface_rotated, car_rect)

        # Obstacle movement
        obstacle_list = move_obstacles(obstacle_list)
        draw_obstacles(obstacle_list)

        # Check for collisions
        game_active = check_collision(obstacle_list)

        # Display score
        display_score()

        # Gradually increase obstacle speed as the score increases, but slower
        obstacle_speed = 5 + score // 20  # Slower speed increase every 20 points

    else:
        if score == 0:
            # Display start screen
            display_start_screen()
        else:
            # Display game over screen
            display_game_over()

    pygame.display.update()
    clock.tick(120)
