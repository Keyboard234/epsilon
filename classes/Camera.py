class Camera:
    def __init__(self, position, displaysize):
        self.position = position
        self.displaysize = displaysize
    def updatepos(self, newpos):
        self.position = newpos
    def toscreenpos(self, pos):
        return (pos[0]-self.position[0]+(self.displaysize[0]/2), pos[1]-self.position[1]+(self.displaysize[1]/2))
    def toworldpos(self, pos):
        return (pos[0]+self.position[0]-(self.displaysize[0]/2), pos[1]+self.position[1]-(self.displaysize[1]/2))
