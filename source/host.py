from physical import PhysicalLayer
import global_lists as GLOBAL
import utilities as UTILS

class Host:

    def createPackage(self,package):
        self.physicalLayer.package = package
    
    def sendPackage(self):
        self.physicalLayer.sendPackage()

    def __init__(self,range,id,x,y):
        self.physicalLayer = PhysicalLayer()
        self.physicalLayer.posX = x 
        self.physicalLayer.posY = y
        self.physicalLayer.range = range
        self.physicalLayer.id = id
