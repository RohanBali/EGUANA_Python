#singleton class
import os, os.path
import json
import sys

class EguanaModel(object):
    class __EguanaModel:
        def __init__(self):
            self.machine = None
            self.filterFunction = None
            self.filterTypeJaw = None
            self.filterTypeHead = None

        def getAllFilterFunctions(self):

            with open('config.json') as data_file:    
                data = json.load(data_file)

            filterFunctionFilenameList = data['allFilterFunctions']
            
            return filterFunctionFilenameList

        def getAllMachines(self):

            with open('config.json') as data_file:    
                data = json.load(data_file)

            machineFilenameList = data['allMachines']
            
            return machineFilenameList

        def getAllHeadFilterTypes(self):

            with open('config.json') as data_file:    
                data = json.load(data_file)

            headFilterList = data['allHeadFilterTypes']
            
            return headFilterList

        def getAllJawFilterTypes(self):

            with open('config.json') as data_file:    
                data = json.load(data_file)

            jawFilterList = data['allJawFilterTypes']
            
            return jawFilterList

        def getAllowedFilterFunctions(self):

            allowedFilterFunctions = []

            with open('config.json') as data_file:    
                data = json.load(data_file)


            className = self.machine.__class__.__name__
            fileName = className[0].lower() + className[1:] + '.py'

            for i in data:
                if i['machineName'] == fileName:
                    filterData = i['filterFunctions']
                    for j in filterData:
                        filterFunctionName = j['filterApplicationName']
                        allowedFilterFunctions.append(self.getFilterObjectFromFunctionName(filterFunctionName))

            return allowedFilterFunctions

        def getAllowedHeadFilterTypes(self):
            return self.getAllowedHeadFilterTypesForFilterFunction(self.filterFunction)
            

        def getAllowedHeadFilterTypesForFilterFunction(self,ffObject):

            headFilters = []

            with open('config.json') as data_file:    
                jsonData = json.load(data_file)


            machineClassName = EguanaModel().machine.__class__.__name__
            machineFileName = machineClassName[0].lower() + machineClassName[1:] + '.py'

            className = ffObject.__class__.__name__
            fileName = className[0].lower() + className[1:] + '.py'


            for i in jsonData:
                if i['machineName'] == machineFileName:
                    filterData = i['filterFunctions']
                    for j in filterData:
                            if j["filterApplicationName"] == fileName:
                                headFilters =  self.getFilterTypeObjectsFromTypeNameArray(j["filterTypes"]["headFilters"],'Head')

            return headFilters


        def getAllowedJawFilterTypes(self):
            
            return self.getAllowedJawFilterTypesForFilterFunction(self.filterFunction)


        def getAllowedJawFilterTypesForFilterFunction(self,ffObjects):
            
            jawFilters = []
            with open('config.json') as data_file:    
                jsonData = json.load(data_file)


            machineClassName = EguanaModel().machine.__class__.__name__
            machineFileName = machineClassName[0].lower() + machineClassName[1:] + '.py'

            className = ffObjects.__class__.__name__
            fileName = className[0].lower() + className[1:] + '.py'


            for i in jsonData:
                if i['machineName'] == machineFileName:
                    filterData = i['filterFunctions']
                    for j in filterData:
                            if j["filterApplicationName"] == fileName:
                                jawFilters = self.getFilterTypeObjectsFromTypeNameArray(j["filterTypes"]["jawFilters"],'Jaw')

            return jawFilters

    # helper methdos

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


        def getFilterFunctionObjectsFromFunctionNameArray(self,filterFunctionNameArray):
        
            filterFunctionObjectArray = []

            for filterFunctionName in filterFunctionNameArray:
                components = filterFunctionName.split('.')
                fileName = components[0]
                className = fileName[0].upper() + fileName[1:]
                module = __import__("filterConfig."+fileName,fromlist=["filterConfig."])                        
                classVar = getattr(module,className)
                classObject = classVar()
                filterFunctionObjectArray.append(classObject)
                
            return filterFunctionObjectArray     

        def getFilterObjectFromFunctionName(self,filterFunctionName):
            components = filterFunctionName.split('.')
            fileName = components[0]
            className = fileName[0].upper() + fileName[1:]
            module = __import__("filterConfig."+fileName,fromlist=["filterConfig."])                        
            classVar = getattr(module,className)
            classObject = classVar()
            return classObject

        def getMachineObjectFromMachineName(self,machineName):
            components = machineName.split('.')
            fileName = components[0]
            className = fileName[0].upper() + fileName[1:]
            module = __import__("machineConfig."+fileName,fromlist=["machineConfig."])                        
            classVar = getattr(module,className)
            classObject = classVar()
            return classObject



    instance = None

    def __new__(cls): # __new__ always a classmethod
        if not EguanaModel.instance:
            EguanaModel.instance = EguanaModel.__EguanaModel()
        return EguanaModel.instance
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)

    