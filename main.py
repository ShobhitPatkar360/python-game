import sys

from pygame import mixer

import random

import pygame  # Press Ctrl+Alt+L  to look code good
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))  # 400,300

# Setting Title
pygame.display.set_caption("Space War")

# Setting Icon
icon = pygame.image.load("robot.png")  # Size = 32x32
pygame.display.set_icon(icon)

# Adding Background
background = pygame.image.load("background.png")

# Adding Background Sound
mixer.music.load("background.mp3")
mixer.music.play(-1)

"""
# enemy
enemyImg = pygame.image.load("enemy.png")  # size 64x64
enemyX = random.randint(0,736)
enemyY = random.randint(50,150)
enemyXChange = 1
enemyYChange = 40
"""

enemyImg = []  # size 64x64
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
num_of_enemy = 6

for i in range(num_of_enemy):  # [0,1,2,3,4,5]
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyXChange.append(1)
    enemyYChange.append(40)

"""
what is range(num_of_enemy) ?
 [0,1,2,3,4,5]

range(100)
[0,1,2,3, .... , 99]

"""


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# player
playerImg = pygame.image.load("player.png")
playerX = 368
playerY = 480
playerXChange = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


# Bullet
bulletImg = pygame.image.load("Bullet.png")  # size 32x32
bulletX = 0
bulletY = 480
bulletXChange = 0
bulletYChange = -3
bullet_state = "ready"  # fire = we want to show bullet ; ready = we want to hide bullet

# Score Displaying
score_value = 0
scoreX = 0
scoreY = 0
font = pygame.font.Font("freesansbold.ttf", 50)


def show_score(x, y):
    global score_value
    score_obj = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score_obj, (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    dis = math.sqrt((math.pow(bulletX - enemyX, 2)) + (math.pow(bulletY - enemyY, 2)))
    if dis < 30:
        return True
    else:
        return False


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 15, y - 30))


play = "on"
# Game Loop
running = True
while running:

    # Red Green Blue
    screen.fill((100, 50, 37))

    # adding background
    screen.blit(background, (0, 0))

    # Step 1 => Detect key + "playerXChange" value change
    for event in pygame.event.get():  # Collection of events [ QUIT , KEYDOWN{}  , KEYUP {}, ,   ,   , ]
        if event.type == pygame.QUIT:  # K_LEFT,K_RIGHT,
            running = False

        if event.type == pygame.KEYDOWN:
            # print("key is pressed")

            if event.key == pygame.K_LEFT:
                playerXChange = -1

            if event.key == pygame.K_RIGHT:
                playerXChange = 1

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    bullet_state = "fire"

        if event.type == pygame.KEYUP:
            playerXChange = 0

    # Addig Boundries
    if playerX <= 0:
        playerX = 0

    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemy):  # i = 0,1,2,3,4,5
        enemyX[i] = enemyX[i] + enemyXChange[i]
        if enemyX[i] >= 736:
            enemyXChange[i] = -1
            enemyY[i] = enemyY[i] + enemyYChange[i]

        elif enemyX[i] <= 0:
            enemyXChange[i] = 1
            enemyY[i] = enemyY[i] + enemyYChange[i]

        # Collion Management
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("laser.wav")
            explosion_sound.play()
            bullet_state = "ready"
            bulletY = 480
            score_value = score_value + 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
            # print("Score : " + str(score))  # print() support concatantion of  only string

        enemy(enemyX[i], enemyY[i], i)

    # player movement => Step 2 => Change Coordinate
    playerX = playerX + playerXChange

    # bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY = bulletY + bulletYChange

    show_score(scoreX, scoreY)
    player(playerX, playerY)
    pygame.display.update()

"""
Player Motion Control
Step1: Detect key
Step2: Change coordinate
"""

"""
Bullet Motion Control
Step1: Player coordinates => Bullet coordinates
Step2: Bullet Y coordinate (decrease)

"""
# 2^2      54^3   math.pow(2,2)  math.pow(54,3)
"""
if else in python
String
if variable == "word"   if variable is "word":

Boolean
if variable == True   if variable:

"""

"""
if enemy is shooted
1.bullet_state = "ready"
2.score display
3.enemy is placed to inital position

"""
