import pygame
import random

# Initialize PyGame
pygame.init()

# Display
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load("game_images/background.jpg")

# Title and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("game_images/robot.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("game_images/player_ship.png")
player_x = 370
player_y = 480
# Move
player_dx = 0


def player(x, y):
    screen.blit(player_img, (x, y))


# Enemy
enemy_img = pygame.image.load("game_images/enemy.png")
enemy_x = random.randint(0, 736)
enemy_y = random.randint(50, 150)
# Move
enemy_dx = 3
enemy_dy = 40


def enemy(x, y):
    screen.blit(enemy_img, (x, y))


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
                print("Right")
                player_dx = 5
            if event.key == pygame.K_LEFT:
                print("Left")
                player_dx = -5
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                print("Keystroke released")
                player_dx = 0

    player_x += player_dx

    if player_x < 0:
        player_x = 0
    elif player_x > 736:
        player_x = 736

    enemy_x += enemy_dx

    if enemy_x < 0:
        enemy_dx = 3
        enemy_y += enemy_dy
    elif enemy_x > 736:
        enemy_dx = -3
        enemy_y += enemy_dy

    player(player_x, player_y)
    enemy(enemy_x, enemy_y)
    pygame.display.update()
