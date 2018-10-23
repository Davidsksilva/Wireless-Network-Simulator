from layers import PhysicalLayer, LinkLayer
import global_variables as GLOBAL
import utilities as UTILS

class Host:

    def createPackage(self, mac_destiny, message, time):
        self.linkLayer.addPackage(mac_destiny, message,time)


    def __init__(self,range,id,x,y):
        self.linkLayer = LinkLayer(x,y,range,id)