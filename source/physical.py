import global_lists as GLOBAL
import utilities as UTILS

class PhysicalLayer:

    def __init__(self):
        self.package = ""
        self.neighboors = []
        GLOBAL.physical_interfaces.append(self)

    def sendPackage(self):

        self.checkNeighboors()
        print("Enviando ",self.package," para ",self.neighboors)
        for x in self.neighboors:
            x.package = self.package

    def checkNeighboors(self):
        for interface in GLOBAL.physical_interfaces:
            if((interface.id != self.id) and (UTILS.inCircle(self.posX,self.posY,self.range,interface.posX,interface.posY) == True)):
                self.neighboors.append(interface)

    def printPackage(self):
        print(self.package)