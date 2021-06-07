import pygame
import random
import time
import pickle
import os

pygame.font.init()

blue = (0, 0, 128)
black = (0,0,0)
white = (255,255,255)
shadow = (192, 192, 192)
white = (255, 255, 255)
lightGreen = (0, 255, 0)
green = (0, 200, 0)
gray = (50, 50, 50)
blue = (0, 0, 128)
lightBlue = (0, 0, 255)
red = (200, 0, 0 )
lightRed = (255, 100, 100)
purple = (102, 0, 102)
invisable = (0, 0, 0, 0)
yellow = (255, 255, 0)

winWidth, winHeight = 1024, 768
centerX, centerY = winWidth/2, winHeight/2
winTitle = "RPG Engine v2.5"
bgColor = black
winResizeable = False
fullScreenActive = True

tileSize = 64
gridWidth = winWidth / tileSize
gridHeight = winHeight / tileSize

fps = 60
buffer = 1/fps

gameVariables = {}

#print(os.path.)
def path(fileName):
    return "../assets/" + fileName

dialogueBox1 = path('dialogueBox.png')
dialogueBoxSize = (winWidth, int(winHeight/4))
retype = True

optionBox1 = path('optionBox.png')

fightSceneOverlay1 = path('fightSceneOverlay1.jpg')

globalBtnSet = {'u' : pygame.K_UP, 'd' : pygame.K_DOWN, 'l' : pygame.K_LEFT, 'r' : pygame.K_RIGHT, 'interactionBtn' : pygame.K_z,
     'scrollUpBtn' : pygame.K_UP, 'scrollDownBtn' : pygame.K_DOWN, 'menusBtn' : pygame.K_z, 'menusBack' : pygame.K_x, 'fullScreen' : pygame.K_f}

#interactionBtn = pygame.K_z

##scrollDownBtn = pygame.K_DOWN
#menusBtn = pygame.K_z

font1 = pygame.font.Font('freesansbold.ttf', 24)

defText = "Hi"
fightOptions = ['Attack', 'Items', 'Run']

class run:
    def __init__(self, *args):
        if len(args) > 0:
            self.msg = args[0]
        
        self.id = 'run'

class files:
    def __init__(self, filename, nameofdump):
        pass

    def load(self, value):
        self.value = value

    def save(self, value, filename, nameofdump):
        self.file = filename
        self.value = value
        self.name = nameofdump
        with open(self.file, "wb") as f:
            pickle.dump(self.value, f)
    
    def read(self, filename):
        self.file = filename
        with open("savegame", "rb") as f:
            self.value = pickle.load(f)
        return self.value

class ticker:
    def __init__(self, buffer):
        self.buffer = buffer
        self.done = False
        self.ticks = buffer

        self.lock = False

    def tick(self):
        if self.done:
            if self.lock:
                pass
            else:
                self.done = False
        else:
            self.ticks -= 1
            if self.ticks < 1:
                self.ticks = self.buffer
                self.done = True
    
    def reset(self, *args):
        self.done = False

        if len(args) > 0:
            self.ticks = args[0]
        else:
            self.ticks = self.buffer

