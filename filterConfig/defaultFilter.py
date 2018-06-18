from filterConfig.eguanaFilter import EguanaFilters


class DefaultFilter(EguanaFilters):

    def __init__(self):

        super(EguanaFilters, self).__init__()
        self.name = "Default Filter"
