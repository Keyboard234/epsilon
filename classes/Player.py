from classes.Weapons import Weapon
from data import weapondata

from functions import Collision

import pygame
import math

class Player:
    def __init__(self, position, MAXFPS, Map):
        self.position = position
        self.velocity = [0, 0]

        self.angle = 0 #in radians

        self.Map = Map
        self.gridsize = self.Map.gridsize
        self.gridx, self.gridy = self.position[0]//self.gridsize, self.position[1]//self.gridsize

        self.bullethit = None

        self.maxhealth = 100
        self.health = self.maxhealth

        self.color = (0, 0, 255)

        self.MAXFPS = MAXFPS
        self.currentweapon = Weapon(weapondata.ak47data, MAXFPS)
    def startmoving(self, newvel):
        self.velocity = newvel
    def fire(self, enemies):
        success, angleoffset = self.currentweapon.shoot()
        if not success:
            return -1
        bulletangle = self.angle + angleoffset
        
        #check collision with walls
        
        point2 = ((math.cos(bulletangle)*1000)+self.position[0], (math.sin(bulletangle)*1000)+self.position[1])
        
        points = [point2]
        for wall in self.Map.getWalls():
            wall = (wall[0][0], wall[0][1], wall[1][0], wall[1][1])
            collide, p = Collision.linerect((self.position, point2), wall)
            points += p
        
        closest = points[0]
        for p in points:
            distance = Collision.dist(self.position, p)
            if distance < Collision.dist(self.position, closest):
                closest = p
        self.bullethit = closest

        #check collision with enemies
        for enemy in enemies:
            collision, closestpoint = Collision.circleline((enemy.position, 10), (self.position, self.bullethit), True)
            if collision:
                self.bulletcolor = (255, 0, 0)
                self.bullethit = closestpoint


    def checkwallcollision(self):
        hitcircle = (self.position, 10)
        for wall in self.Map.getWalls():
            wall = (wall[0][0], wall[0][1], wall[1][0], wall[1][1])
            colliding = Collision.circlerect(hitcircle, wall)
            if colliding:
                self.color = (255, 0, 0)
                return True

    def tryMove(self):
        self.position[0] += self.velocity[0]
        if self.checkwallcollision():
            self.position[0] -= self.velocity[0]
        
        self.position[1] += self.velocity[1]
        if self.checkwallcollision():
            self.position[1] -= self.velocity[1]

    def update(self):
        self.color = (0, 0, 255)
        self.tryMove()
        self.gridx, self.gridy = self.position[0]//self.gridsize, self.position[1]//self.gridsize

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
        pygame.draw.line(display, (0, 255, 0), camera.toscreenpos(self.position), linepoint)
        
        if self.bullethit is not None:
            pygame.draw.line(display, (255, 255, 255), camera.toscreenpos(self.position), camera.toscreenpos(self.bullethit))
        self.bullethit = None

        pygame.draw.polygon(display, self.color, [camera.toscreenpos(point) for point in pointstransformed])
