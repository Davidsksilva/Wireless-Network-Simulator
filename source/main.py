from layers import PhysicalLayer
from host import Host

a = Host(6,1,10,10)
b = Host(6,2,12,12)
c = Host(6,3,11,11)



a.createPackage(3, "Hello from A",2)
b.createPackage(3, "Hello from B",2)



time_counter = 0

while True:
    print("------------")
    print("Time = ",time_counter)
    print("------------")
    
    a.networkLayer.readPackage()
    a.networkLayer.sendPackage()
    c.networkLayer.linkLayer.checkBusy()
    a.networkLayer.linkLayer.checkBusy()
    b.networkLayer.linkLayer.checkBusy()

    b.networkLayer.readPackage()
    b.networkLayer.sendPackage()
    c.networkLayer.linkLayer.checkBusy()
    a.networkLayer.linkLayer.checkBusy()
    b.networkLayer.linkLayer.checkBusy()

    c.networkLayer.readPackage()
    c.networkLayer.sendPackage()
    a.networkLayer.linkLayer.checkBusy()
    b.networkLayer.linkLayer.checkBusy()

    time_counter = time_counter + 1

    if(time_counter == 10):
        break
   # a.linkLayer.readPackages()
    #a.linkLayer.sendPackage()
    #c.linkLayer.checkBusy()

    #b.linkLayer.readPackages()
    #b.linkLayer.sendPackage()
    #c.linkLayer.checkBusy()

    #c.linkLayer.readPackages()
    #c.linkLayer.sendPackage()





    