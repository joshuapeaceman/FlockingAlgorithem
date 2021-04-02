import sys
from pathlib import Path
import pyqtgraph

from PyQt5 import QtCore
from PyQt5.QtCore import QThread

from src.gui import MainWindow
from src import FlockingWorker


class AppCtrl:
    def __init__(self):
        self.mainWindow = MainWindow.MainWindow(self.basePath())
        self.mainWindow.show()
        self.connect_signals()
        self.initialize_gui()

        self.plot = self.mainWindow.getPlot()

        self.mainPlot = None
        self.plot_init_flag = True

        self.flock_plot_data = []

        self.boids_cnt = 30
        self.boids_normal_movement_factor = 30
        self.boids_alignment_factor = 0
        self.boids_cohesion_factor = 0

        self.boids_separation_factor = 0
        self.distance_to_next_boid = 30
        self.slow_down_factor = 1
        self.frame_size = 1000


        self.flock_thread = QThread()
        self.flocking_worker = FlockingWorker.FlockingWorker(self)
        self.flocking_worker.timer.start()
        self.flocking_worker.plot_data_signal.connect(self.fill_flock)

        self.flocking_worker.moveToThread(self.flock_thread)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.updatePlot)




    def connect_signals(self):
        self.mainWindow.boids.valueChanged.connect(self.boids_cnt_setter)
        self.mainWindow.normal.valueChanged.connect(self.boids_normal_movement_factor_setter)
        self.mainWindow.alignment.valueChanged.connect(self.boids_alignment_factor_setter)
        self.mainWindow.cohesion.valueChanged.connect(self.boids_cohesion_factor_setter)
        self.mainWindow.separation.valueChanged.connect(self.boids_separation_factor_setter)
        self.mainWindow.distance.valueChanged.connect(self.boids_distance_setter)
        self.mainWindow.slow_down.valueChanged.connect(self.boids_slow_down_factor_setter)


        self.mainWindow.run_simulation.clicked.connect(self.run_simulation)

    def initialize_gui(self):
        self.boids_slow_down_factor_setter()
        self.boids_separation_factor_setter()
        self.boids_alignment_factor_setter()
        self.boids_cohesion_factor_setter()
        self.boids_cnt_setter()
        self.boids_normal_movement_factor_setter()
        self.boids_distance_setter()



    def boids_cnt_setter(self):
        self.boids_cnt = self.mainWindow.boids.value()
        self.mainWindow.boid_cnt.setText(str(self.boids_cnt))

    def boids_normal_movement_factor_setter(self):
        self.boids_normal_movement_factor = self.mainWindow.normal.value()
        self.mainWindow.movement_factor.setText(str(self.boids_normal_movement_factor))

    def boids_alignment_factor_setter(self):
        self.boids_alignment_factor = self.mainWindow.alignment.value() / 100
        self.mainWindow.alignment_factor.setText(str(self.boids_alignment_factor))

    def boids_cohesion_factor_setter(self):
        self.boids_cohesion_factor = self.mainWindow.cohesion.value() / 100
        self.mainWindow.cohesion_factor.setText(str(self.boids_cohesion_factor))

    def boids_separation_factor_setter(self):
        self.boids_separation_factor = self.mainWindow.separation.value() / 100
        self.mainWindow.separation_factor.setText(str(self.boids_separation_factor))

    def boids_distance_setter(self):
        self.distance_to_next_boid = self.mainWindow.distance.value()
        self.mainWindow.distance_factor.setText(str(self.distance_to_next_boid))

    def boids_slow_down_factor_setter(self):
        self.slow_down_factor = self.mainWindow.slow_down.value() / 10
        self.mainWindow.slow_down_factor.setText(str(self.slow_down_factor))

    def run_simulation(self):
        self.flock_thread.start()
        self.flocking_worker.createFlock(self.boids_cnt)
        self.flocking_worker.timer.start()
        self.timer.start()

    def fill_flock(self, flock):
        self.flock_plot_data = flock

    def updatePlot(self):
        if self.plot_init_flag:
            if self.flock_plot_data:
                self.pen = pyqtgraph.mkPen('y', width=3)
                self.mainPlot = self.plot.plot(self.flock_plot_data[0], self.flock_plot_data[1],
                                               name='Boids',
                                               pen=None,
                                               symbolPen=self.pen,
                                               symbol='o',
                                               symbolSize=5
                                               )
                self.plot_init_flag = False
        else:
            if self.flock_plot_data:
                self.mainPlot.setData(self.flock_plot_data[0], self.flock_plot_data[1])

    def basePath(self):
        path: str
        if getattr(sys, 'frozen', False):
            path = sys._MEIPASS
        elif __file__:
            path = Path(__file__).parent
        return path
