import os, os.path
import json


class EguanaFilterConfig():

    def __init__(self):
    	self.name = ""
    	self.machineType = None
        self.headFilters = []
        self.jawFilters = []

    def setupMachineType(self,machineType):
        self.machineType = machineType
        self.setupAllowedFilterTypes()

    def filterButtonPressed(self):
        print("Head Filters\n")
        print(self.headFilters)
        print("Jaw Filters\n")
        print(self.jawFilters)
 
    def setupAllowedFilterTypes(self):

        with open('config.json') as data_file:    
            jsonData = json.load(data_file)


        machineClassName = self.machineType.__class__.__name__
        machineFileName = machineClassName[0].lower() + machineClassName[1:] + '.py'

        className = self.__class__.__name__
        fileName = className[0].lower() + className[1:] + '.py'


        for i in jsonData:
            if i['machineName'] == machineFileName:
                filterData = i['filterFunctions']
                for j in filterData:
                        if j["filterApplicationName"] == fileName:
                            self.headFilters = j["filterTypes"]["headFilters"]
                            self.jawFilters = j["filterTypes"]["jawFilters"]
