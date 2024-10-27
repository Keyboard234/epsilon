import random
from math import radians

class Weapon:
    def __init__(self, data, FPS):
        self.data = data

        self.maxammo = self.data["maxammo"]
        self.currentammo = self.maxammo
        
        self.rounddelayframes = (1/(self.data["roundsperminute"] / 60)) * FPS
        self.delaytimer = 0
        
        self.spread = radians(data["spreaddegrees"])
    def update(self):
        if self.delaytimer > 1:
            self.delaytimer -= 1
        else:
            self.delaytimer = 0
            self.canshoot = True
    def shoot(self):
        if self.currentammo == 0:
            print("no ammo")
            return False, -1
        if not self.canshoot:
            return False, -1
        
        self.canshoot = False
        self.delaytimer = self.rounddelayframes
        self.currentammo -= 1
        
        bulletangle = random.uniform(-self.spread/2, self.spread/2)
        print(bulletangle)
        return True, bulletangle
    def reload(self):
        self.currentammo = self.data["maxammo"]
