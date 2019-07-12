import os


class MachineManager:

    def __init__(self):

        self.supportedMachines = []
        for fileName in [name for name in os.listdir('./machineConfig') if os.path.isfile('./machineConfig/' + name) and not name == 'eguanaMachineConfig.py' and name.endswith('.py')]:
            components = fileName.split('.')
            fileName = components[0]
            className = fileName[0].upper() + fileName[1:]
            try:
                module = __import__("machineConfig." + fileName, fromlist=["machineConfig."])
                classVar = getattr(module, className)
            except:
                continue
            self.supportedMachines.append(classVar())
