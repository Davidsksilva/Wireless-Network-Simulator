
class Header:


    def __init(self, type, mac):

        # Header Camada Física
        if( type == 0 ): 

            self.type = 0
            self.mac = mac
            
            

        # Header Camada de Enlace
        elif ( type == 1 ):

            self.type = 1

        # Header Camada de Rede
        elif( type == 2 ):

            self.type = 2



class Package:

    def __init__(self):

        self.dataLoad = ""

        self.headers =[]

    def addHeader(self, header):

        self.headers.append(header)

    

    