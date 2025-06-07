# Goodie and GoddieMgr classes
import pygame
import pygwidgets
import random
from Constants import *

# 🛡️ Shieldie 클래스 (쉘드 아이템)
class Shieldie():
    MIN_SIZE = 15
    MAX_SIZE = 45
    MIN_SPEED = 2
    MAX_SPEED = 6
    SHIELDIE_IMAGE = pygame.image.load('images/shieldie.png')
    RIGHT = 'right'
    LEFT = 'left'

    def __init__(self, window):
        self.window = window
        size = random.randrange(Shieldie.MIN_SIZE, Shieldie.MAX_SIZE + 1)
        self.y = random.randrange(0, GAME_HEIGHT - size)

        self.direction = random.choice([Shieldie.LEFT, Shieldie.RIGHT])
        if self.direction == Shieldie.LEFT:
            self.x = WINDOW_WIDTH
            self.speed = - random.randrange(Shieldie.MIN_SPEED, Shieldie.MAX_SPEED + 1)
            self.minLeft = - size
        else:
            self.x = 0 - size
            self.speed = random.randrange(Shieldie.MIN_SPEED, Shieldie.MAX_SPEED + 1)

        self.image = pygwidgets.Image(self.window, (self.x, self.y), Shieldie.SHIELDIE_IMAGE)
        percent = int((size * 10) / Shieldie.MAX_SIZE)
        self.image.scale(percent, False)

    def update(self):
        self.x += self.speed
        self.image.setLoc((self.x, self.y))
        if self.direction == Shieldie.LEFT:
            return self.x < self.minLeft
        else:
            return self.x > WINDOW_WIDTH

    def draw(self):
        self.image.draw()

    def collide(self, playerRect):
        return self.image.overlaps(playerRect)


class Goodie():
    MIN_SIZE = 10
    MAX_SIZE = 40
    MIN_SPEED = 1
    MAX_SPEED = 8
    GOODIE_IMAGE = pygame.image.load('images/goodie.png')
    RIGHT = 'right'
    LEFT = 'left'

    def __init__(self, window):
        self.window = window
        size = random.randrange(Goodie.MIN_SIZE, Goodie.MAX_SIZE + 1)
        self.y = random.randrange(0, GAME_HEIGHT - size)

        self.direction = random.choice([Goodie.LEFT, Goodie.RIGHT])
        if self.direction == Goodie.LEFT:
            self.x = WINDOW_WIDTH
            self.speed = - random.randrange(Goodie.MIN_SPEED, Goodie.MAX_SPEED + 1)
            self.minLeft = - size
        else:
            self.x = 0 - size
            self.speed = random.randrange(Goodie.MIN_SPEED, Goodie.MAX_SPEED + 1)

        self.image = pygwidgets.Image(self.window, (self.x, self.y), Goodie.GOODIE_IMAGE)
        percent = int((size * 100) / Goodie.MAX_SIZE)
        self.image.scale(percent, False)

    def update(self):
        self.x += self.speed
        self.image.setLoc((self.x, self.y))
        if self.direction == Goodie.LEFT:
            return self.x < self.minLeft
        else:
            return self.x > WINDOW_WIDTH

    def draw(self):
        self.image.draw()

    def collide(self, playerRect):
        return self.image.overlaps(playerRect)


class GoodieMgr():
    GOODIE_RATE_LO = 90
    GOODIE_RATE_HI = 111
    SHIELDIE_RATE = 180

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):
        self.goodiesList = []
        self.shieldiesList = []
        self.nFramesTilNextGoodie = GoodieMgr.GOODIE_RATE_HI
        self.nFramesTilNextShieldie = GoodieMgr.SHIELDIE_RATE

    def update(self, thePlayerRect):
        nGoodiesHit = 0
        shieldGiven = False

        # Goodies 처리
        for oGoodie in self.goodiesList[:]:
            deleteMe = oGoodie.update()
            if deleteMe or oGoodie.collide(thePlayerRect):
                self.goodiesList.remove(oGoodie)
                if oGoodie.collide(thePlayerRect):
                    nGoodiesHit += 1

        # Shieldies 처리
        for oShieldie in self.shieldiesList[:]:
            deleteMe = oShieldie.update()
            if deleteMe or oShieldie.collide(thePlayerRect):
                self.shieldiesList.remove(oShieldie)
                if oShieldie.collide(thePlayerRect):
                    shieldGiven = True

        # Goodie 생성
        self.nFramesTilNextGoodie -= 1
        if self.nFramesTilNextGoodie <= 0:
            self.goodiesList.append(Goodie(self.window))
            self.nFramesTilNextGoodie = random.randrange(GoodieMgr.GOODIE_RATE_LO, GoodieMgr.GOODIE_RATE_HI)

        # Shieldie 생성
        self.nFramesTilNextShieldie -= 1
        if self.nFramesTilNextShieldie <= 0:
            self.shieldiesList.append(Shieldie(self.window))
            self.nFramesTilNextShieldie = GoodieMgr.SHIELDIE_RATE

        return nGoodiesHit, shieldGiven

    def draw(self):
        for oGoodie in self.goodiesList:
            oGoodie.draw()
        for oShieldie in self.shieldiesList:
            oShieldie.draw()
