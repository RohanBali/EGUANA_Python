import os


class FilterManager:

    def __init__(self):

        self.supportedFilters = []
        for fileName in [name for name in os.listdir('./filterConfig') if os.path.isfile('./filterConfig/' + name) and not name == 'eguanaFilter.py' and name.endswith('.py')]:
            components = fileName.split('.')
            fileName = components[0]
            className = fileName[0].upper() + fileName[1:]
            try:
                module = __import__("filterConfig." + fileName, fromlist=["filterConfig."])
                classVar = getattr(module, className)
            except BaseException as e:
                print(str(e))
                continue
            self.supportedFilters.append(classVar())
