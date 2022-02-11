from PyQt5 import QtWidgets, QtGui, QtCore
import sys
from math import sin, cos, pi
import simpy.rt
import model

import ui_main
import pyqtgraph
from threading import Thread, Lock

class ExampleApp(QtWidgets.QMainWindow, ui_main.Ui_MainWindow):
    signal = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        pyqtgraph.setConfigOption('background', 'w') #before loading widget
        pyqtgraph.setConfigOption('antialias', True)
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)

        self.mainTh = Thread(target=self.simTh)
        self.objPoint = []

        self.grPlot.plotItem.showGrid(True, True, 0.7)
        self.grPlot.plotItem.getViewBox().setMouseEnabled(False,False)
        self.grPlot.setYRange(-10, 10)
        self.grPlot.setXRange(-10, 10)
        self.grPlot.getPlotItem().getAxis('top').setFixedHeight(25)
        self.grPlot.getPlotItem().getAxis('bottom').setFixedHeight(25)
        self.grPlot.getPlotItem().getAxis('left').setFixedWidth(25)
        self.grPlot.getPlotItem().getAxis('right').setFixedWidth(25)
        self.grPlot.sceneObj.sigMouseClicked.connect(self.setPoint)

        self.signal.connect(self.draw)

        # model object
        self.mdl = model.model([45*pi/180, 45*pi/180])

        self.mainTh.start()

    def simulation(self, env):
        tm = 0
        while True:
            self.mdl.integrate([0, 0])

            if tm > 0.1:
                self.signal.emit()
                tm = 0

            tm = tm + self.mdl.dt
            yield env.timeout(self.mdl.dt)

    def simTh(self):
        # simulation environment
        self.env = simpy.rt.RealtimeEnvironment(factor=1, strict=0)
        # simulation process definition
        proc = self.env.process(self.simulation(self.env))
        # simulation start
        self.env.run()

    def draw(self):
        points = self.mdl.kinematics()
        pen1 = pyqtgraph.mkPen(color='g', width=10)
        self.grPlot.plotItem.plot(points[0], points[1], pen=pen1, clear=True)
        if len(self.objPoint) > 0:
            self.grPlot.plot([self.objPoint[0]], [self.objPoint[1]], pen=None, symbol='o')

    def setPoint(self, event):
        point = self.grPlot.getPlotItem().getViewBox().mapSceneToView(event.scenePos())
        self.objPoint = [point.x(), point.y()]
        th = self.mdl.inverseKin(self.objPoint)
        self.mdl.setPos([th[0][0], th[1][0]])


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    form.update() #start with something
    app.exec_()
    print("DONE")
