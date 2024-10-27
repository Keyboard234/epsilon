from classes.Camera import Camera
from classes.Map import Map
from classes.Player import Player
from classes.Enemy import Enemy

import math
import pygame
pygame.init()

display_width, display_height = 500, 500
DISPLAY = pygame.display.set_mode((display_width, display_height))
DISPLAY.fill((0, 0, 0))
pygame.display.set_caption("Epsilon")

MAXFPS = 60

enemies = []

def dist(p1, p2):
    return math.sqrt( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 )

def anglebetween(p1, p2):
    y = p2[1] - p1[1]
    x = p2[0] - p1[0]
    return math.atan2(y, x)

def update():
    pressed_keys = pygame.key.get_pressed()

    new_x_vel = 0
    new_y_vel = 0
    if pressed_keys[pygame.K_w] and not pressed_keys[pygame.K_s]:
        new_y_vel = -2
    if pressed_keys[pygame.K_s] and not pressed_keys[pygame.K_w]:
        new_y_vel = 2
    if pressed_keys[pygame.K_a] and not pressed_keys[pygame.K_d]:
        new_x_vel = -2
    if pressed_keys[pygame.K_d] and not pressed_keys[pygame.K_a]:
        new_x_vel = 2

    if (new_x_vel, new_y_vel) != (player.velocity[0], player.velocity[1]):
        player.startmoving((new_x_vel, new_y_vel))
    
    if pygame.mouse.get_pressed()[0]:
        player.fire()

    player.update()

    #change camera position based on mouse distance and angle from player
    mouseworldpos = camera.toworldpos(pygame.mouse.get_pos())
    playerpos = player.position
    mouse_plr_dist = dist(playerpos, mouseworldpos)/5
    
    mouse_plr_angle = anglebetween(playerpos, mouseworldpos)
    player.angle = mouse_plr_angle
    
    offsetpos = [math.cos(mouse_plr_angle)*mouse_plr_dist, math.sin(mouse_plr_angle)*mouse_plr_dist]

    camera.position = (playerpos[0] + offsetpos[0], playerpos[1] + offsetpos[1])

def render():
    DISPLAY.fill((0, 0, 0))

    #draw map
    map1.render(camera, DISPLAY)
    
    #draw vertical background lines
    for x in range(-1, 2):
        linex = x*100
        point1y = -200
        point2y = 200
        
        point1pos = camera.toscreenpos((linex, point1y))
        point2pos = camera.toscreenpos((linex, point2y))

        pygame.draw.line(DISPLAY, (255, 255, 255), point1pos, point2pos)
    
    #draw horizontal background lines
    for y in range(-1, 2):
        liney = y*100
        point1x = -200
        point2x = 200
        
        point1pos = camera.toscreenpos((point1x, liney))
        point2pos = camera.toscreenpos((point2x, liney))

        pygame.draw.line(DISPLAY, (255, 255, 255), point1pos, point2pos)

    player.render(DISPLAY, camera)
    for enemy in enemies:
        enemy.render(DISPLAY, camera)

    pygame.display.flip()

def main():
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(MAXFPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        update()
        render()

if __name__ == "__main__":
    map1 = Map("data/maps/newmap.json")
    playerstartpos = [0, 0]
    camera = Camera([0, 0], (display_width, display_height))
    player = Player(playerstartpos, MAXFPS)
    enemy = Enemy([20, 20], MAXFPS)
    enemies.append(enemy)
    main()
