# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from opc import OPC_PATH, OPCHandler, OPCReadingThread
from ui.main import Ui_MainWindow
from MyAboutDialog import MyAboutDialog
import pyqtgraph as pg
import OpenOPC
import sys
import datetime
import time


class OpcDataTrender(QtGui.QMainWindow):
    def __init__(self):
        super(OpcDataTrender, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.aboutDialog = MyAboutDialog(self)

        self.samplesX = []
        self.samplesY = []

        try:
            self.opc = OPCHandler()
        except OpenOPC.OPCError, error_msg:
            self.opc = None
            QtGui.QMessageBox.question(self.ui.centralwidget,
                                       u"OPC Error",
                                       u"Failed to open a connection to OPC server :\n%s" % error_msg,
                                       QtGui.QMessageBox.Ok)
            exit()

        self.timer = QtCore.QTimer()
        self.startTimestamp = 0

        ###########
        # Threads #
        ###########
        # OPC reading thread
        self.opcThread = OPCReadingThread()
        self.opcThread.dataReady.connect(self.getData, QtCore.Qt.QueuedConnection)

        QtCore.QObject.connect(self.ui.actionAbout,
                               QtCore.SIGNAL("triggered()"),
                               self.aboutDialog.open)

        QtCore.QObject.connect(QtCore.QCoreApplication.instance(),
                               QtCore.SIGNAL("aboutToQuit()"),
                               self.quit)

        QtCore.QObject.connect(self.ui.startBtn,
                               QtCore.SIGNAL("clicked()"),
                               self.onStart)
        QtCore.QObject.connect(self.ui.stopBtn,
                               QtCore.SIGNAL("clicked()"),
                               self.onStop)
        QtCore.QObject.connect(self.ui.updateKnob,
                               QtCore.SIGNAL('valueChanged(int)'),
                               self.onRefreshRateChange)
        QtCore.QObject.connect(self.timer,
                               QtCore.SIGNAL('timeout()'),
                               self.onTimer)

    def __del__(self):
        if self.opc:
            self.opc.close()

    def quit(self):
        """
        Called when app is about to quit
        """
        pass

    def closeEvent(self, event):
        """
        Exit confirmation
        """
        event.ignore()
        if QtGui.QMessageBox.Yes == QtGui.QMessageBox.question(self.ui.centralwidget,
                                                               u"Exit",
                                                               u"Are you sure to quit ?",
                                                               QtGui.QMessageBox.No | QtGui.QMessageBox.Yes):
            event.accept()

    def getData(self, data):
        for _i, (item, value, _quality, _timestamp) in enumerate(data):
            if item == OPC_PATH + u"itemName1":
                pass
            elif item == OPC_PATH + u"itemName2":
                pass
            elif item == u".testData":
                if self.isActive():
                    try:
                        self.samplesY.append(int(value))
                        self.samplesX.append((time.clock() - self.startTimestamp) / 1.0)
                    except TypeError:
                        pass
        self.ui.statusbar.showMessage(u"Last received data : %s" % datetime.datetime.now().strftime("%H:%M:%S.%f"))

    def onRefreshRateChange(self, value):
        if self.timer.isActive():
            updateFreq = float(value) / 10.0
            self.timer.setInterval(1000.0 * updateFreq)

    def onStart(self):
        self.samplesX = []
        self.samplesY = []
        self.startTimestamp = time.clock()

        self.opcThread.start(QtCore.QThread.TimeCriticalPriority)

        updateFreq = float(self.ui.updateKnob.value()) / 10.0
        self.timer.start(1000.0 * updateFreq)

    def onStop(self):
        self.timer.stop()
        self.opcThread.exiting = True

    def isActive(self):
        return self.timer.isActive()

    def onTimer(self):
        """
        Executed periodically when the monitor update time is fired
        :return:
        """
        print "Timer timeout"
        self.updatePlot()

    def updatePlot(self):
        self.ui.plot.clear()

        c = pg.PlotDataItem({'x': self.samplesX,
                             'y': self.samplesY},
                            pen="r")
        print self.samplesX
        print self.samplesY
        self.ui.plot.addItem(c)
        self.ui.plot.repaint()


def main():
    app = QtGui.QApplication(sys.argv)
    w = OpcDataTrender()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
