class Header:


    def __init__(self, type, mac_origin, mac_destiny, number,request,sequenceNumber, sequenceList):
            
        # Header Camada de Enlace
        if ( type == 0 ):

            self.type = 0
            self.macOrigin = mac_origin
            self.macDestiny = mac_destiny
            self.number = number


        # Header Camada de Rede
        elif( type == 1 ):

            self.type = 1
            self.macDestiny = mac_destiny
            self.request = request # 0 RREQ, 1 RREP
            self.sequenceNumber = sequenceNumber
            self.sequenceList = sequenceList

        # Header Busy Tone
        elif (type == 2):

            self.type = 2
            self.macOrigin = mac_origin

class Package:

    def __init__(self, data_load, time):

        self.dataLoad = data_load
        self.headers =[]
        self.sendTime = time
        self.readTime = time

    def appendHeader(self, header):

        self.headers.append(header)

    def getLinkHeader(self):

        for header in self.headers:
            if(header.type == 0):
                print("achou")
                return header

    #return self.headers[0]

    def getNetworkHeader(self):

        for header in self.headers:
            if(header.type == 1):
                return header


    

    