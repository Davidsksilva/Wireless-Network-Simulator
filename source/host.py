from layers import PhysicalLayer, LinkLayer, NetworkLayer
import global_variables as GLOBAL
import utilities as UTILS

class Host:

    def createPackage(self, mac_destiny, message, time):
        self.networkLayer.addPackage(mac_destiny,message,time)
        #self.linkLayer.addPackage(mac_destiny, message,time)


    def __init__(self,range,id,x,y):
        #self.linkLayer = LinkLayer(x,y,range,id)
        self.networkLayer = NetworkLayer(range,id,x,y)