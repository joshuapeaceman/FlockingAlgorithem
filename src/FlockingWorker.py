from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSignal

from src import Boid


class FlockingWorker(QObject):
    plot_data_signal = pyqtSignal(tuple)

    def __init__(self, ctrl):
        QObject.__init__(self, parent=None)

        self.ctrl = ctrl
        self.flock = {}
        self.timer = QtCore.QTimer()
        self.timer.setInterval(2)
        self.timer.timeout.connect(self.update_boids)

    def createFlock(self, number_of_boids):
        self.flock.clear()
        for _ in range(number_of_boids):
            self.flock.update({_: Boid.Boid(self.ctrl, self.flock)})

    def stop(self):
        pass

    def update_boids(self):
        for idx, val in enumerate(self.flock):
            self.flock[val].update()
        self.translate_flock_position_data_to_plot_data()

    def translate_flock_position_data_to_plot_data(self):
        data = ([], [])
        for idx, val in enumerate(self.flock):
            data[0].append(self.flock[val].x)
            data[1].append(self.flock[val].y)
        self.plot_data_signal.emit(data)
