from filterConfig.eguanaFilter import EguanaFilters


class GoldFilter(EguanaFilters):

    def __init__(self):

        super(EguanaFilters, self).__init__()
        self.name = "Gold filter"
