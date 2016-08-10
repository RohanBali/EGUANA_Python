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
                            self.headFilters =  self.getFilterTypeObjectsFromTypeNameArray(j["filterTypes"]["headFilters"],'Head')
                            self.jawFilters = self.getFilterTypeObjectsFromTypeNameArray(j["filterTypes"]["jawFilters"],'Jaw')


    def getFilterTypeObjectsFromTypeNameArray(self,filterTypeNameArray,filterType):

        filterTypeObjectArray = []

        if filterType == 'Jaw':
            for filterTypeName in filterTypeNameArray:
                components = filterTypeName.split('.')
                fileName = components[0]
                className = fileName[0].upper() + fileName[1:]
                module = __import__("filterTypesConfig.jawFilters."+fileName,fromlist=["filterTypesConfig.jawFilters."])                        
                classVar = getattr(module,className)
                classObject = classVar()
                filterTypeObjectArray.append(classObject)
        else:
            for filterTypeName in filterTypeNameArray:
                components = filterTypeName.split('.')
                fileName = components[0]
                className = fileName[0].upper() + fileName[1:]
                module = __import__("filterTypesConfig.headFilters."+fileName,fromlist=["filterTypesConfig.headFilters."])                        
                classVar = getattr(module,className)
                classObject = classVar()
                filterTypeObjectArray.append(classObject)

        return filterTypeObjectArray

