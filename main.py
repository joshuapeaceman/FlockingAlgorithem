import sys
import traceback

import pyqtgraph
from PyQt5 import QtWidgets

from src import AppCtrl


if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        appCtrl = AppCtrl.AppCtrl()


        sys.exit(app.exec_())
    except:
        traceback.print_exc()


