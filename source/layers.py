import global_variables as GLOBAL
import utilities as UTILS
from package import Package, Header

class PhysicalLayer:

    def __init__(self, x, y, r, i):
        self.outputPackagesChannel1 = []
        self.inputPackagesChannel1 = []
        self.outputPackagesChannel2 = []
        self.inputPackagesChannel2 = []
        self.neighboors = []
        self.posX = y
        self.posY = x
        self.range = r
        self.mac = i
        GLOBAL.physical_interfaces.append(self)

    def receivePackage(self, package):

        if(package.headers[0].type == 2):
            self.inputPackagesChannel2.insert(len(self.inputPackagesChannel2),package)
        else:
             self.inputPackagesChannel1.insert(len(self.inputPackagesChannel1),package)

    def addPackage(self, package, type):

        # Canal 2 - Busy Tone
        if ( type == 2 ):
            self.outputPackagesChannel2.insert(len(self.outputPackagesChannel2), package)
        
        # Canal 1 - Normal
        else:
            self.outputPackagesChannel1.insert(len(self.outputPackagesChannel1),package)

    def sendPackage(self,type):

        # Canal 2 - Busy Tone
        if( type == 2):

            package = self.outputPackagesChannel2.pop(0)
            self.checkNeighboors()
            #print(self.mac," enviou ",package.dataLoad)
            for x in self.neighboors:
                x.receivePackage(package)

        # Canal 1 - Normal
        else:
            package = self.outputPackagesChannel1.pop(0)

            self.checkNeighboors()
            print(self.mac," enviou ",package.dataLoad)
            for x in self.neighboors:
                x.receivePackage(package)

    def checkNeighboors(self):
        for interface in GLOBAL.physical_interfaces:
            if((interface.mac != self.mac) and (UTILS.inCircle(self.posX,self.posY,self.range,interface.posX,interface.posY) == True)):
                self.neighboors.append(interface)

    def printPackage(self):
        
        for package in self.inputPackagesChannel1:
            print(package)


class LinkLayer:

    def __init__(self, x, y, r, i):

        self.backoff = 0
        self.counter = 0
        self.busy = 0
        self.busyToneList = []
        self.physicalLayer = PhysicalLayer(x,y,r,i) 


    def addPackage(self, mac_destiny, data_load, time):

        # Create Link Layer Header
        header = Header(0,self.physicalLayer.mac,mac_destiny,self.counter)

        self.counter = self.counter + 1

        # Create Package
        package = Package(data_load,time)

        # Append Header to package
        package.appendHeader(header)

        # Send Package to Physical Layer
        self.physicalLayer.addPackage(package,1)

    def sendPackage(self):

        if(self.physicalLayer.outputPackagesChannel1):


            destiny = self.physicalLayer.outputPackagesChannel1[0].headers[0].macDestiny

            # Checa se o receptor está com busy tone
            permissionToSend = False

            for x in self.busyToneList:

                if(destiny == x[0]):

                    # Se receptor estiver livre, libera o pacote para emissão
                    if(x[1] == 0):
                       permissionToSend = True
            
            if( (permissionToSend == True) or (not len(self.busyToneList))):
                if(self.physicalLayer.outputPackagesChannel1[0].sendTime == 0):

                    self.physicalLayer.sendPackage(1)

                else:

                    self.physicalLayer.outputPackagesChannel1[0].sendTime-=1


    def sendBusyTone(self):

        # Create Link Layer Header
        header = Header(2,self.physicalLayer.mac,-1,-1)

        # Create Package
        package = Package(self.busy,0)

        # Append Header to package
        package.appendHeader(header)

        # Send Package to Physical Layer
        self.physicalLayer.addPackage(package,2)
        self.physicalLayer.sendPackage(2)

    def readPackages(self):


        # Se houver pacotes normais
        if(self.physicalLayer.inputPackagesChannel1):

            self.busy = 1

            if(self.physicalLayer.inputPackagesChannel1[0].readTime == 0 ):
                    # Terminou de ler o  pacote
                
                package = self.physicalLayer.inputPackagesChannel1.pop(0)

                if(package.headers[0].macDestiny == self.physicalLayer.mac):
                    print(self.physicalLayer.mac, " leu ",package.dataLoad, " de ",package.headers[0].macOrigin)
            
                # Libera o canal
                self.busy = 0
            
            else:
                self.physicalLayer.inputPackagesChannel1[0].readTime-=1


        else:

            self.busy = 0


        self.sendBusyTone()


        # Se houver pacotes de busy tone
        if(self.physicalLayer.inputPackagesChannel2):

            package = self.physicalLayer.inputPackagesChannel2.pop(0)

            found = False

            # Procura MAC na lista de Busy Tones
            for x in self.busyToneList:

                if(x[0] == package.headers[0].macOrigin):
                    x[1] = package.dataLoad
                    found = True
                
            if(found == False):

                x = [package.headers[0].macOrigin,package.dataLoad]
                self.busyToneList.append(x)




            
            
        
    def printPackage(self):

        for package in self.physicalLayer.inputPackagesChannel1:

            if( package.headers[0].macDestiny == self.physicalLayer.mac):
                print(package.dataLoad)




        

