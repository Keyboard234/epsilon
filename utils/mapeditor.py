import json

import pygame
pygame.init()

display_width, display_height = 500, 500
DISPLAY = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Epsilon Map Editor")

map1 = {"wall": {"position": (50, 20), "size": (10, 100), "material": "metal"}}

isDrawing = False
lastmousepos = (0,0)

class Wall:
    def __init__(self, position, size, material):
        pass
    def render(self):
        pass

mapWalls = [] #(pos, size, mat)

def update():
    global isDrawing
    global lastmousepos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            isDrawing = not isDrawing
            lastmousepos = pygame.mouse.get_pos()
            print(isDrawing)
    
def render():
    global isDrawing
    global lastmousepos

    DISPLAY.fill((0, 0, 0))
    
    #render vertical background lines
    for x in range(0, 11):
        linex = x*100
        point1y = -500
        point2y = 500
        
        point1pos = (linex, point1y)
        point2pos = (linex, point2y)

        pygame.draw.line(DISPLAY, (255, 255, 255), point1pos, point2pos)
    
    #render horizontal background lines
    for y in range(0, 11):
        liney = y*100
        point1x = -500
        point2x = 500
        
        point1pos = (point1x, liney)
        point2pos = (point2x, liney)

        pygame.draw.line(DISPLAY, (255, 255, 255), point1pos, point2pos)
    
    #render box if drawing
    if isDrawing:
        currentpos = list(pygame.mouse.get_pos())
        lastpos = list(lastmousepos)
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

        boxRect = pygame.Rect(lastpos[0], lastpos[1], sizex, sizey)
        pygame.draw.rect(DISPLAY, (0, 0, 255), boxRect, 1)

    pygame.draw.circle(DISPLAY, (255, 0, 0), pygame.mouse.get_pos(), 4)
    pygame.display.flip()

def saveMap(name):

    #for wall in mapWalls:
    
    jsonobject = json.dumps(map1)
    with open(name, "w") as o:
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
