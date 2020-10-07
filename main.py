import pygame
import random
import math

# Initialize PyGame
pygame.init()

# Display
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load("game_images/background.jpg")

# Title and icon
pygame.display.set_caption("Shark Invaders")
icon = pygame.image.load("game_images/icon.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("game_images/player.png")
player_x = 370
player_y = 480
# Move
player_dx = 0
# Player score
score = 0


def player(x, y):
    screen.blit(player_img, (x, y))


# Enemy
enemy_img = pygame.image.load("game_images/enemy.png")
enemy_x = random.randint(0, 735)
enemy_y = random.randint(50, 150)
# Move
enemy_dx = 2
enemy_dy = 40


def enemy(x, y):
    screen.blit(enemy_img, (x, y))


# Shark Tooth
tooth_img = pygame.image.load("game_images/tooth.png")
tooth_x = 0
tooth_y = 480
# Move
tooth_dx = 0
tooth_dy = 4
tooth_state = "ready"


def shoot_tooth(x, y):
    global tooth_state
    tooth_state = "fire"
    screen.blit(tooth_img, (x + 16, y + 10))


def did_collide(enemy_x, enemy_y, tooth_x, tooth_y):
    # Distance between 2 points formula
    distance = math.sqrt(math.pow(enemy_x - tooth_x, 2) + math.pow(enemy_y - tooth_y, 2))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_dx = 3.5
            if event.key == pygame.K_LEFT:
                player_dx = -3.5
            if event.key == pygame.K_SPACE:
                if tooth_state == "ready":
                    shoot_tooth(player_x, tooth_y)
                    tooth_x = player_x

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_dx = 0

    # Player movement
    player_x += player_dx
    if player_x < 0:
        player_x = 0
    elif player_x > 736:
        player_x = 736

    # Enemy Movement
    enemy_x += enemy_dx
    if enemy_x < 0:
        enemy_dx = 2
        enemy_y += enemy_dy
    elif enemy_x > 736:
        enemy_dx = -2
        enemy_y += enemy_dy

    # Tooth Movement
    if tooth_y <= 0:
        tooth_y = 480
        tooth_state = "ready"

    if tooth_state == "fire":
        shoot_tooth(tooth_x, tooth_y)
        tooth_y -= tooth_dy

    # Collision
    collision = did_collide(enemy_x, enemy_y, tooth_x, tooth_y)
    if collision:
        tooth_y = 480
        tooth_state = "ready"
        score += 1
        enemy_x = random.randint(0, 735)
        enemy_y = random.randint(50, 150)
        print(score)

    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    pygame.display.update()
