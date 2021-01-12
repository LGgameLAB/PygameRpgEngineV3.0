import sys
import time

import pygame
import pytmx

import fightScene as fs
import fx, gameData, npc, settings, sounds, stats

pygame.init()


class event:
    def __init__(self, id):
        self.id = id

class roomGroup:
    def __init__(self):
        self.rooms = []
        self.roomIndex = 0
        #self.room = self.rooms[self.roomIndex]

    def addRooms(self, *args):

        for arg in args:
            self.rooms.append(arg)

        self.update()

    def update(self):
        self.room = self.rooms[self.roomIndex]
    
    def switchRoom(self, destName):
        for room in self.rooms:
            for door in room.doors:
                if door.name == destName:
                    self.room = room 
                    self.roomIndex = self.rooms.index(self.room)

                    return door.endRect[0], door.endRect[1]
        


class cam:

    def __init__(self, width, height, limit):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.limit = limit
        self.cutScene = False
        self.moveCount = 0 
        self.trigLast = 0

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def applyRect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        if self.cutScene:
            self.camera.x += self.stepX #(targX - self.camera.x)/64
            self.camera.y += self.stepY #(targY - self.camera.y)/64
            self.moveCount += 1
            if self.moveCount > self.scrollSpeed -1:
                time.sleep(self.stopTime)
                self.cutScene = False
                x = -target.rect.centerx + int(settings.winWidth / 2)
                y = -target.rect.centery + int(settings.winHeight / 2)
        else:
            #resets the counter for scroll movement
            if self.trigLast > 0:
                self.trigLast -= 1 

            self.moveCount = 0

            x = -target.rect.centerx + int(settings.winWidth / 2)
            y = -target.rect.centery + int(settings.winHeight / 2)

            # limit scrolling to map size
            if self.limit:
                x = min(0, x)  # left
                y = min(0, y)  # top
                x = max(-(self.width - settings.winWidth), x)  # right
                y = max(-(self.height - settings.winHeight), y)  # bottom

            self.camera = pygame.Rect(x, y, self.width, self.height)

    def setScroll(self, scrollTarget, speed, stopTime):
        if self.trigLast < 1:
            self.scrollSpeed = speed
            self.stopTime = stopTime
            self.scrollTarget = pygame.Rect(scrollTarget[0]*64, scrollTarget[1]*64, settings.tileSize, settings.tileSize)
            self.cutScene = True
            self.targX = -self.scrollTarget.centerx + int(settings.winWidth / 2)
            self.targY = -self.scrollTarget.centery + int(settings.winHeight / 2)
            #targetPos = (targX, targY)
            self.stepX = (self.targX - self.camera.x)/self.scrollSpeed #min(1, (targX - self.camera.x)/64)
            self.stepY = (self.targY - self.camera.y)/self.scrollSpeed #min(1, (targY - self.camera.y)/64)
            self.trigLast = 100
        

class game:

    def __init__(self):
        self.buffer = settings.buffer
        self.useCam = True
        self.mapLayer = []
        self.spriteLayer = []
        self.fightSceneLayer = []
        self.dialogueLayer = []
        self.fxLayer = []
        #self.fxLayer.append(fx.flash(settings.red, 1, .1))
        self.mixer = sounds.mixer()
        #self.mixer.playMusic(sounds.music["intro"], -1)
        self.fightSceneBool = False
        self.fightScene = False
        self.fullScreen = False
        self.menu = True

        

    def new(self, win, rooms, player):
        self.win = win
        self.map = roomGroup()
        for room in rooms:
            self.map.addRooms(room)
        
        self.player = player

        self.cam = cam(self.map.room.width, self.map.room.height, True)
        self.mapLayer.append(self.map.room)
        self.spriteLayer.append(self.player)

        for sprite in self.map.room.sprites:
            self.spriteLayer.append(sprite)

    def events(self):
        self.map.update() 
        self.map.room.update(self.player)
        events = self.map.room.returnEvent()
        self.dialogueLayer.clear()
        self.fightSceneLayer.clear()
        self.mapLayer.clear()
        self.spriteLayer.clear()

        movePause = False
        

        if len(events) > 0:
            # This seems wierd but may add new layer for optionbox situations
            for event in events: 
                if event.id == "dialogue":
                    self.dialogueLayer.append(event)
                    movePause = True

                if event.id == "optionBox":
                    self.dialogueLayer.append(event)
                    movePause = True
                    if event.subMenuActive:
                        for sprite in event.returnMenu():
                            self.dialogueLayer.append(sprite)

                if event.id == "door":
                    self.player.x, self.player.y = self.map.switchRoom(event.destName)
                    movePause = True
                
                if event.id == "trigger":
                    if event.type == "soundEdit":
                        self.mixer.setVolume(event.value)
                    
                    if event.type == "musicPlay":
                        self.mixer.playMusic(event.value, -1)
                    
                    if event.type == "musicStop":
                        self.mixer.stop()
                    
                    if event.type == "fx":
                        self.fxLayer.append()
                    
                    if event.type == "testPrint":
                        print("HellYAH")
                    
                    if event.type == "cutScene":
                        #print(self.cam.trigLast)
                        if self.cam.cutScene == False:
                            print("yessir")
                            print(event.value[4])
                            if event.run < event.value[4]:
                                self.cam.setScroll((event.value[0], event.value[1]) , event.value[2], event.value[3])
                                self.map.room.triggers[self.map.room.triggers.index(event)].run += 1
                        else:
                            movePause = True
                        
                    
                    #if event.type == 

                if event.id == "battleSprite":
                    movePause = True
                    if self.fightScene != False:
                        self.fightSceneLayer.append(self.fightScene)
                        self.fightScene.update()
                        if self.fightScene.options != False:
                            self.dialogueLayer.append(self.fightScene.options)
                            if self.fightScene.options.subMenuActive:
                                for sprite in self.fightScene.options.returnMenu():
                                    self.dialogueLayer.append(sprite)
                    else:
                        self.fxLayer.append(fx.fadeOut(0.002))
                        self.fightScene = fs.fightScene(self.player, event)
                        self.fightSceneLayer.append(self.fightScene)
                        self.fightScene.update()
        else:
            self.fightScene = False

        if not movePause:
            self.player.move(self.map.room.returnCollision())

        self.mixer.update(events)

        self.spriteLayer.append(self.player)

        for sprite in self.map.room.sprites:
            self.spriteLayer.append(sprite)

        for spFx in self.fxLayer:
            spFx.update()
            if spFx.active == False:
                self.fxLayer.remove(spFx)

        self.mapLayer.append(self.map.room)

        self.cam.update(self.player)

        

    def rendScreen(self):
        self.win.fill(settings.bgColor)

        for item in self.mapLayer:
            self.win.blit(item.image, self.cam.apply(item))

        for item in self.spriteLayer:
            if item.framed:
                self.win.blit(item.image, self.cam.apply(item), item.frame)
            else:
                self.win.blit(item.image, self.cam.apply(item))

        for item in self.fightSceneLayer:
            # if item.framed:
            #    self.win.blit(item.image, item.fightRect, item.frame)
            # else:
            #    self.win.blit(item.image, item.fightRect)

            self.win.blit(item.image, item.rect)

        for item in self.dialogueLayer:
            self.win.blit(item.image, item.rect)
        
        for item in self.fxLayer:
            print("oye")
            self.win.blit(item.image, item.rect)

    def mainloop(self):
        run = True

        while run:

            time.sleep(self.buffer)

            # Window exit checker

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if settings.winResizeable:
                    if event.type == pygame.VIDEORESIZE:
                        self.win = pygame.display.set_mode((event.w, event.h),
                                                        pygame.RESIZABLE)

                    settings.winWidth = event.w
                    settings.winHeight = event.h
                    settings.dialogueBoxSize = (event.w, int(event.h/4))

            self.getFullScreen()
            self.events()
            self.rendScreen()

            pygame.display.update()

    def getFullScreen(self):
        if settings.fullScreenActive:
            keys = pygame.key.get_pressed()
            if keys[settings.globalBtnSet['fullScreen']]:
                if self.fullScreen:
                    self.win = pygame.display.set_mode((settings.winWidth, settings.winHeight))
                    self.fullScreen = False
                else:
                    self.win = pygame.display.set_mode((settings.winWidth, settings.winHeight), pygame.FULLSCREEN)
                    self.fullScreen = True

    def text_format(self, message, textFont, textSize, textColor):
        newFont=pygame.font.Font(textFont, textSize)
        newText=newFont.render(message, 0, textColor)
    
        return newText
        
    def mainMenu(self):
        
        white = (255, 255, 255)
        black = (0, 0, 0)
        gray = (50, 50, 50)
        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        yellow = (255, 255, 0)

        clock = pygame.time.Clock()
        selected="start"
        font = settings.path("Retro.ttf")
        self.mixer.playMusic('intro', 1)
    
        while self.menu:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_UP:
                        selected="start"
                    elif event.key==pygame.K_DOWN:
                        selected="quit"
                    if event.key==pygame.K_RETURN:
                        if selected=="start":
                            print("Start")
                            self.menu = False
                        if selected=="quit":
                            pygame.quit()
                            quit()
    
            # Main Menu UI
            self.win.fill(black)
            title=self.text_format("Rpg Engine", font, 90, yellow)
            if selected=="start":
                text_start=self.text_format("START", font, 75, yellow)
            else:
                text_start = self.text_format("START", font, 75, white)
            if selected=="quit":
                text_quit=self.text_format("QUIT", font, 75, yellow)
            else:
                text_quit = self.text_format("QUIT", font, 75, white)
    
            title_rect=title.get_rect()
            start_rect=text_start.get_rect()
            quit_rect=text_quit.get_rect()
    
            # Main Menu Text
            self.win.blit(title, (int(settings.winWidth/2 - (title_rect[2]/2)), 80))
            self.win.blit(text_start, (int(settings.winHeight/2 - (start_rect[2]/2)), 300))
            self.win.blit(text_quit, (int(settings.winWidth/2 - (quit_rect[2]/2)), 360))
            pygame.display.update()
            clock.tick(settings.fps)
            pygame.display.set_caption("Rpg Engine-Menu")
            self.getFullScreen()


    def loop(self):
        pygame.display.set_caption(settings.winTitle)
        self.mainMenu()
        self.mainloop()


game1 = game()
game1.new(gameData.win, gameData.rooms, gameData.player)
game1.loop()

pygame.quit()
