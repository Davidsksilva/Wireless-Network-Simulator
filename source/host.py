from layers.physical import PhysicalLayer
import global_lists as GLOBAL
import utilities as UTILS
class Host:

    _neighboors = []
    _position = []

    def __init__(self,range,id,x,y):
        self._id = id
        self._range = range
        self._physicalLayer = PhysicalLayer()
        self._posX = x
        self._posY = y
        GLOBAL.hosts.append(self)
    
    def addNeighboor(self,neighboor):
        self._neighboors.append(neighboor)

    def createPackage(self,package):
        self._physicalLayer._package = package
    
    def checkNeighboors(self):
        for host in GLOBAL.hosts:
            if((host._id != self._id) and (UTILS.inCircle(self._posX,self._posY,self._range,host._posX,host._posY) == True)):
                self._neighboors.append(host)
                
    def sendPackage(self):
        for x in self._neighboors:
            x._physicalLayer._package = self._physicalLayer._package
