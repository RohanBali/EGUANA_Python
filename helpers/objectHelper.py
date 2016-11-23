def getJawFilterNameFromJawFilterFilename(jawFilterFilename):
    components = jawFilterFilename.split('.')
    fileName = components[0]
    className = fileName[0].upper() + fileName[1:]

    module = __import__("filterTypesConfig.jawFilters."+fileName,fromlist=["filterTypesConfig.jawFilters."])                        
    classVar = getattr(module,className)
    return classVar.name    
                    

def getHeadFilterNameFromHeadFilterFilename(headFilterFilename):
    components = headFilterFilename.split('.')
    fileName = components[0]
    className = fileName[0].upper() + fileName[1:]

    module = __import__("filterTypesConfig.headFilters."+fileName,fromlist=["filterTypesConfig.headFilters."])                        
    classVar = getattr(module,className)
    return classVar.name    


def getModuleNameFromModuleFilename(moduleFilename):
    components = moduleFilename.split('.')
    fileName = components[0]
    className = fileName[0].upper() + fileName[1:]

    module = __import__("moduleConfig."+fileName,fromlist=["moduleConfig."])                        
    classVar = getattr(module,className)
    return classVar.name    


def getMachineNameFromMachineFilename(machineFilename):
    components = machineFilename.split('.')
    fileName = components[0]
    className = fileName[0].upper() + fileName[1:]

    module = __import__("machineConfig."+fileName,fromlist=["machineConfig."])                        
    classVar = getattr(module,className)
    return classVar.name    

