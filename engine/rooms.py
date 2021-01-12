import pygame
import pytmx
import npc
import settings
import gameData

class door:
    def __init__(self, name, rect, destinationName, outDir): 
        self.id = 'door'
        self.name = name
        self.rect = rect
        self.active = False
        if outDir == 'u':
            self.endRect = pygame.Rect(self.rect[0], self.rect[1] - 64, self.rect[2], self.rect[3])
        
        elif outDir == 'd':
            self.endRect = pygame.Rect(self.rect[0], self.rect[1] + 64, self.rect[2], self.rect[3])
        
        elif outDir == 'l':
            self.endRect = pygame.Rect(self.rect[0] + 64, self.rect[1], self.rect[2], self.rect[3])
        
        else:
            self.endRect = pygame.Rect(self.rect[0] - 64, self.rect[1], self.rect[2], self.rect[3])

        self.destName = destinationName

class trigger:
    def __init__(self, rect, type, value):
        self.id = "trigger"
        self.rect = rect
        self.type = type
        self.value = value
        self.active = False
        self.run = 0

        try:
            if "[" in self.value:
                self.value = self.value.strip('][').split(', ') 
            
                for i in range(0, len(self.value)): 
                    try:
                        self.value[i] = int(self.value[i]) 
                    except:
                        pass
        
        except:
            pass
        

    
class room:

    def __init__(self, filename, tileProportion):
        tiledMap = pytmx.load_pygame(filename, pixelalpha=True)
        self.tileWidth = tiledMap.tilewidth
        self.tileHeight = tiledMap.tileheight
        print(tileProportion)
        print(self.tileWidth)
        self.scale = int(tileProportion / self.tileWidth)
        self.tmxdata = tiledMap
        try:
            self.id = tiledMap.properties['gameId']
            print(self.id)
        except:
            print("no Id")
        self.width = (tiledMap.width * self.scale) * tiledMap.tilewidth
        self.height = (tiledMap.height * self.scale) * tiledMap.tileheight
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.framed = False

        self.walls = []
        self.sprites = []
        self.doors = []
        self.triggers = []

        # self.fullArt =

        self.image = pygame.Surface((self.width, self.height))
        self.load()
        self.image  # .convert()

        self.x = 0
        self.y = 0

        self.dialogue = False

        self.events = []

    def load(self):
        tile = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tileImage = tile(gid)
                    # if tile:
                    if not tileImage is None:
                        #tileRect = pygame.Rect(x * (self.tmxdata.tilewidth * self.scale), y * (self.tmxdata.tileheight * self.scale),self.tileWidth, self.tileHeight)
                        tileImage = pygame.transform.scale(
                            tileImage, (self.tmxdata.tilewidth * self.scale, self.tmxdata.tileheight * self.scale)).convert()
                        self.image.blit(tileImage, (x * (self.tmxdata.tilewidth *
                                                         self.scale), y * (self.tmxdata.tileheight * self.scale)))

        for tile_object in self.tmxdata.objects:
            if tile_object.name == 'player':
                self.pStartX, self.pStartY = int(
                    tile_object.x*self.scale), int(tile_object.y*self.scale)

            if tile_object.name == 'wall' or tile_object.name == 'void':
                self.walls.append(pygame.Rect(int(tile_object.x*self.scale), int(tile_object.y*self.scale),
                                              int(tile_object.width*self.scale), int(tile_object.height*self.scale)))

            if tile_object.name == 'goblin':
                try:
                    self.sprites.append(gameData.goblin(
                        tile_object.x * self.scale, tile_object.y * self.scale, tile_object.dialogue))
                except:
                    self.sprites.append(gameData.goblin(
                        tile_object.x * self.scale, tile_object.y * self.scale, settings.defText))

            if tile_object.name == 'goblin2':
                self.sprites.append(gameData.goblin2(
                    tile_object.x * self.scale, tile_object.y * self.scale))
            
            if tile_object.name == 'door':
                rect = pygame.Rect(int(tile_object.x*self.scale), int(tile_object.y*self.scale),
                                              int(tile_object.width*self.scale), int(tile_object.height*self.scale))
                                            
                self.doors.append(door(tile_object.selfName, rect, tile_object.destName,  tile_object.outDir))

            if tile_object.name == 'trigger':
                    rect = pygame.Rect(int(tile_object.x*self.scale), int(tile_object.y*self.scale),
                        int(tile_object.width*self.scale), int(tile_object.height*self.scale))
                    
                    self.triggers.append(trigger(rect, tile_object.functionType, tile_object.value))


    # def wallOffset(self, offset):
    #    print(self.walls)
    #    for wall in self.walls:
    #        wall = wall.move(offset)

    def returnCollision(self):
        spriteRects = []
        for sprite in self.sprites:
            spriteRects.append(sprite.rect)

        collision = self.walls + spriteRects
        return collision

    def loadSprites(self, *args):
        for arg in args:
            self.sprites.append(arg)

    def update(self, player):
        pause = False
        playerRect = player.rect

        for event in self.events:
            if event.active == False:
                self.events.remove(event)

        self.checkDoor(player)
        self.checkTrigger(player)
            

        for sprite in self.sprites:
            if self.checkEventslen():
                pause = True

            sprite.update(self.walls, playerRect, pause)

            if sprite.dialogueBox.active:
                if not sprite.dialogueBox in self.events:
                    self.events.append(sprite.dialogueBox)

            if sprite.optionBox.active:
                if not sprite.optionBox in self.events:
                    self.events.append(sprite.optionBox)

            if sprite.active:
                if not sprite in self.events:
                    self.events.append(sprite)


    def checkDoor(self, player):
        result = False
        for door in self.doors:
            if door.rect.colliderect(player.rect):

                self.events.append(door)
                result = True
                print("door")

        return result
    
    def checkTrigger(self, player):
        for trigger in self.triggers:
            if trigger.rect.colliderect(player.rect):
                self.events.append(trigger)

    def returnEvent(self):
        return self.events

    def checkEventslen(self):
        if len(self.events) < 1:
            return False
        else:
            return True
