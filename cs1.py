import pygame as py
import random


class Entity:
    def __init__(self, name, image, x, y, w, h, speed):

        # Entity Name
        self.name = name
        # Image Path
        self.path = image
        # X Position
        self.x = x
        # Y Position
        self.y = y

        # For Scaling
        # *Width
        self.w = w
        # *Height
        self.h = h

        # Entity Speed
        self.v = speed
        # Is Entity Exist
        self.is_exist = True
        # Image load
        self.img = 0
        pass

    def pos(self):
        # Gives position as (x,y)
        return self.x, self.y

    def size(self):
        # Gives size as (x,y)
        return self.w, self.h

    def img_load(self, center=False, scale=False):
        # Loads image
        self.img = py.image.load(self.path)
        if center or scale:
            self.img_transform(center=center, scale=scale)

    def img_transform(self, center=False, scale=False, w=0, h=0):
        # Moves center to origin
        if center:
            self.x -= self.w / 2
            self.y -= self.h / 2
        # Scales to given values or original values
        if scale:
            if w == 0 or h == 0:
                self.img = py.transform.scale(self.img, (self.w, self.h))
            else:
                self.img = py.transform.scale(self.img, (w, h))

class Player(Entity):
    def __init__(self, name, image, x, y, w, h, speed):
        super().__init__(name, image, x, y, w, h, speed)
        self.bullet = []

class Bullet(Entity):
    def __init__(self, name, image, x, y, w, h, speed):
        super().__init__(name, image, x, y, w, h, speed)
        # When ready equals zero ship will fire.
        self.ready = 0.0
        # Fire rate of ship
        self.fire_rate = 0.004
        self.is_exist = False

class Enemy(Entity):
    def __init__(self, name, image, x, y, w, h, speed):
        super().__init__(name, image, x, y, w, h, speed)
        self.spawn = 0
        self.generate_rate = 0.001
        self.rate_increase = 0.0001
        self.number = 0

def collusion(a, b):
    posAx, posAy = a.pos()
    sizeAx, sizeAy = a.size()
    posBx, posBy = b.pos()
    sizeBx, sizeBy = b.size()
    colA = posAx < posBx < posAx + sizeAx or posAx < posBx + sizeBx < posAx + sizeAx
    colB = posAy < posBy < posAy + sizeAy or posAy < posBy + sizeBy < posAy + sizeAy
    return colA and colB


game = {"name": "Space Invaders",
        "icon": "images/icon.png",
        "bg": "images/bg.jpg",
        "w": 1024,
        "h": 768,
        "score": 0,
        "bgc": (255, 255, 255)}

# Initialize the pygame
py.init()

# Title and Icon
py.display.set_caption(game["name"])
py.display.set_icon(py.image.load(game["icon"]))

# Creates screen
screen = py.display.set_mode((game["w"], game["h"]))
background = py.image.load(game["bg"])

# Clock
clock = py.time.Clock()

# Font
font = []
for size in range(1, 256):
    font.append(py.font.Font("freesansbold.ttf", size))

# Background
bgImg = py.image.load(game["bg"])
bgImg = py.transform.scale(bgImg, (game["w"], game["h"]))

player = Player("Player", "images/icon.png", 512, 684, 64, 64, 0.6)
enemy = Enemy("Enemy", "images/character.png", random.randint(64, 980), random.randint(-100, -64), 64, 64, 0.4)
fire = Bullet("Shot", "images/fire.png", player.x, player.y, 8, 8, 1)

# Player
# *Load and transform
player.img_load(center=True, scale=True)

# Enemy
# *Load and transform
enemy.img_load(center=True, scale=True)

# Fire
# *Scale
fire.img_load(scale=True)

# Game Loop
running = True
while running:
    clock.tick(1000)
    for event in py.event.get():
        # Quit from cross
        if event.type == py.QUIT:
            running = False

    # screen.fill((0, 0, 0)) BG with color
    screen.blit(bgImg, (0, 0))

    """enemy.spawn += enemy.generate_rate
    enemy.generate_rate += enemy.rate_increase
    print(enemy.spawn)
    if enemy.spawn <= 1:
        enemy[enemy.number] = Enemy("Enemy", "images/character.png", player.x, player.y, 8, 8, 1)
        screen.blit(enemy[enemy.number].img, (enemy.x, enemy.y))
        enemy.number += 1
        enemy.spawn = 0"""

    # Player controls
    # *Movement
    keys = py.key.get_pressed()
    if keys[py.K_RIGHT] and player.x < game["w"] - player.w:
        player.x += player.v
    if keys[py.K_LEFT] and 0 < player.x:
        player.x -= player.v
    if keys[py.K_DOWN] and player.y < game["h"] - player.h:
        player.y += player.v
    if keys[py.K_UP] and 0 < player.y:
        player.y -= player.v
    # *Fire
    if keys[py.K_SPACE] and player.is_exist and fire.ready >= 1:
        fire.x = player.x + player.w / 2
        fire.img_transform(center=True)
        fire.y = player.y
        fire.is_exist = True
        fire.ready = 0
    if fire.ready < 1:
        fire.ready += fire.fire_rate

    # Collisions
    # *Enemy and fire
    if collusion(enemy, fire):
        # They will never know where it will come from.
        enemy.x, enemy.y = random.randint(64, 960), random.randint(-100, -64)
        screen.blit(enemy.img, (enemy.x, enemy.y))
        fire.is_exist = False
        game["score"] += 1
        print("Score :", game["score"])

    # Entity behaviours
    if enemy.is_exist:
        screen.blit(enemy.img, (enemy.x, enemy.y))
        # Enemies goes down brrrrr
        enemy.y += enemy.v
        # If enemies goes down too much, they're gonna get destroyed.
        if game["h"] < enemy.y < 0 - enemy.h:
            enemy.is_exist = False

    if player.is_exist:
        screen.blit(player.img, (player.x, player.y))
        if collusion(enemy, player):
            player.is_exist = False
            print("Game over!")
            print("Score :", game["score"])

    if fire.is_exist:
        screen.blit(fire.img, (fire.x, fire.y))
        # Fires goes up brrrrr
        fire.y -= fire.v
        # If fires goes up too much, they're gonna get destroyed.
        if fire.y < 0 - fire.h:
            fire.is_exist = False

    # Score show
    score_text = font[32].render("Score : " + str(game["score"]), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Game over
    if not player.is_exist:
        game_over = font[64].render("Game Over!", True, (255, 255, 255))
        screen.blit(game_over, (325, 350))

    py.display.update()
