#Importing AscE
import sys
sys.path.insert(0, './__AscE__')
import AscE
from AscE_Components import *
#Importing AscE ^

class ExampleComponent(Component):
    def __init__(self):
        self.ExampleVariable = 0
        Component.__init__(self, dependancies=[Transform()])
    def OnUpdate(self):
        self.ExampleFunction()
    def OnAwake(self):
        pass
    def ExampleFunction(self):
        self.ExampleVariable += 1
