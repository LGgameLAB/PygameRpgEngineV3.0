import random
import time


healthKey = "Health"
maxHpKey = "Max Hit Points"
levelKey = "Level"
expKey = "Experience"

statFormat = {maxHpKey: 0, healthKey: 0,levelKey: 0, expKey: 0}

class attack:
    def __init__(self, damage, data):
        self.damage = damage
        self.type = data["dmgType"]
        self.id = 'attack'

class item:
    def __init__(self, name, effect):
        self.name = name
        self.id = "item"
        self.effect = effect
    
    def getInfo(self):
        return self.name, self.effect

class weapon:
    def __init__(self, damage, data, name):
        self.attack = attack(damage, data)
        self.id = 'weapon'
        self.name = name
    
    def getInfo(self):
        return self.name

#Weapons are part of items but to access them more easily they have a seperate list
class inventory:
    def __init__(self):
        self.items = []
        self.weapons = []

    def addItems(self, *args):
        for arg in args:
            self.items.append(arg)
        
        for item in self.items:
            if item.id == "weapon":
                self.weapons.append(item)

class stats:
    def __init__(self, *args):
        global statFormat

        self.stats = {}
        if len(args) == 1:
            if isinstance(args[0], list):
                x = 0
                for k in statFormat:
                    self.stats[k] = args[0][x]
                    x += 1
        else:
            x = 0
            for k in statFormat:
                self.stats[k] = args[x]
                x += 1

        self.attackList = []
        self.inventory = inventory()
        self.weakness = ''

    def addAttacks(self, *args):
        for arg in args:
            self.attackList.append(arg)
    
    def recvHit(self, hit):
        global healthKey

        if hit.type == "self.weakness":
            self.stats[healthKey] -= hit.damage*2
        else:
            self.stats[healthKey] -= hit.damage
    
    def randAttack(self):
        if len(self.inventory.weapons) > 1:
            randVal = random.randint(0, len(self.inventory.weapons) - 1)
        
        else:
            randVal = 0

        time.sleep(2)

        return self.inventory.weapons[randVal].attack
        
    


def basicSword():
    return weapon(6, {"dmgType": 'slash'}, 'Basic Sword')

def basicJavelin():
    return weapon(8, {"dmgType": 'piercing'}, 'Basic Javelin')

def spellBook():
    return item("SpellBook", "Heal")