class PhysicalLayer:

    def __init__(self):
        self._package = ""
    def sendPackage(self,destination):
        destination._package = self._package

    def printPackage(self):
        print(self._package)