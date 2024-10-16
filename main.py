import pygame
import os
import random
import neat
pygame.font.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Load assets
RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.9
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop(0)

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(190, 230)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

class Bird2(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(260, 300)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

class Bird3(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.randint(230, 260)
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

def remove_off_screen_obstacles(obstacles):
    return [obstacle for obstacle in obstacles if obstacle.rect.x > -obstacle.rect.width]

def main(genomes, config):
    pygame.init()
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    run = True
    clock = pygame.time.Clock()
    players = []
    nets = []
    ge = []
    game_speed = 60
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    obstacles = []
    death_count = 0
    clouds = [Cloud(), Cloud()]
    score = 0

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(Dinosaur())
        ge.append(genome)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run and len(players) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        SCREEN.fill((255, 255, 255))

        for player in players:
            player.update(pygame.key.get_pressed())

        if len(obstacles) == 0:
            obstacle_type = random.randint(0, 11)  # Increased range for more granular control
            if obstacle_type in [0, 1]: 
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif obstacle_type in [2, 3]:  # 30% chance for large cactus
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif obstacle_type in [4, 6, 7]:
                obstacles.append(Bird(BIRD))
            elif obstacle_type in [8,5, 9]:
                obstacles.append(Bird2(BIRD))
            elif obstacle_type in [10, 11]:
                obstacles.append(Bird3(BIRD))


        for obstacle in obstacles:
            obstacle.update()
            for i, player in enumerate(players):
                if player.dino_rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 2
                    players.pop(i)
                    nets.pop(i)
                    ge.pop(i)
                else:
                    ge[i].fitness += 1

        for i, player in enumerate(players):
            # Gather more information about the game state
            obstacle_type = obstacles[0].__class__.__name__ if obstacles else "None"
            obstacle_height = obstacles[0].rect.height if obstacles else 0
            obstacle_width = obstacles[0].rect.width if obstacles else 0
            obstacle_y = obstacles[0].rect.y if obstacles else 0
            next_obstacle_distance = obstacles[1].rect.x - player.dino_rect.x if len(obstacles) > 1 else 1000

            # Calculate vertical distance to bird, considering different bird heights
            vertical_distance_to_bird = 0
            if obstacle_type in ["Bird", "Bird2", "Bird3"]:
                vertical_distance_to_bird = player.dino_rect.y - obstacle_y

            output = nets[i].activate((
                player.dino_rect.y,
                player.dino_rect.bottom,
                abs(player.dino_rect.y - obstacles[0].rect.y) if obstacles else 0,
                abs(player.dino_rect.x - obstacles[0].rect.x) if obstacles else 1000,
                game_speed,
                obstacle_type == "SmallCactus",
                obstacle_type == "LargeCactus",
                obstacle_type == "Bird",
                obstacle_type == "Bird2",
                obstacle_type == "Bird3",
                obstacle_height,
                obstacle_width,
                vertical_distance_to_bird,
                next_obstacle_distance,
                player.dino_jump,
                player.dino_duck
            ))
            
            # Adjust the jumping threshold for birds
            jump_threshold = 0
            if obstacle_type in ["Bird"]:
                jump_threshold = 0.7  # Lower threshold to encourage more jumping for birds

            if output[0] > jump_threshold and player.dino_rect.y == player.Y_POS:
                player.dino_jump = True
                player.dino_run = False
            elif output[1] < 0 and player.dino_rect.y == player.Y_POS:
                player.dino_duck = True
                player.dino_run = False

        obstacles = remove_off_screen_obstacles(obstacles)
        
        background()
        
        for cloud in clouds:
            cloud.draw(SCREEN)
            cloud.update()
        
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
        
        for player in players:
            player.draw(SCREEN)

        pygame.display.update()
        clock.tick(30)




def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    winner = p.run(main, 150)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)