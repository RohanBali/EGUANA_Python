from eguana_base_widget import EguanaDefaultWidget
from PyQt5.QtGui import *
from PyQt5.Qt import *
import math
from machineManager import MachineManager
from filterManager import FilterManager

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class EguanaMainWidget(EguanaDefaultWidget):

    def __init__(self, parent):

        super(EguanaMainWidget, self).__init__(parent)
        self.machineManger = MachineManager()
        self.layout = QGridLayout(self)
        self.layout.setSpacing(50)
        self.layout.setContentsMargins(50, 50, 50, 50)
        numDevices = len(self.machineManger.supportedMachines)
        numColumns = 3

        for i in range(numDevices):
            device = self.machineManger.supportedMachines[i]
            self.faceCheckButton = QPushButton(device.machineName,self)
            self.faceCheckButton.clicked.connect(lambda state, x=i: self.machineButtonPressed(x))
            self.faceCheckButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.layout.addWidget(self.faceCheckButton, int(i / numColumns), i % numColumns)

        self.setLayout(self.layout)

    def machineButtonPressed(self, index):

        machineClassObj = self.machineManger.supportedMachines[index]
        folderPath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if folderPath != '' and machineClassObj.isDirectoryValid(folderPath):
            machine_widget = EguanaMachineWidget(self.parent(), machineClassObj, folderPath)
            self.presentWidget(machine_widget)


class EguanaMachineWidget(EguanaDefaultWidget):

    def __init__(self, parent, machine, folderPath):

        super(EguanaMachineWidget, self).__init__(parent)
        self.selectedFiltersList = []
        self.filterConfigurationList = []
        self.filterManagerInstance = FilterManager()
        self.layout = QGridLayout(self)
        self.layout.setSpacing(50)
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.allFiltersListWidget = QListWidget(self)
        for i in range(len(self.filterManagerInstance.supportedFilters)):
            filterObject = self.filterManagerInstance.supportedFilters[i]
            self.allFiltersListWidget.addItem(filterObject.name)
        self.addFilterButton = QPushButton('>', self)
        self.addFilterButton.clicked.connect(self.addFilterButtonPressed)

        self.removeFilterButton = QPushButton('<', self)
        self.removeFilterButton.clicked.connect(self.removeFilterButtonPressed)

        self.selectedFiltersListWidget = QListWidget(self)
        self.layout.addWidget(self.allFiltersListWidget, 1, 0, 2, 1)
        self.layout.addWidget(self.addFilterButton, 1, 1)
        self.layout.addWidget(self.removeFilterButton, 2, 1)
        self.layout.addWidget(self.selectedFiltersListWidget, 1, 2, 2, 1)

        self.addFilterConfigurationButton = QPushButton('+', self)
        self.addFilterConfigurationButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(self.addFilterConfigurationButton, 1, 3, 2, 1)

        self.selectedFilterConfigurationListWidget = QListWidget(self)
        self.layout.addWidget(self.selectedFilterConfigurationListWidget, 3, 0, 1, 4)


        self.addFilterConfigurationButton.clicked.connect(self.addFilterConfigurationButtonPressed)

        title = machine.machineName + ' ' + folderPath
        titleLabel = QLabel(title, self)
        titleLabel.setAlignment(Qt.AlignLeft)
        self.layout.addWidget(titleLabel, 0, 0, 1, 4)
        self.setLayout(self.layout)

    def addFilterButtonPressed(self):

        indexList = self.allFiltersListWidget.selectedIndexes()
        if len(indexList) > 0:
            index = indexList[0]
            filterObject = self.filterManagerInstance.supportedFilters[index.row()]
            self.selectedFiltersList.append(filterObject)
            self.reloadSelectList()

    def removeFilterButtonPressed(self):

        indexList = self.selectedFiltersListWidget.selectedIndexes()
        if len(indexList) > 0:
            index = indexList[0]
            del self.selectedFiltersList[index.row()]
            self.reloadSelectList()

    def reloadSelectList(self):

        self.selectedFiltersListWidget.clear()
        for i in range(len(self.selectedFiltersList)):
            filterObject = self.selectedFiltersList[i]
            self.selectedFiltersListWidget.addItem(filterObject.name)

    def addFilterConfigurationButtonPressed(self):

        if len(self.selectedFiltersList) > 0:
            self.filterConfigurationList.append(self.selectedFiltersList)
            self.selectedFiltersList = []
            self.reloadSelectList()

        self.selectedFilterConfigurationListWidget.clear()
        for i in range(len(self.filterConfigurationList)):
            filterConfigString = ''
            answer = alphabet[i]
            filterConfigString += answer
            filterConfigString += ' ------> '
            filterList = self.filterConfigurationList[i]
            for j in range(len(filterList)):
                filterConfigString += filterList[j].name
                if j != len(filterList) - 1:
                    filterConfigString += ' + '
            self.selectedFilterConfigurationListWidget.addItem(filterConfigString)

    # self.checkManagerInstance = checkManagerInstance
    # checkLabel = QLabel("CHECKS",self)
    # checkLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred);
    # checkLabel.setAlignment(Qt.AlignCenter);
    # checkLabel.setStyleSheet("font-weight: 100; font-size: 50px; color: white;");
    # self.layout.addWidget(checkLabel,0,0,1,3)
    # self.faceCheckButton = QPushButton("Face Checks",self)
    # self.faceCheckButton.clicked.connect(self.faceCheckButtonPressed)
    # if (self.checkManagerInstance.faceChecksPassed == 1):
    #   self.faceCheckButton.setStyleSheet("border:5px solid #006400; font-weight: 600; font-size: 30px; color: white;");
    # else:
    #   self.faceCheckButton.setStyleSheet("border:5px solid #FF0000; font-weight: 600; font-size: 30px; color: white;");
    # self.faceCheckButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding);
    # self.layout.addWidget(self.faceCheckButton,1,0)
    # self.gazeCheckButton = QPushButton("Gaze Checks",self)
    # self.gazeCheckButton.clicked.connect(self.gazeCheckButtonPressed)
    # self.gazeCheckButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding);
    # if (self.checkManagerInstance.gazeChecksPassed  == 1):
    #   self.gazeCheckButton.setStyleSheet("border:5px solid #006400; font-weight: 600; font-size: 30px; color: white;");
    # else:
    #   self.gazeCheckButton.setStyleSheet("border:5px solid #FF0000; font-weight: 600; font-size: 30px; color: white;");
    # self.layout.addWidget(self.gazeCheckButton,1,1)
    # self.calibrationCheckButton = QPushButton("Calibration Checks",self)
    # self.calibrationCheckButton.clicked.connect(self.calibrationCheckButtonPressed)
    # self.calibrationCheckButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding);
    # if (self.checkManagerInstance.calibrationChecksPasssed  == 1):
    #   self.calibrationCheckButton.setStyleSheet("border:5px solid #006400; font-weight: 600; font-size: 30px; color: white;");
    # else:
    #   self.calibrationCheckButton.setStyleSheet("border:5px solid #FF0000; font-weight: 600; font-size: 30px; color: white;");
    # self.layout.addWidget(self.calibrationCheckButton,1,2)
    # logLabel = QLabel("LOGS",self)
    # logLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred);
    # logLabel.setAlignment(Qt.AlignCenter);
    # logLabel.setStyleSheet("font-weight: 100; font-size: 50px; color: white;");
    # self.layout.addWidget(logLabel,2,0,1,3)
    # if (self.checkManagerInstance.gazeLogCreated == 1 and self.checkManagerInstance.faceLogCreated == 1):
    #   logCreatedLabel = QLabel("Logs Created",self)
    #   logCreatedLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding);
    #   logCreatedLabel.setAlignment(Qt.AlignCenter);
    #   logCreatedLabel.setStyleSheet("font-weight: 100; font-size: 30px; color: white;");
    #   self.layout.addWidget(logCreatedLabel,3,0,1,3)
    # else:
    #   self.createLogButton = QPushButton("Create Logs",self)
    #   self.createLogButton.clicked.connect(self.createLogsButtonPressed)
    #   self.createLogButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding);
    #   self.layout.addWidget(self.createLogButton,3,0,1,3)
