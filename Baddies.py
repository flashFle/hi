import pygame
import pygwidgets
import random
import math  # 곡선 이동을 위한 math 함수
from Constants import *

# 👾 곡선으로 떨어지는 Baddie 클래스
class Baddie():
    MIN_SIZE = 10
    MAX_SIZE = 40
    MIN_SPEED = 1
    MAX_SPEED = 8
    BADDIE_IMAGE = pygame.image.load('images/baddie.png')  # 미리 로드

    def __init__(self, window):
        self.window = window
        self.size = random.randint(Baddie.MIN_SIZE, Baddie.MAX_SIZE)
        self.baseX = random.randint(0, WINDOW_WIDTH - self.size)
        self.y = -self.size  # 위에서 시작
        self.image = pygwidgets.Image(self.window, (self.baseX, self.y), Baddie.BADDIE_IMAGE)

        scale_percent = int((self.size / Baddie.MAX_SIZE) * 100)
        self.image.scale(scale_percent, False)

        self.speed = random.randint(Baddie.MIN_SPEED, Baddie.MAX_SPEED)

        # 🌊 곡선 움직임 파라미터
        self.waveAmplitude = random.randint(20, 60)  # 좌우 흔들림 범위
        self.waveFrequency = random.uniform(0.02, 0.05)  # 흔들리는 속도
        self.frameCount = 0  # 시간 흐름을 위한 변수

    def update(self):
        self.y += self.speed
        self.frameCount += 1

        # x 위치를 사인파로 조정
        curvedX = self.baseX + self.waveAmplitude * math.sin(self.frameCount * self.waveFrequency)
        self.image.setLoc((curvedX, self.y))

        return self.y > GAME_HEIGHT

    def draw(self):
        self.image.draw()

    def collide(self, playerRect):
        return self.image.overlaps(playerRect)


# 👾 BaddieMgr 클래스: Baddie 생성 및 관리
class BaddieMgr():
    INITIAL_ADD_RATE = 20  # 시작 시 배디 생성 간격 (프레임 단위)
    MIN_ADD_RATE = 4       # 최소 간격

    def __init__(self, window):
        self.window = window
        self.reset()

    def reset(self):
        self.baddiesList = []
        self.totalFrameCount = 0  # 전체 경과 프레임 수
        self.nFramesTilNextBaddie = self.INITIAL_ADD_RATE

    def update(self):
        nRemoved = 0
        for baddie in self.baddiesList[:]:
            if baddie.update():
                self.baddiesList.remove(baddie)
                nRemoved += 1

        self.totalFrameCount += 1
        self.nFramesTilNextBaddie -= 1

        if self.nFramesTilNextBaddie <= 0:
            self.baddiesList.append(Baddie(self.window))

            # 📉 프레임 수가 많아질수록 간격을 줄임
            newRate = max(
                self.MIN_ADD_RATE,
                self.INITIAL_ADD_RATE - self.totalFrameCount // 300  # 300프레임마다 1씩 감소
            )
            self.nFramesTilNextBaddie = newRate

        return nRemoved

    def draw(self):
        for baddie in self.baddiesList:
            baddie.draw()

    def hasPlayerHitBaddie(self, playerRect, shieldActive=False):
        if shieldActive:
            return False
        return any(baddie.collide(playerRect) for baddie in self.baddiesList)
