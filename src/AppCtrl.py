import random
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
        self.frame_size = 1000



        self.flock_plot_data = [[], []]

        self.boids_cnt = 75

        self.boids_max_speed = 10
        self.boids_alignment_factor = 0.03
        self.boids_cohesion_factor = 0.19
        self.boids_separation_factor = 5.5
        self.boids_field_of_view_angle = 115
        self.distance_to_next_boid = 35
        self.slow_down_factor = 2.5







        self.plot_init_flag = True
        self.trace_boids = False
        self.add_lines = False


        self.trace_boids_cnt = 0

        self.trace_scipper = 10
        self.colors = ['b', 'y', 'g', 'r']

        self.flock_thread = QThread()
        self.flocking_worker = FlockingWorker.FlockingWorker(self)
        self.flocking_worker.timer.start()
        self.flocking_worker.plot_data_signal.connect(self.fill_flock)

        self.flocking_worker.moveToThread(self.flock_thread)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(2)
        self.timer.timeout.connect(self.updatePlot)

    def connect_signals(self):
        self.mainWindow.boids.valueChanged.connect(self.boids_cnt_setter)
        self.mainWindow.max_speed.valueChanged.connect(self.boids_max_speed_setter)
        self.mainWindow.alignment.valueChanged.connect(self.boids_alignment_factor_setter)
        self.mainWindow.cohesion.valueChanged.connect(self.boids_cohesion_factor_setter)
        self.mainWindow.separation.valueChanged.connect(self.boids_separation_factor_setter)
        self.mainWindow.distance.valueChanged.connect(self.boids_distance_setter)
        self.mainWindow.slow_down.valueChanged.connect(self.boids_slow_down_factor_setter)
        self.mainWindow.field_of_view_angle.valueChanged.connect(self.boids_field_of_view_angle_setter)
        self.mainWindow.trace_boids.stateChanged.connect(self.trace_boids_setter)
        self.mainWindow.add_lines.stateChanged.connect(self.add_lines_setter)

        self.mainWindow.run_simulation.clicked.connect(self.run_simulation)

    def initialize_gui(self):
        self.boids_slow_down_factor_setter()
        self.boids_separation_factor_setter()
        self.boids_alignment_factor_setter()
        self.boids_cohesion_factor_setter()
        self.boids_cnt_setter()
        self.boids_max_speed_setter()
        self.boids_distance_setter()
        self.boids_field_of_view_angle_setter()

    def trace_boids_setter(self):
        self.trace_boids = self.mainWindow.trace_boids.isChecked()

    def add_lines_setter(self):
        self.add_lines = self.mainWindow.add_lines.isChecked()

    def boids_cnt_setter(self):
        self.boids_cnt = self.mainWindow.boids.value()
        self.mainWindow.boid_cnt.setText(str(self.boids_cnt))

    def boids_max_speed_setter(self):
        self.boids_max_speed = self.mainWindow.max_speed.value()
        self.mainWindow.max_speed_factor.setText(str(self.boids_max_speed))

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

    def boids_field_of_view_angle_setter(self):
        self.boids_field_of_view_angle = self.mainWindow.field_of_view_angle.value() / 2
        self.mainWindow.field_of_view_angle_factor.setText(str(self.boids_field_of_view_angle * 2))

    def run_simulation(self):
        self.trace_boids_cnt = self.boids_cnt
        self.flock_plot_data[0].clear()
        self.flock_plot_data[1].clear()
        self.flock_thread.start()
        self.flocking_worker.createFlock(self.boids_cnt)
        self.flocking_worker.timer.start()
        self.timer.start()

    def fill_flock(self, flock):
        # activate/deactivate tracing boids
        if self.trace_boids:
            # skip adding data/frame for performance reasons
            if self.trace_scipper % 15 == 0:
                # very inefficient
                self.flock_plot_data[0][:0] = flock[0]
                self.flock_plot_data[1][:0] = flock[1]
                data_len = len(self.flock_plot_data[0])

                # after 10 frames/data points cut off the the last data set/frame
                if data_len >= self.trace_boids_cnt * 10:
                    del self.flock_plot_data[0][-self.trace_boids_cnt:]
                    del self.flock_plot_data[1][-self.trace_boids_cnt:]

        else:
            self.flock_plot_data[0] = flock[0]
            self.flock_plot_data[1] = flock[1]

        self.trace_scipper += 1

    def updatePlot(self):
        if self.plot_init_flag:
            if self.flock_plot_data:
                self.mainPlot = self.plot.plot(self.flock_plot_data[0], self.flock_plot_data[1],
                                               name='Boids',
                                               pen=None,
                                               symbolPen=pyqtgraph.mkPen('r', width=3),
                                               symbol='o',
                                               symbolSize=10
                                               )
                self.plot_init_flag = False
        else:
            if self.flock_plot_data:
                self.mainPlot.setData(self.flock_plot_data[0], self.flock_plot_data[1])
                # activate/deactivate lines between boids
                if self.add_lines:
                    self.mainPlot.setPen(pyqtgraph.mkPen(self.colors[random.randint(0, 3)], width=3))
                else:
                    self.mainPlot.setPen(None)

    def basePath(self):
        path: str
        if getattr(sys, 'frozen', False):
            path = sys._MEIPASS
        elif __file__:
            path = Path(__file__).parent
        return path
