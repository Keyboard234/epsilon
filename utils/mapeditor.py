import json
import math
import pygame
pygame.init()

display_width, display_height = 500, 500
DISPLAY = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Epsilon Map Editor")

gridsize = 400
#map1 = {"3 -1": [{"position": (50, 20), "size": (10, 100), "material": "metal"}, {...}, ...], "3, 2": ... }

isDrawing = False
lastmousepos = (0,0)
currentMaterial = "metal"

currentWall = []
mapWalls = [] #(pos, size, mat)

file = input("Level file name (press enter for new level):")

if file != "":
    with open(file, "r") as f:
        mapWalls = json.load(f)

def coordToGrid(coord):
    return [math.floor(coord[0]/10)*10, math.floor(coord[1]/10)*10]

def update():
    global isDrawing
    global lastmousepos
    global currentWall
    global currentMaterial
    global mapWalls

    currentpos = coordToGrid(pygame.mouse.get_pos())
    lastpos = coordToGrid(lastmousepos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #save map
            #jsonmap = convertMap(mapWalls)
            saveMap(mapWalls, "testmap1")
            pygame.quit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            isDrawing = not isDrawing
            lastmousepos = coordToGrid(pygame.mouse.get_pos())
            print(lastmousepos)
            print(isDrawing)
            if not isDrawing:
                mapWalls.append(currentWall)
                currentWall = []
    
    if isDrawing:
        sizex, sizey = currentpos[0] - lastmousepos[0], currentpos[1] - lastmousepos[1]
        
        if sizex < 0 and sizey < 0:
            sizex, sizey = lastmousepos[0] - currentpos[0], lastmousepos[1] - currentpos[1]
            
        elif sizex < 0:
            sizex, sizey = lastmousepos[0] - currentpos[0], currentpos[1] - lastmousepos[1]
        elif sizey < 0:
            sizex, sizey = currentpos[0] - lastmousepos[0], lastmousepos[1] - currentpos[1]
            #temp = sizey
            currentpos[1] = sizey
            #currentpos[1] = temp

        currentWall = [lastpos, (sizex, sizey), currentMaterial]

def drawGridLines():
    #render vertical background lines
    for x in range(0, 11):
        linex = x*100
        point1y = -500
        point2y = 500
        
        point1pos = (linex, point1y)
        point2pos = (linex, point2y)

        pygame.draw.line(DISPLAY, (100, 100, 100), point1pos, point2pos)
    
    #render horizontal background lines
    for y in range(0, 11):
        liney = y*100
        point1x = -500
        point2x = 500
        
        point1pos = (point1x, liney)
        point2pos = (point2x, liney)

        pygame.draw.line(DISPLAY, (100, 100, 100), point1pos, point2pos)


def render():
    global isDrawing
    global lastmousepos
    global currentWall

    DISPLAY.fill((0, 0, 0))

    drawGridLines()
        
    #render current walls
    for wall in mapWalls:
        wallRect = pygame.Rect(wall[0][0], wall[0][1], wall[1][0], wall[1][1])
        pygame.draw.rect(DISPLAY, (255, 255, 255), wallRect)

    #render box if drawing
    if isDrawing:
        wallRect = pygame.Rect(currentWall[0][0], currentWall[0][1], currentWall[1][0], currentWall[1][1])
        pygame.draw.rect(DISPLAY, (0, 0, 255), wallRect, 1)

    pygame.draw.circle(DISPLAY, (255, 0, 0), pygame.mouse.get_pos(), 4)
    pygame.display.flip()
"""
def convertMap(wallList):
    json.
    for wall in wallList:
        pass
"""
def saveMap(jsonmap, name):
    jsonobject = json.dumps(jsonmap)
    with open(name + ".json", "w") as o:
        o.write(jsonobject)

def main():
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    while True:
        clock.tick(30)
        update()
        render()

if __name__ == "__main__":
    main()
