from physical import PhysicalLayer
from host import Host

a = Host(2,1,10,10)
b = Host(2,2,0,0)
c = Host(2,3,11,11)

a.createPackage("Oi")
a.sendPackage()

b._physicalLayer.printPackage()
c._physicalLayer.printPackage()


    