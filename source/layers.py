import global_variables as GLOBAL
import utilities as UTILS
from package import Package, Header, Route

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
            if(package.headers[0].macDestiny == self.mac):
                self.inputPackagesChannel1.insert(len(self.inputPackagesChannel1),package)
        
        

    def addPackage(self, package, type):

        # Canal 2 - Busy Tone
        if ( type == 2 ):
            self.outputPackagesChannel2.insert(len(self.outputPackagesChannel2), package)
        
        # Canal 1 - Normal
        else:
            self.outputPackagesChannel1.insert(len(self.outputPackagesChannel1),package)

    def broadcastGivenPackage(self, type, package):

        # Canal 2 - Busy Tone
        if( type == 2):

            self.checkNeighboors()
            for x in self.neighboors:
                x.receivePackage(package)

        # Canal 1 - Normal
        elif (type == 1):

                self.checkNeighboors()
                print(self.mac," enviou ",package.dataLoad)
                for x in self.neighboors:
                    x.receivePackage(package)

    def broadcastPackage(self,type):

        
        # Canal 2 - Busy Tone
        if( type == 2):

            package = self.outputPackagesChannel2.pop(0)
            self.checkNeighboors()
            #print(self.mac," enviou ",package.dataLoad)
            for x in self.neighboors:
                x.receivePackage(package)

        # Canal 1 - Normal
        elif (type == 1):
            if(self.outputPackagesChannel1):
                package = self.outputPackagesChannel1.pop(0)

                self.checkNeighboors()
                print(self.mac," enviou ",package.dataLoad)
                for x in self.neighboors:
                    x.receivePackage(package)


    def checkNeighboors(self):

        for interface in GLOBAL.physical_interfaces:
            if((interface.mac != self.mac) and (UTILS.inCircle(self.posX,self.posY,self.range,interface.posX,interface.posY) == True)):

               if interface not in self.neighboors:
                self.neighboors.append(interface)

    def printPackage(self):
        
        for package in self.inputPackagesChannel1:
            print("pacote = ",package.dataLoad)


class LinkLayer:

    def __init__(self, x, y, r, i):

        self.backoff = 0
        self.counter = 0
        self.busy = 0
        self.sendCounter = 0
        self.readyPackagesList = []
        self.busyToneList = []
        self.physicalLayer = PhysicalLayer(x,y,r,i) 

    def addHeader(self,package):

         # Create Link Layer Header
        header = Header(0,self.physicalLayer.mac,-1,self.counter,-1,-1,-1)

        self.counter = self.counter + 1

        # Append Header to package
        package.appendHeader(header)

        # Send Package to Physical Layer
        self.physicalLayer.addPackage(package,1)

    def addPackage(self, mac_destiny, data_load, time):

        # Create Link Layer Header
        header = Header(0,self.physicalLayer.mac,mac_destiny,self.counter,-1,-1,-1)

        self.counter = self.counter + 1

        # Create Package
        package = Package(data_load,time)

        # Append Header to package
        package.appendHeader(header)

        # Send Package to Physical Layer
        self.physicalLayer.addPackage(package,1)

    def sendNewPackage(self, package, mac_destiny):

        # Create Link Layer Header
        header = Header(0,self.physicalLayer.mac,mac_destiny,self.counter,-1,-1,-1)

        self.counter = self.counter + 1
    
        # Append Header to package
        package.appendHeader(header)


        destiny = mac_destiny
        
        # Checa se o receptor está com busy tone
        permissionToSend = False

        for x in self.busyToneList:

            if(destiny == x[0]):

                # Se receptor estiver livre, libera o pacote para emissão
                if(x[1] == 0):
                    permissionToSend = True
                else:
                    permissionToSend = False
        

            if( (permissionToSend == True) or (not len(self.busyToneList))):

                self.physicalLayer.broadcastGivenPackage(1,package)

    def sendPackage(self):
    

        if(len(self.physicalLayer.outputPackagesChannel1) != 0):

            destiny = self.physicalLayer.outputPackagesChannel1[0].headers[0].macDestiny
            
            # Checa se o receptor está com busy tone
            permissionToSend = False

            for x in self.busyToneList:

                if(destiny == x[0]):

                    # Se receptor estiver livre, libera o pacote para emissão
                    if(x[1] == 0):
                        permissionToSend = True
                    else:
                        permissionToSend = False
            

            if( (permissionToSend == True) or (not len(self.busyToneList))):

                if(self.sendCounter == 0):
                    self.sendCounter = self.physicalLayer.outputPackagesChannel1[0].sendTime
                    self.physicalLayer.broadcastPackage(1)
                else:
                    self.sendCounter-=1
    
    def sendBusyTone(self):

        # Create Link Layer Header
        header = Header(2,self.physicalLayer.mac,-1,-1,-1,-1,-1)

        # Create Package
        package = Package(self.busy,0)

        # Append Header to package
        package.appendHeader(header)

        # Send Package to Physical Layer
        self.physicalLayer.addPackage(package,2)
        self.physicalLayer.broadcastPackage(2)

    def checkBusy(self):

        if(self.physicalLayer.inputPackagesChannel1):

            self.busy = 1

        else:

            self.busy = 0


       # print("busy = ",self.busy)
        self.sendBusyTone()


    def readPackages(self):


        # Se houver pacotes normais
        if(self.physicalLayer.inputPackagesChannel1):

            self.busy = 1

            if(self.physicalLayer.inputPackagesChannel1[0].readTime == 0 ):
                    # Terminou de ler o  pacote
                
                package = self.physicalLayer.inputPackagesChannel1.pop(0)

                if(package.headers[0].macDestiny == self.physicalLayer.mac):
                    print(self.physicalLayer.mac, " leu ",package.dataLoad, " de ",package.headers[0].macOrigin)
                    #self.readyPackagesList.append(package)
            
                    # Libera o canal
                    self.busy = 0
            
            else:
                self.physicalLayer.inputPackagesChannel1[0].readTime-=1


        else:

            self.busy = 0


        self.sendBusyTone()


        # Se houver pacotes de busy tone
        while(self.physicalLayer.inputPackagesChannel2):

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

    def readNewPackages(self):
    

        # Se houver pacotes normais
        if(self.physicalLayer.inputPackagesChannel1):

            self.busy = 1

            if(self.physicalLayer.inputPackagesChannel1[0].readTime == 0 ):
                    # Terminou de ler o  pacote
                
                package = self.physicalLayer.inputPackagesChannel1.pop(0)


                self.readyPackagesList.append(package)
        
                # Libera o canal
                self.busy = 0
        
            else:
                self.physicalLayer.inputPackagesChannel1[0].readTime-=1

        else:

            self.busy = 0


        self.sendBusyTone()


        # Se houver pacotes de busy tone
        while(self.physicalLayer.inputPackagesChannel2):

            package = self.physicalLayer.inputPackagesChannel2.pop(0)

            found = False

            # Procura MAC na lista de Busy Tones
            for x in self.busyToneList:

                if(x[0] == package.headers[1].macOrigin):
                    x[1] = package.dataLoad
                    found = True
                
            if(found == False):

                x = [package.headers[1].macOrigin,package.dataLoad]
                self.busyToneList.append(x)
         
    def printPackage(self):

        for package in self.physicalLayer.inputPackagesChannel1:

            if( package.headers[1].macDestiny == self.physicalLayer.mac):
                print(package.dataLoad)

class NetworkLayer:

    def __init__(self,range,id,x,y):

        self.linkLayer = LinkLayer(x,y,range,id)

        self.packagesList = []

        self.routes = []


    def readPackage(self):

        self.linkLayer.readNewPackages()

        if(self.linkLayer.readyPackagesList):

            package = self.linkLayer.readyPackagesList.pop(0)
            header = package.headers[0]


            if (header.request == -1):

                print("Camada de Redes recebeu pacote de mensagem")
            
            elif (header.request == 0 ):

                print("Camada de Redes recebeu pacote de RREQ")

            elif (header.request == 1):

                print("Camada de Redes recebeu pacote de RREP")



            


    def addPackage(self,mac_destiny, message,time):

        package = Package(message,time)

        header = Header(1,-1,mac_destiny,-1,-1,-1,None)

        # Append Header to package
        package.appendHeader(header)

        self.packagesList.append(package)
        
    def sendPackage(self):

        if(self.packagesList):
            

            # Get package from list
            package = self.packagesList[0]

            # Check if host knows the route

            sequence = None
            for route in self.routes:
                if(route.destiny == package):
                    sequence = route.sequence


            # If there is a route, send data package
            if( sequence != None ):
                # Append Header to package
                package.updateSequence(sequence)
                self.linkLayer.sendNewPackage(package, package.headers[0].macDestiny)

            







        

