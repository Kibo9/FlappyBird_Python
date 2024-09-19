import pygame, sys, random 

def draw_road():
    screen.blit(road_surface, (road_x_pos, 150))  # The road is now vertically centered, starting at y=150
    screen.blit(road_surface, (road_x_pos + 1600, 150))  # Repeat for smooth scrolling

def create_obstacle():
    random_lane = random.choice(lane_positions)
    obstacle = obstacle_surface.get_rect(midbottom=(random.randint(1700, 1900), random_lane))  # Offscreen spawn
    return obstacle

def move_obstacles(obstacles):
    for obstacle in obstacles:
        obstacle.centerx -= 5  # Move obstacles left
    visible_obstacles = [obstacle for obstacle in obstacles if obstacle.right > -50]  # Remove offscreen obstacles
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
    if keys[pygame.K_UP] and car_rect.top > 150:  # Top limit (150)
        car_rect.centery -= 10
    if keys[pygame.K_DOWN] and car_rect.bottom < 750:  # Bottom limit (750)
        car_rect.centery += 10

pygame.init()
screen = pygame.display.set_mode((1600, 900))  # New screen size: 1600x900
clock = pygame.time.Clock()

# Load road background
road_surface = pygame.image.load('assets/road.png').convert()
road_surface = pygame.transform.scale(road_surface, (1600, 600))  # Road size: 1600x600, fits in the middle
road_x_pos = 0

# Load player car
car_surface = pygame.image.load('assets/player_car.png').convert_alpha()
car_surface = pygame.transform.scale(car_surface, (80, 160))  # Adjust car size to fit new proportions
car_rect = car_surface.get_rect(center=(200, 450))  # Center the car on the road

# Load obstacle cars
obstacle_surface = pygame.image.load('assets/obstacle_car.png').convert_alpha()
obstacle_surface = pygame.transform.scale(obstacle_surface, (80, 160))  # Adjust obstacle car size
obstacle_list = []
SPAWN_OBSTACLE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_OBSTACLE, 1200)

# Lanes (evenly spaced in the 600-pixel road area)
lane_positions = [250, 350, 450, 550, 650]  # Lanes from y=150 to y=750

# Load sounds
crash_sound = pygame.mixer.Sound('sound/crash.wav')

# Game variables
game_active = True
keys = pygame.key.get_pressed()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and game_active == False:
            game_active = True
            obstacle_list.clear()
            car_rect.center = (200, 450)  # Reset car position to the middle lane

        if event.type == SPAWN_OBSTACLE:
            obstacle_list.append(create_obstacle())

    keys = pygame.key.get_pressed()

    if game_active:
        # Move road and obstacles
        road_x_pos -= 5  # Adjust speed
        draw_road()
        if road_x_pos <= -1600:  # Loop the road
            road_x_pos = 0

        # Player car movement
        car_movement()
        screen.blit(car_surface, car_rect)

        # Obstacle movement
        obstacle_list = move_obstacles(obstacle_list)
        draw_obstacles(obstacle_list)

        # Check for collisions
        game_active = check_collision(obstacle_list)

    pygame.display.update()
    clock.tick(120)

