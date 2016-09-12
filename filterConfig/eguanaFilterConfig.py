import sys

import os, os.path
import json
from eguanaModel import EguanaModel

class EguanaFilterConfig():

    def __init__(self):
        self.name = ""
        self.headFilters = []
        self.jawFilters = []

    def filterButtonPressed(self):
        print("Head Filters\n")
        print(self.headFilters)
        print("Jaw Filters\n")
        print(self.jawFilters)



    def getFilename(self):
        fullPath =  sys.modules[self.__class__.__module__].__file__
        components = fullPath.split('/')
        return components[-1]