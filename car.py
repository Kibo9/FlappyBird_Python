import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
CAR_START_POSITION = (200, 450)
LANE_POSITIONS = [230, 330, 430, 530, 630, 730]
OBSTACLE_SPEED_INCREMENT = 5

class CosmicHighway:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.Font('Moonstrike-nRqzP.otf', 40)

        # Load assets
        self.load_assets()

        self.reset_game()

    def load_assets(self):
        self.road_surface = pygame.image.load('assets/road.png').convert()
        self.road_surface = pygame.transform.scale(self.road_surface, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.car_surface = pygame.image.load('assets/player_car.png').convert_alpha()
        self.car_surface = pygame.transform.scale(self.car_surface, (120, 60))
        
        # Load obstacle images
        self.obstacle_surfaces = [pygame.image.load(f'assets/{car}.png').convert_alpha() for car in
                                  ['compact_blue', 'compact_green', 'compact_orange', 'compact_red',
                                   'coupe_midnight', 'coupe_green', 'coupe_blue', 'coupe_red',
                                   'sedan_blue', 'sedan_gray', 'sedan_green', 'sedan_red',
                                   'sport_blue', 'sport_green', 'sport_red', 'sport_yellow']]
        self.obstacle_surfaces = [pygame.transform.scale(car, (120, 60)) for car in self.obstacle_surfaces]
        
        self.truck_surfaces = [pygame.image.load(f'assets/truck_{color}.png').convert_alpha() for color in
                               ['blue', 'cream', 'green', 'red']]
        self.truck_surfaces = [pygame.transform.scale(truck, (60, 60)) for truck in self.truck_surfaces]
        
        self.trailer_surface = pygame.image.load('assets/trailer.png').convert_alpha()
        self.trailer_surface = pygame.transform.scale(self.trailer_surface, (240, 60))

        # Load sounds
        self.crash_sound = pygame.mixer.Sound('sound/crash.mp3')
        self.honk_sound = pygame.mixer.Sound('sound/honk.wav')
        pygame.mixer.music.load('sound/background_music.wav')
        pygame.mixer.music.play(-1)

        self.obstacle_list = []
        self.SPAWN_OBSTACLE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWN_OBSTACLE, 1200)

    def reset_game(self):
        self.game_active = False
        self.on_game_over_screen = False
        self.score = 0
        self.high_score = 0
        self.car_rect = self.car_surface.get_rect(center=CAR_START_POSITION)
        self.obstacle_speed = 5
        self.road_x_pos = 0

    def draw_road(self):
        self.screen.blit(self.road_surface, (self.road_x_pos, 0))
        self.screen.blit(self.road_surface, (self.road_x_pos + SCREEN_WIDTH, 0))

    def create_obstacle(self):
        random_lane = random.choice(LANE_POSITIONS)

        if random.random() < 0.2:  # 20% chance for truck with trailer
            random_truck = random.choice(self.truck_surfaces)
            trailer = self.trailer_surface.get_rect(midbottom=(random.randint(1700, 1900), random_lane))
            truck = random_truck.get_rect(midbottom=(trailer.right + 30, random_lane))
            return [(self.trailer_surface, trailer), (random_truck, truck)]
        else:
            random_car = random.choice(self.obstacle_surfaces)
            obstacle = random_car.get_rect(midbottom=(random.randint(1700, 1900), random_lane))
            return [(random_car, obstacle)]

    def move_obstacles(self):
        for parts in self.obstacle_list:
            for car_surface, obstacle in parts:
                obstacle.centerx -= self.obstacle_speed

        visible_obstacles = []
        for parts in self.obstacle_list:
            parts_visible = []
            for car_surface, obstacle in parts:
                if obstacle.right > -20:
                    parts_visible.append((car_surface, obstacle))
            if parts_visible:
                visible_obstacles.append(parts_visible)
            else:
                self.score += 1
        return visible_obstacles

    def draw_obstacles(self):
        for parts in self.obstacle_list:
            for car_surface, obstacle in parts:
                self.screen.blit(car_surface, obstacle)

    def check_collision(self):
        for parts in self.obstacle_list:
            for car_surface, obstacle in parts:
                if self.car_rect.colliderect(obstacle):
                    self.crash_sound.play()
                    return False
        return True

    def car_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.car_rect.top > 150:
            self.car_rect.centery -= 10
        if keys[pygame.K_DOWN] and self.car_rect.bottom < 750:
            self.car_rect.centery += 10

    def display_score(self):
        score_surface = self.game_font.render(f'Score: {self.score}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(800, 50))
        self.screen.blit(score_surface, score_rect)

    def display_game_over(self):
        game_over_surface = self.game_font.render('Game Over! Press Enter to Return to Title', True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center=(800, 450))
        self.screen.blit(game_over_surface, game_over_rect)

    def display_start_screen(self):
        title_surface = self.game_font.render('Cosmic Highway', True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(800, 300))
        self.screen.blit(title_surface, title_rect)

        start_surface = self.game_font.render('Press Enter to Start', True, (255, 255, 255))
        start_rect = start_surface.get_rect(center=(800, 500))
        self.screen.blit(start_surface, start_rect)

        exit_surface = self.game_font.render('Press Q to Exit', True, (255, 255, 255))
        exit_rect = exit_surface.get_rect(center=(800, 600))
        self.screen.blit(exit_surface, exit_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.on_game_over_screen:
                            self.on_game_over_screen = False
                            self.game_active = False
                        elif not self.game_active:
                            self.game_active = True
                            self.obstacle_list.clear()
                            self.car_rect.center = CAR_START_POSITION
                            self.score = 0

                    if event.key == pygame.K_h:
                        self.honk_sound.play()

                    if not self.game_active and event.key == pygame.K_q:  # Check for Q key
                        pygame.quit()
                        sys.exit()  # Quit the game

                if event.type == self.SPAWN_OBSTACLE and self.game_active:
                    self.obstacle_list.append(self.create_obstacle())

            # Game logic
            self.road_x_pos -= self.obstacle_speed
            if self.road_x_pos <= -SCREEN_WIDTH:
                self.road_x_pos = 0

            self.car_movement()

            if self.game_active:
                self.obstacle_list = self.move_obstacles()
                self.draw_obstacles()
                self.game_active = self.check_collision()
                self.display_score()
                self.obstacle_speed = 5 + self.score // 5

                if not self.game_active:
                    self.on_game_over_screen = True
                    if self.score > self.high_score:
                        self.high_score = self.score

            elif self.on_game_over_screen:
                self.display_game_over()
            else:
                self.display_start_screen()

            self.draw_road()
            self.screen.blit(self.car_surface, self.car_rect)

            pygame.display.update()
            self.clock.tick(60)

if __name__ == "__main__":
    game = CosmicHighway()
    game.run()
