import json
import pygame

class Map:
    def __init__(self, file):
        with open(file, "r") as f:
            self.mapdata = json.load(f)
    def render(self, cam, display):
        for key in self.mapdata:
            if key == "wall":
                wallpos = self.mapdata[key]["position"]
                wallsize = self.mapdata[key]["size"]
                wallmaterial = self.mapdata[key]["material"]
                
                wallscreenpos = cam.toscreenpos(wallpos)
                wallrect = pygame.Rect(wallscreenpos[0], wallscreenpos[1], wallsize[0], wallsize[1])
                pygame.draw.rect(display, (200, 200, 200), wallrect)
