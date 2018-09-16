from layers.physical import PhysicalLayer
from host import Host




#for x in range(50):
    #for y in range(50):
        #GLOBAL.coordinates.append((x,y))



a = Host(2,1,10,10)
b = Host(2,2,0,0)
c = Host(2,3,11,11)


a.checkNeighboors()
a.createPackage("Oi")
a.sendPackage()

b._physicalLayer.printPackage()
c._physicalLayer.printPackage()


    