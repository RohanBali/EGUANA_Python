from PyQt5.QtGui  import *
from PyQt5.QtGui import QLinearGradient
from PyQt5.Qt import *


class EguanaDefaultWidget(QWidget):

    def __init__(self, parent):

        super(EguanaDefaultWidget, self).__init__(parent)
        pal = QPalette()
        pal.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setAutoFillBackground(1)
        self.setPalette(pal)

    def presentWidget(self, widget):

        self.parent().setCentralWidget(widget)
