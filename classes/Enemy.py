from classes.Weapons import Weapon
from data import weapondata

import pygame
import math

class Enemy:
    def __init__(self, position, MAXFPS):
        self.position = position
        self.velocity = [0, 0]
        self.angle = 0 #in radians

        self.maxhealth = 100
        self.health = self.maxhealth

        self.MAXFPS = MAXFPS
        self.currentweapon = Weapon(weapondata.m9data, MAXFPS)
    def startmoving(self, newvel):
        self.velocity = newvel
    def fire(self):
        self.currentweapon.shoot()
        
    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.currentweapon.update()

        if self.health <= 0:
            print("dead")

    def render(self, display, camera):
        size = 10


        point1pos = (math.cos(self.angle), math.sin(self.angle)) #front
        point2pos = (math.cos(self.angle+math.pi/0.3), math.sin(self.angle+math.pi/0.3))
        point3pos = (math.cos(self.angle-math.pi/0.3), math.sin(self.angle-math.pi/0.3))
        points = [point1pos, point2pos, point3pos]
        pointstransformed = [( (point[0]*size)+self.position[0] , (point[1]*size)+self.position[1] ) for point in points]
        
        linepoint = camera.toscreenpos((math.cos(self.angle)*size*4+self.position[0], math.sin(self.angle)*size*4+self.position[1]))
        pygame.draw.line(display, (0, 255, 0), camera.toscreenpos((self.position)), linepoint)
        
        pygame.draw.polygon(display, (255, 0, 0), [camera.toscreenpos(point) for point in pointstransformed])
