from filterConfig.eguanaFilter import EguanaFilters


class SsFilter(EguanaFilters):

    def __init__(self):

        super(EguanaFilters, self).__init__()
        self.name = "Simple Substraction Filter"
