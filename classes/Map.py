import json
import pygame

class Map:
    def __init__(self, file):
        with open(file, "r") as f:
            self.mapdata = json.load(f)
        self.gridsize = 400
    def getWalls(self):
        return self.mapdata
    def render(self, cam, display):
        for wall in self.mapdata:
            wallpos = wall[0]
            wallsize = wall[1]
            wallmaterial = wall[2]
            
            wallscreenpos = cam.toscreenpos(wallpos)
            wallrect = pygame.Rect(wallscreenpos[0], wallscreenpos[1], wallsize[0], wallsize[1])
            pygame.draw.rect(display, (200, 200, 200), wallrect)

            """
            #draw bounding box
            
            posx2 = wallpos[0] + wallsize[0]
            posy2 = wallpos[1] + wallsize[1]

            line1 = ((wallpos[0], wallpos[1]), (posx2, wallpos[1])) #top
            line2 = ((wallpos[0], wallpos[1]), (wallpos[0], posy2)) #left

            line3 = ((posx2, posy2),           (posx2, wallpos[1])) #right
            line4 = ((posx2, posy2),           (wallpos[0], posy2)) #bottom
    
            pygame.draw.line(display, (255, 0, 0), cam.toscreenpos(line1[0]), cam.toscreenpos(line1[1]), 1)
            pygame.draw.line(display, (255, 0, 0), cam.toscreenpos(line2[0]), cam.toscreenpos(line2[1]), 1)
            pygame.draw.line(display, (255, 0, 0), cam.toscreenpos(line3[0]), cam.toscreenpos(line3[1]), 1)
            pygame.draw.line(display, (255, 0, 0), cam.toscreenpos(line4[0]), cam.toscreenpos(line4[1]), 1)
            """
