import pygame
import random
import math
import pygame.surfarray as surfarray
from pygame.locals import *
from itertools import cycle

# Initialize PyGame
pygame.init()

# Display
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load("game_images/background.jpg")
FPS = 30
FPSCLOCK = pygame.time.Clock()

# Title and icon
pygame.display.set_caption("Shark Invaders")
icon = pygame.image.load("game_images/icon.png")
pygame.display.set_icon(icon)

class Game:
    def __init__(self):
        # Player
        self.player_img = pygame.image.load("game_images/player.png")
        self.player_x = 370
        self.player_y = 480
        # Move
        self.player_dx = 0

        # Player score
        self.score_value = 0
        self.font = pygame.font.Font("freesansbold.ttf", 32)
        self.text_x = 10
        self.text_y = 10

        # Game over font
        self.game_over_font = pygame.font.Font("freesansbold.ttf", 64)

        # Enemy
        self.enemy_img = []
        self.enemy_x = []
        self.enemy_y = []
        # Move
        self.enemy_dx = []
        self.enemy_dy = []
        self.num_of_enemies = 3

        for i in range(self.num_of_enemies):
            self.enemy_img.append(pygame.image.load("game_images/enemy.png"))
            self.enemy_x.append(random.randint(0, 735))
            self.enemy_y.append(random.randint(50, 150))
            # Move
            self.enemy_dx.append(10)
            self.enemy_dy.append(100)

        # Shark Tooth
        self.tooth_img = pygame.image.load("game_images/tooth.png")
        self.tooth_x = 0
        self.tooth_y = 480
        # Move
        self.tooth_dx = 0
        self.tooth_dy = 20
        self.tooth_state = "ready"

    def show_score(self, x, y):
        score = self.font.render("Score : " + str(self.score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    def game_over_text(self):
        over_text = self.game_over_font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_text, (200, 250))

    def player(self, x, y):
        screen.blit(self.player_img, (x, y))

    def shoot_tooth(self, x, y):
        #global self.tooth_state
        self.tooth_state = "fire"
        screen.blit(self.tooth_img, (x + 16, y + 10))


    def did_collide(self, enemy_x, enemy_y, tooth_x, tooth_y):
        # Distance between 2 points formula
        distance = math.sqrt(math.pow(enemy_x - tooth_x, 2) + math.pow(enemy_y - tooth_y, 2))
        if distance < 27:
            return True
        else:
            return False

    def enemy(self, x, y, i):
        screen.blit(self.enemy_img[i], (x, y))


    # Game Loop

    def frame_step(self, input_actions):
        screen.fill((0, 0, 0))
        screen.blit(background, (0, 0))


        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         running = False
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_RIGHT:
        #             player_dx = 3.5
        #         if event.key == pygame.K_LEFT:
        #             player_dx = -3.5
        #         if event.key == pygame.K_SPACE:
        #             if tooth_state == "ready":
        #                 shoot_tooth(player_x, tooth_y)
        #                 tooth_x = player_x
        #
        #     if event.type == pygame.KEYUP:
        #         if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
        #             player_dx = 0

        pygame.event.pump()

        reward = 0.1
        terminate = False

        if sum(input_actions) != 1:
            raise ValueError("Multiple input Actions!")

        # INPUT ACTIONS
        # Action 0: Do Nothing
        if input_actions[0] == 1:
            self.player_dx = 0

        # Action 1: Go right
        if input_actions[1] == 1:
            self.player_dx = 12

        # Action 2: Go Left
        if input_actions[2] == 1:
            self.player_dx = -12

        # Action 3: Shoot
        if input_actions[3] == 1:
            self.player_dx = 0
            if self.tooth_state == "ready":
                self.shoot_tooth(self.player_x, self.tooth_y)
                self.tooth_x = self.player_x


        # Player movement
        self.player_x += self.player_dx
        if self.player_x < 0:
            self.player_x = 0
        elif self.player_x > 736:
            self.player_x = 736


        # Enemy Movement
        for i in range(self.num_of_enemies):

            # Game over
            #collide_player = self.did_collide(self.enemy_x[i], self.enemy_y[i], self.player_x, self.player_y)
            if(self.enemy_y[i] > 440):
                for j in range(self.num_of_enemies):
                    self.enemy_y[j] = 2000
                #self.game_over_text()
                terminate = True
                reward = -1
                self.__init__()
                break

            self.enemy_x[i] += self.enemy_dx[i]
            if self.enemy_x[i] < 0:
                self.enemy_dx[i] = 12
                self.enemy_y[i] += self.enemy_dy[i]
            elif self.enemy_x[i] > 736:
                self.enemy_dx[i] = -12
                self.enemy_y[i] += self.enemy_dy[i]

            # Collision
            collision = self.did_collide(self.enemy_x[i], self.enemy_y[i], self.tooth_x, self.tooth_y)
            if collision:
                # UPDATE REWARD
                if self.tooth_state == "fire":
                    self.score_value += 1
                    reward = 1
                    self.tooth_y = 480
                    self.tooth_state = "ready"
                    self.enemy_x[i] = random.randint(0, 735)
                    self.enemy_y[i] = random.randint(50, 150)

            self.enemy(self.enemy_x[i], self.enemy_y[i], i)

        # Tooth Movement
        if self.tooth_y <= 0:
            self.tooth_y = 480
            self.tooth_state = "ready"

        if self.tooth_state == "fire":
            self.shoot_tooth(self.tooth_x, self.tooth_y)
            self.tooth_y -= self.tooth_dy

        # Process image data
        image_data = pygame.surfarray.array3d(pygame.display.get_surface())

        self.player(self.player_x, self.player_y)
        self.show_score(self.text_x, self.text_y)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

        return image_data, reward, terminate
