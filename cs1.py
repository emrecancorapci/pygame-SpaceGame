import pygame as pg
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
        self.img = pg.image.load(self.path)
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
                self.load = pg.transform.scale(self.load, (self.w, self.h))
            else:
                self.load = pg.transform.scale(self.load, (w, h))


class Bullet(Entity):
    def __init__(self, name, image, x, y, w, h, speed):
        super().__init__(name, image, x, y, w, h, speed)
        self.ready = 0
        self.fire_rate = 0
        self.is_exist = False


def collusion(a, b):
    posAx, posAy = a.pos()
    sizeAx, sizeAy = a.size()
    posBx, posBy = b.pos()
    sizeBx, sizeBy = b.size()
    colA = posAx < posBx < posAx + sizeAx or posAx < posBx + sizeBx < posAx + sizeAx
    colB = posAy < posBy < posAy + sizeAy or posAy < posBy + sizeBy < posAy + sizeAy
    return colA and colB


game = {"name": "Space Invaders",
        "icon": "icon.png",
        "bg": "bg.jpg",
        "w": 1024,
        "h": 768,
        "score": 0,
        "bgc": (255, 255, 255)}

# Initialize the pygame
pg.init()

# Title and Icon
pg.display.set_caption(game["name"])
pg.display.set_icon(pg.image.load(game["icon"]))

# Creates screen
screen = pg.display.set_mode((game["w"], game["h"]))
background = pg.image.load(game["bg"])

# Background
bgImg = pg.image.load(game["bg"])
bgImg = pg.transform.scale(bgImg, (game["w"], game["h"]))

player = Entity("Player", "icon.png", 512, 684, 64, 64, 0.6)
enemy = Entity("Enemy", "character.png", random.randint(64, 980), random.randint(-100, -64), 64, 64, 0.4)
fire = Bullet("Shot", "fire.png", player.x, player.y, 8, 8, 1)

# Player
# *Load
player.img_load(center=True, scale=True)

# Enemy
# *Scale
enemy.img_load(center=True, scale=True)

# Fire
# *Scale
fire.img_load(scale=True)
fire_ready = 0.0

# Game Loop
running = True
while running:
    for event in pg.event.get():
        # Quit from cross
        if event.type == pg.QUIT:
            running = False

    # screen.fill((0, 0, 0)) BG with color
    screen.blit(bgImg, (0, 0))
    # Player controls
    # *Movement
    if pg.key.get_pressed()[pg.K_RIGHT] and player.x < game["w"] - player.w:
        player.x += player.v
    if pg.key.get_pressed()[pg.K_LEFT] and 0 < player.x:
        player.x -= player.v
    if pg.key.get_pressed()[pg.K_DOWN] and player.y < game["h"] - player.h:
        player.y += player.v
    if pg.key.get_pressed()[pg.K_UP] and 0 < player.y:
        player.y -= player.v
    # *Fire
    if pg.key.get_pressed()[pg.K_SPACE] and player.is_exist and fire_ready >= 100:
        fire.x = player.x + player.w / 2
        fire.img_transform(center=True)
        fire.y = player.y
        fire.is_exist = True
        fire.ready = 0
    if fire.ready < 100:
        fire.ready += fire.fire_rate

    # Collisions
    # *Enemy and fire
    if collusion(enemy, fire):
        enemy.x, enemy.y = random.randint(64, 960), random.randint(-100, -64)
        screen.blit(enemy.load, (enemy.x, enemy.y))
        fire.is_exist = False
        game["score"] += 1
        print("Score :", game["score"])

    # *Player and enemy
    if collusion(enemy, player):
        player.x, player.y = 0, 0
        player.is_exist = False
        print("Game over!")
        print("Score :", game["score"])

    # Entity behaviours
    if enemy.is_exist:
        enemy.y += enemy.v
        screen.blit(enemy.load, (enemy.x, enemy.y))

    if player.is_exist:
        screen.blit(player.load, (player.x, player.y))

    if fire.is_exist:
        screen.blit(fire.load, (fire.x, fire.y))
        fire.y -= fire.v
        if fire.x < 0 - fire.w:
            fire.is_exist = False

    pg.display.update()
