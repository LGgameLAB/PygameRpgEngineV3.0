import npc, stats, fx, sounds
import pygame
import settings as stgs
import animations as anims
import optionBox as opBox
import rooms as rms
import player

pygame.init()

if stgs.winResizeable:
    win = pygame.display.set_mode(
        (stgs.winWidth, stgs.winHeight), pygame.RESIZABLE)
else:
    win = pygame.display.set_mode(
        (stgs.winWidth, stgs.winHeight))

print(stgs.path("sampleGoblin"))


######  NPC Creation ######

#name, statsList, moveType, interactionType, imgSheet, x, y, w, h, text


#Talking goblin
def goblin(x, y, text):
    gobSamp = pygame.image.load(stgs.path('sampleGoblin.png'))
    gobUp = pygame.image.load(stgs.path('goblinUp.png'))
    gobDown = pygame.image.load(stgs.path('goblinDown.png'))
    gobLeft = pygame.image.load(stgs.path('goblinLeft.png'))
    gobRight = pygame.image.load(stgs.path('goblinRight.png'))
    return npc.npc('goblin', [12, 12, 1, 20], 1, 1, {'u': gobUp, 'd': gobDown, 'l': gobLeft, 'r': gobRight, 'startFrame': 6, 'fullArt': gobSamp}, x, y, stgs.tileSize, stgs.tileSize, text)

#Fighting goblin
def goblin2(x, y):
    gobSamp = pygame.image.load(stgs.path('sampleGoblin.png'))
    gobUp = pygame.image.load(stgs.path('goblinUp.png'))
    gobDown = pygame.image.load(stgs.path('goblinDown.png'))
    gobLeft = pygame.image.load(stgs.path('goblinLeft.png'))
    gobRight = pygame.image.load(stgs.path('goblinRight.png'))
    return npc.npc('goblin', [12, 12, 1, 20], 1, 2, {'u': gobUp, 'd': gobDown, 'l': gobLeft, 'r': gobRight, 'startFrame': 6, 'fullArt': gobSamp}, x, y, stgs.tileSize, stgs.tileSize, '')

###### Items ######




###### Game ######
rooms = [
    rms.room(stgs.path("dungeonTest.tmx"), stgs.tileSize),
    rms.room(stgs.path("farm1.4.tmx"), stgs.tileSize)
]


charImagePath = stgs.path('LukeDaKnight.png')
charFullArtPath = stgs.path('knightFullArt.png')
charImage = pygame.image.load(charImagePath)
charFullArt = pygame.image.load(charFullArtPath)
charAnimation = {'u': [charImage], 'd': [charImage], 'l': [
    charImage], 'r': [charImage], 'fullArt': charFullArt}
# print(str(rooms[1].pStartY) + " <- here")
playerStats = stats.stats(20, 20, 1, 0)
playerStats.inventory.addItems(stats.basicSword(), stats.basicJavelin())
playerStats.inventory.addItems(stats.spellBook())

player = player.player(
    x = rooms[0].pStartX,
    y = rooms[1].pStartY,
    dir = 'r',
    animations = charAnimation,
    vel = 8,
    animationTick = stgs.ticker(10),
    stats = playerStats,
    framed = False,
    width = 56, #Relative to image size. Should generally fit in one tile.
    height = 64,)
    
