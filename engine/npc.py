import random

import pygame

import animations as anims
import optionBox as opBox
import settings as stgs
import textwrap
import stats

class dialogue:
    def __init__(self, text):
        self.image = pygame.image.load(stgs.dialogueBox1)
        self.width = stgs.dialogueBoxSize[0]
        self.height = stgs.dialogueBoxSize[1]
        self.rect = pygame.Rect(0, stgs.winHeight - self.height, self.width, self.height)
        self.image = pygame.transform.scale(self.image, (self.rect[2], self.rect[3]))
        self.active = False

        self.id = "dialogue"

        self.wrapCount = 32

        self.listText = self.wrap(text)
        for v in self.listText:
            self.listText[self.listText.index(v)] = self.splice(v)

        self.font = stgs.font1
        #self.text = self.font.render(self.strText, True , stgs.white)

        self.typed = False
        self.typedText = ""

        self.startBuffer = stgs.ticker(20)
        self.startBuffer.lock = True

        self.index = 0
        self.text = []

    def splice(self, string): 
        list1=[] 
        list1[:0]=string 
        return list1 

    def wrap(self, string):
        return textwrap.wrap(string, self.wrapCount)

    def update(self):
        self.clearImg()
        
        if self.active:
            self.startBuffer.tick()
            if not self.typed:
                self.line = self.listText[self.index]
                self.typedText = self.typedText +  self.line[len(self.typedText)]

                try:
                    self.text[self.index] = self.typedText
                except:
                    self.text.append(self.typedText)
                
                if len(self.typedText) == len(self.line):
                    self.index += 1
                    self.typedText = ""
                
                if self.index > len(self.listText) - 1:
                    self.typed = True
                    self.index = 0

            for text in self.text:
                textRend = self.font.render(text, True , stgs.white)
                self.image.blit(textRend, (50, 30 +(self.text.index(text)*24)))
                
                #self.typed = True

            if self.startBuffer.done:
                if self.typed:
                    keys = pygame.key.get_pressed()
                    if keys[stgs.globalBtnSet['interactionBtn']]:
                        self.active = False
                        self.startBuffer.reset() 
                        if stgs.retype:
                            self.line = self.listText[self.index]
                            self.text = []
                            self.typedText = ""
                            self.typed = False
                            self.clearImg()
                    

    def clearImg(self):
        self.width = stgs.dialogueBoxSize[0]
        self.height = stgs.dialogueBoxSize[1]
        self.rect = pygame.Rect(0, stgs.winHeight - self.height, self.width, self.height)
        self.image = pygame.image.load(stgs.dialogueBox1)
        self.image = pygame.transform.scale(self.image, (self.rect[2], self.rect[3]))

class npc:
    def __init__(self, name, statsList, moveType, interactionType, imgSheet, x, y, w, h, text):
        self.name = name
        self.stats = stats.stats(statsList)
        self.stats.inventory.addItems(stats.basicSword())
        self.moveType = moveType
        self.interactionType = interactionType
        self.imgSheet = imgSheet
        self.dir = 'r'
        self.x, self.y = x, y
        self.width, self.height = w, h
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.fullArt = imgSheet["fullArt"]
        self.framed = True
        self.setAnimations = anims.animation(self.imgSheet, self.dir, 0.2, self.imgSheet['startFrame'])
        self.setAnimation()
        self.ticker1 = stgs.ticker(5)
        self.dirs = ['u', 'd', 'l', 'r']
        self.moving = False
        self.vel = 2
        self.dist = 0

        self.text = text #"Watcha bee doin' ouwt by yershelf?!"
        self.dialogueBox = dialogue(self.text)
        self.interTick = stgs.ticker(8)
        self.clock = 0
        self.optionBox = opBox.optionBox({'1': {'3': {'7': 'hi', '8': "Whats  up"}, '4': 'aloha'}, '2':{'5': 'hola', '6': 'ola'}})  #'hola'})
        self.optionTick = stgs.ticker(10)

        #this is really misleading but active is for event purposes only; ex: for fightscene shtuff
        self.active = False
        self.id = "battleSprite"

    def update(self, walls, pRect, pause):
        if pause:
            if self.dialogueBox.active:
                self.dialogueBox.update()

            if self.optionBox.active:
                self.optionBox.update()
        else:
            self.clock += 1

            if self.ticker1.done:
                self.setAnimations.update(self.moving, self.dir)

            self.setAnimation()

            self.ticker1.tick()
            self.interTick.tick()
            self.optionTick.tick()

            if self.interactionType == 1:
                if abs(pRect.centerx - self.rect.centerx) < stgs.tileSize + 2 and abs(pRect.centery - self.rect.centery) < stgs.tileSize + 2: 
                    keys = pygame.key.get_pressed()
                    if self.interTick.done:
                        if keys[stgs.globalBtnSet['interactionBtn']]:
                            self.dialogueBox.active = True

            if self.interactionType == 2:
                if abs(pRect.centerx - self.rect.centerx) < stgs.tileSize + 2 and abs(pRect.centery - self.rect.centery) < stgs.tileSize + 2: 
                    keys = pygame.key.get_pressed()
                    if self.interTick.done:
                        if keys[stgs.globalBtnSet['interactionBtn']]:
                            self.active = True
                pass

            if self.interactionType == 3:
                if abs(pRect.centerx - self.rect.centerx) < stgs.tileSize + 2 and abs(pRect.centery - self.rect.centery) < stgs.tileSize + 2: 
                    keys = pygame.key.get_pressed()
                    if self.optionTick.done:
                        if keys[stgs.globalBtnSet['interactionBtn']]:
                            self.optionBox.active = True
                            

            if self.moveType == 1:
                if self.clock > 200:
                    self.clock = 0
                    self.changeDir()

            if self.moveType == 0:
                pass
            
            pRect = [pRect]
            self.move(walls + pRect)

    def changeDir(self):
        self.newDirs = []
        for val in self.dirs:
            if val != self.dir:
                self.newDirs.append(val)

        self.dir = self.newDirs[random.randint(0, 2)]
        if self.moveType == 1:
            self.moving = True
            self.dist = 64

    def move(self, walls):
        if self.moving:
            if self.dist < self.vel:
                self.moving = False
                self.dist = 0
            else:
                self.dist -= self.vel

                if self.dir == 'u':
                    self.y -= self.vel
                    self.checkCollide(walls)

                if self.dir == 'd':
                    self.y += self.vel
                    self.checkCollide(walls)
                if self.dir == 'l':
                    self.x -= self.vel
                    self.checkCollide(walls)
                if self.dir == 'r':
                    self.x += self.vel
                    self.checkCollide(walls)

                self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def checkCollide(self, walls):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        for wall in walls:
            if wall.colliderect(self.rect):
                if self.dir == 'l':
                    self.x += self.vel
                elif self.dir == 'r':
                    self.x -= self.vel
                elif self.dir == 'u':
                    self.y += self.vel
                else:
                    self.y -= self.vel 

                self.changeDir()

    def setAnimation(self):
        self.image = self.setAnimations.GetImg()
        self.frame = self.setAnimations.GetFrame()







#Talking goblin
def goblin(x, y, text):
    gobSamp = pygame.image.load('sample_assets/sampleGoblin.png')
    gobUp = pygame.image.load('sample_assets/goblinUp.png')
    gobDown = pygame.image.load('sample_assets/goblinDown.png')
    gobLeft = pygame.image.load('sample_assets/goblinLeft.png')
    gobRight = pygame.image.load('sample_assets/goblinRight.png')
    return npc('goblin', [12, 12, 1, 20], 1, 1, {'u': gobUp, 'd': gobDown, 'l': gobLeft, 'r': gobRight, 'startFrame': 6, 'fullArt': gobSamp}, x, y, stgs.tileSize, stgs.tileSize, text)

#Fighting goblin
def goblin2(x, y):
    gobSamp = pygame.image.load('sample_assets/sampleGoblin.png')
    gobUp = pygame.image.load('sample_assets/goblinUp.png')
    gobDown = pygame.image.load('sample_assets/goblinDown.png')
    gobLeft = pygame.image.load('sample_assets/goblinLeft.png')
    gobRight = pygame.image.load('sample_assets/goblinRight.png')
    return npc('goblin', [12, 12, 1, 20], 1, 2, {'u': gobUp, 'd': gobDown, 'l': gobLeft, 'r': gobRight, 'startFrame': 6, 'fullArt': gobSamp}, x, y, stgs.tileSize, stgs.tileSize, '')


# class enemy:
#      def __init__(self, name):
#             self.name = name
#
# def goblin():
#   return enemy('goblin')
#
# gob1 = goblin()
#
