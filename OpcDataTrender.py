# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from opc import OPC_PATH, OPCHandler, OPCReadingThread
from ui.main import Ui_MainWindow
from MyAboutDialog import MyAboutDialog
from TagSelectorDialog import TagSelectorDialog
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

        self.samples = []

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

        QtCore.QObject.connect(self.ui.actionAddTag,
                               QtCore.SIGNAL("triggered()"),
                               self.addTag)
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

    def addTag(self):
        currentItems = [sample['tagName'] for sample in self.samples]
        d = TagSelectorDialog(self.opc, currentItems=currentItems)
        r = d.exec_()
        if r == QtGui.QDialog.Accepted:
            self.samples = []
            listWidget = d.ui.tagsToReadListWidget
            for i in xrange(listWidget.count()):
                self.samples.append({'tagName': u"%s" % listWidget.item(i).text(),
                                     'plotColor': listWidget.item(i).backgroundColor(),
                                     'x': [],
                                     'y': []})

    def getData(self, data):
        if self.isActive():
            for _i, (item, value, _quality, _timestamp) in enumerate(data):
                try:
                    for sample in self.samples:
                        if sample['tagName'] == item:
                            sample['y'].append(int(value))
                            sample['x'].append((time.clock() - self.startTimestamp) / 1.0)
                            break
                    # else:
                    #     self.samples.append({'item': item,
                    #                          'x': [(time.clock() - self.startTimestamp) / 1.0],
                    #                          'y': [int(value)]})
                except TypeError:
                    pass
        self.ui.statusbar.showMessage(u"Last received data : %s" % datetime.datetime.now().strftime("%H:%M:%S.%f"))

    def onRefreshRateChange(self, value):
        if self.timer.isActive():
            updateFreq = float(value) / 10.0
            self.timer.setInterval(1000.0 * updateFreq)

    def onStart(self):
        # Stop previous thread
        self.onStop()

        self.opcThread.items = []
        for sample in self.samples:
            self.opcThread.items.append(sample['tagName'])
            # Init samples values
            sample['x'] = []
            sample['y'] = []

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
        self.updatePlot()

    def updatePlot(self):
        self.ui.plot.clear()

        for sample in self.samples:
            c = pg.PlotDataItem({'x': sample['x'],
                                 'y': sample['y']},
                                pen=sample['plotColor'])
            self.ui.plot.addItem(c)
        self.ui.plot.repaint()


def main():
    app = QtGui.QApplication(sys.argv)
    w = OpcDataTrender()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
