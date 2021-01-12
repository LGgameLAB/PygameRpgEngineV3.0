import pygame
import stats
import settings
import animations

class player:

    animations = {}
    x = 0
    y = 0
    dir = 'r'
    vel = 0
    width, height = settings.tileSize, settings.tileSize
    rect = pygame.Rect(
        x, y, width, height)
    fullArt = 'fullArt'
    framed = False
    animationTick = settings.ticker(10)

    def __init__(self, **kwargs):
        
        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        # self.animations = animations
        # self.x = int(startX)
        # self.y = int(startY)
        # self.dir = startDir
        # self.vel = speed
        # self.width, self.height = 56, 64  # settings.tileSize, settings.tileSize
        self.rect = pygame.Rect(
            self.x, self.y, self.width, self.height)

        self.fullArt = self.animations['fullArt']
        # self.framed = False
        # self.animationTick = settings.ticker(animationBuffer)

        self.setAnimation()

        # self.stats = stats.stats(20, 20, 1, 0,)
        # self.stats.inventory.addItems(stats.basicSword(), stats.basicJavelin())
        # self.stats.inventory.addItems(stats.spellBook())

    def move(self, walls):
        keys = pygame.key.get_pressed()

        #clicked = False

        keySet = settings.globalBtnSet

        if keys[keySet['u']]:
            self.y -= self.vel
            self.dir = 'u'
            self.checkCollide(walls)
            clicked = True
        if keys[keySet['d']]:
            self.y += self.vel
            self.dir = 'd'
            self.checkCollide(walls)
            clicked = True
        if keys[keySet['r']]:
            self.x += self.vel
            self.dir = 'r'
            self.checkCollide(walls)
            clicked = True
        if keys[keySet['l']]:
            self.x -= self.vel
            self.dir = 'l'
            self.checkCollide(walls)
            clicked = True


        self.x = int(self.x)
        self.y = int(self.y)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #print(str(self.x) + " " + str(self.y))

    def update(self, walls):
        self.move(walls)

        if self.animationTick.done:
            self.setAnimation()

        self.animationTick.tick()

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

    #This nonsense is here because there is no current animation sheet for the character
    def setAnimation(self):
        setAnimations = self.animations[self.dir]

        if len(setAnimations) > 1:
            pass
        else:
            self.image = setAnimations[0]#.convert()
            #win.blit(self.image, (self.x, self.y))

    def rotate(self, angle):
        self.image2 = self.fullArt
        self.image = pygame.transform.rotate(self.image2, angle)

