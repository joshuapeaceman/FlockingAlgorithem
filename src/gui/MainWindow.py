"""MainGUI Class"""
import os

import pyqtgraph
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow


class MainWindow(QMainWindow):

    def __init__(self, basePath):
        super().__init__()
        uic.loadUi(os.path.join(basePath, 'gui', 'MainWindow.ui'), self)
        self.graphWidget = pyqtgraph.PlotWidget()
        self.graphWidget.setAspectLocked(1)
        self.mainFrame.addWidget(self.graphWidget)

    def getPlot(self):
        return self.graphWidget
