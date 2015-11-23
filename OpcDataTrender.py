# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from opc import OPC_PATH, OPCHandler, OPCReadingThread
from ui.main import Ui_MainWindow
import OpenOPC
import sys


class OpcDataTrender(QtGui.QMainWindow):
    def __init__(self):
        super(OpcDataTrender, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        try:
            self.opc = OPCHandler()
        except OpenOPC.OPCError, error_msg:
            self.opc = None
            QtGui.QMessageBox.question(self.ui.centralwidget,
                                       u"OPC Error",
                                       u"Failed to open a connection to OPC server :\n%s" % error_msg,
                                       QtGui.QMessageBox.Ok)
            exit()

        ###########
        # Threads #
        ###########
        # OPC reading thread
        self.opcThread = OPCReadingThread()
        self.opcThread.dataReady.connect(self.getData, QtCore.Qt.QueuedConnection)
        # TODO: Start thread

        QtCore.QObject.connect(QtCore.QCoreApplication.instance(),
                               QtCore.SIGNAL("aboutToQuit()"),
                               self.quit)

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

    def onTimer(self):
        """
        Executed periodically when the monitor update time is fired
        :return:
        """
        self.updatePlot()

    def updatePlot(self):
        pass


def main():
    app = QtGui.QApplication(sys.argv)
    w = OpcDataTrender()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
