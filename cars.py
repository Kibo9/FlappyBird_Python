import pygame, sys, random

def draw_road():
    screen.blit(road_surface, (road_x_pos, 150))
    screen.blit(road_surface, (road_x_pos + 1600, 150))

def draw_stars():
    screen.blit(stars_top_surface, (stars_top_x_pos, 0))
    screen.blit(stars_top_surface, (stars_top_x_pos + 1600, 0))
    screen.blit(stars_bottom_surface, (stars_bottom_x_pos, 750))
    screen.blit(stars_bottom_surface, (stars_bottom_x_pos + 1600, 750))

def draw_obstacle(occupied_lanes, last_spawn_x):
    available_lanes = [lane for lane in lane_positions if lane not in occupied_lanes]
    
    if len(available_lanes) <= 1:
        return [], last_spawn_x
    
    random_lane = random.choice(available_lanes)
    occupied_lanes.append(random_lane)
    
    if random.random() < 0.2:
        random_truck = random.choice(truck_surfaces)
        trailer_x = random.randint(1700, 1900)
        if trailer_x < last_spawn_x + 200:
            trailer_x = last_spawn_x + 200
        last_spawn_x = trailer_x
        trailer = trailer_surface.get_rect(midbottom=(trailer_x, random_lane))
        truck = random_truck.get_rect(midbottom=(trailer.right + 30, random_lane))
        return [(trailer_surface, trailer), (random_truck, truck)], last_spawn_x
    else:
        random_car = random.choice(obstacle_surfaces)
        car_x = random.randint(1700, 1900)
        if car_x < last_spawn_x + 200:
            car_x = last_spawn_x + 200
        last_spawn_x = car_x
        obstacle = random_car.get_rect(midbottom=(car_x, random_lane))
        return [(random_car, obstacle)], last_spawn_x

def move_obstacles(obstacles):
    global score
    for parts in obstacles:
        for car_surface, obstacle in parts:
            obstacle.centerx -= obstacle_speed
    visible_obstacles = []
    for parts in obstacles:
        parts_visible = []
        for car_surface, obstacle in parts:
            if obstacle.right > -10:
                parts_visible.append((car_surface, obstacle))
        if parts_visible:
            visible_obstacles.append(parts_visible)
        else:
            score += 1
    return visible_obstacles

def draw_obstacles(obstacles):
    for parts in obstacles:
        for car_surface, obstacle in parts:
            screen.blit(car_surface, obstacle)

def check_collision(obstacles):
    for parts in obstacles:
        for car_surface, obstacle in parts:
            if car_rect.colliderect(obstacle):
                crash_sound.play()
                return False
    return True

def car_movement():
    global car_movement_direction, car_movement_angle
    car_movement_direction = 0
    if keys[pygame.K_UP] and car_rect.top > 150:
        car_rect.centery -= 10
        car_movement_direction = -1
    if keys[pygame.K_DOWN] and car_rect.bottom < 750:
        car_rect.centery += 10
        car_movement_direction = 1

def rotate_car():
    global car_surface_rotated, car_movement_angle
    if car_movement_direction == -1:
        car_movement_angle = max(car_movement_angle - 1, -10)
    elif car_movement_direction == 1:
        car_movement_angle = min(car_movement_angle + 1, 10)
    else:
        if car_movement_angle > 0:
            car_movement_angle -= 1
        elif car_movement_angle < 0:
            car_movement_angle += 1

    car_surface_rotated = pygame.transform.rotozoom(car_surface, -car_movement_angle, 1)

def display_score():
    score_surface = game_font.render(f'Score: {score}', True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(800, 50))
    screen.blit(score_surface, score_rect)

def display_game_over():
    game_over_surface = game_font.render('Game Over! Press Enter to Return to Title', True, (255, 255, 255))
    game_over_rect = game_over_surface.get_rect(center=(800, 450))
    screen.blit(game_over_surface, game_over_rect)

def display_start_screen():
        # Draw stars and road on the start screen
    draw_stars()
    draw_road()
    
    # Draw the player car on the start screen
    rotate_car()  # Make sure the car is displayed with its rotation logic
    screen.blit(car_surface_rotated, car_rect)
    
    title_surface = game_font.render('Cosmic Highway', True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(800, 300))
    screen.blit(title_surface, title_rect)

    start_surface = game_font.render('Press Enter to Start', True, (255, 255, 255))
    start_rect = start_surface.get_rect(center=(800, 500))
    screen.blit(start_surface, start_rect)

    high_score_surface = game_font.render(f'High Score: {high_score}', True, (255, 255, 255))
    high_score_rect = high_score_surface.get_rect(center=(800, 400))
    screen.blit(high_score_surface, high_score_rect)

    # New line: Add text for quitting the game
    quit_surface = game_font.render('Press Q to Quit', True, (255, 255, 255))
    quit_rect = quit_surface.get_rect(center=(800, 600))
    screen.blit(quit_surface, quit_rect)

pygame.init()
screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
game_font = pygame.font.Font('Moonstrike-nRqzP.otf', 40)

road_surface = pygame.image.load('assets/road.png').convert()
road_surface = pygame.transform.scale(road_surface, (1600, 600))
road_x_pos = 0

stars_top_surface = pygame.image.load('assets/stars_top.png').convert()
stars_top_surface = pygame.transform.scale(stars_top_surface, (1600, 150))
stars_bottom_surface = pygame.image.load('assets/stars_bottom.png').convert()
stars_bottom_surface = pygame.transform.scale(stars_bottom_surface, (1600, 150))
stars_top_x_pos = 0
stars_bottom_x_pos = 0

car_surface = pygame.image.load('assets/player_car.png').convert_alpha()
car_surface = pygame.transform.scale(car_surface, (120, 60))
car_rect = car_surface.get_rect(center=(200, 450))

car_surface_rotated = car_surface
car_movement_angle = 0
car_movement_direction = 0

obstacle_surfaces = [pygame.image.load(f'assets/{car}.png').convert_alpha() for car in
                     ['compact_blue', 'compact_green', 'compact_orange', 'compact_red',
                      'coupe_midnight', 'coupe_green', 'coupe_blue', 'coupe_red',
                      'sedan_blue', 'sedan_gray', 'sedan_green', 'sedan_red',
                      'sport_blue', 'sport_green', 'sport_red', 'sport_yellow']]
obstacle_surfaces = [pygame.transform.scale(car, (120, 60)) for car in obstacle_surfaces]

truck_surfaces = [pygame.image.load(f'assets/truck_{color}.png').convert_alpha() for color in
                  ['blue', 'cream', 'green', 'red']]
truck_surfaces = [pygame.transform.scale(truck, (60, 60)) for truck in truck_surfaces]

trailer_surface = pygame.image.load('assets/trailer.png').convert_alpha()
trailer_surface = pygame.transform.scale(trailer_surface, (240, 60))

obstacle_list = []
SPAWN_OBSTACLE = pygame.USEREVENT
pygame.time.set_timer(SPAWN_OBSTACLE, 1200)

lane_positions = [230, 330, 430, 530, 630, 730]

crash_sound = pygame.mixer.Sound('sound/crash.mp3')
honk_sound = pygame.mixer.Sound('sound/honk.wav')
pygame.mixer.music.load('sound/background_music.wav')
pygame.mixer.music.play(-1)

game_active = False
on_game_over_screen = False
keys = pygame.key.get_pressed()
score = 0
high_score = 0
obstacle_speed = 5

# New variables for increasing obstacles and speed
max_obstacles = 1
obstacle_increase_threshold = 5
max_obstacles_cap = 7

# Initialize road speed
road_speed = 6

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if on_game_over_screen:
                    on_game_over_screen = False
                    game_active = False
                elif not game_active:
                    game_active = True
                    obstacle_list.clear()
                    car_rect.center = (200, 450)
                    score = 0
                    obstacle_speed = 7
                    max_obstacles = 1

                    # Reset obstacle increase threshold to 10 on every restart
                    obstacle_increase_threshold = 10  # Reset the threshold to 10 for each new game

             # Quit the game if "Q" is pressed
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_h:
                honk_sound.play()

        if event.type == SPAWN_OBSTACLE and game_active:
            occupied_lanes = []
            last_spawn_x = 1700
            for _ in range(max_obstacles):
                new_obstacle, last_spawn_x = draw_obstacle(occupied_lanes, last_spawn_x)
                if new_obstacle:
                    obstacle_list.append(new_obstacle)

    keys = pygame.key.get_pressed()

    # Update road speed based on obstacle speed
    road_speed = obstacle_speed + 2

    # Move road with dynamic speed
    road_x_pos -= road_speed
    stars_top_x_pos -= 1
    stars_bottom_x_pos -= 1

    if road_x_pos <= -1600:
        road_x_pos = 0
    if stars_top_x_pos <= -1600:
        stars_top_x_pos = 0
    if stars_bottom_x_pos <= -1600:
        stars_bottom_x_pos = 0

    screen.fill((0, 0, 0))

    if game_active:
        # Increase max obstacles based on score
        if score >= obstacle_increase_threshold and max_obstacles < max_obstacles_cap:
            obstacle_increase_threshold += 5
            max_obstacles += 1
            obstacle_speed += 1

        draw_stars()
        draw_road()

        car_movement()
        rotate_car()
        screen.blit(car_surface_rotated, car_rect)

        obstacle_list = move_obstacles(obstacle_list)
        draw_obstacles(obstacle_list)
        game_active = check_collision(obstacle_list)

        display_score()

        # Increase player car speed with score
        obstacle_speed = 7 + score // 5

        # Increase the number of obstacles every 5 points, with a cap
        if score // obstacle_increase_threshold >= max_obstacles and max_obstacles < max_obstacles_cap:
            max_obstacles += 1

        if not game_active:
            on_game_over_screen = True
            if score > high_score:
                high_score = score

    elif on_game_over_screen:
        display_game_over()
        if score > high_score:
            high_score = score
    else:
        display_start_screen()

    pygame.display.update()
    clock.tick(60)
