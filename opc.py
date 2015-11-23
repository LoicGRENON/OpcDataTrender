# -*- coding: utf-8 -*-

from PyQt4 import QtCore
import OpenOPC

# OPC_PATH = "MyController.Application."
OPC_PATH = ""
# OPC_SERVER = "CODESYS.OPC.DA"
OPC_SERVER = "Matrikon.OPC.Simulation.1"


class OPCHandler:
    def __init__(self):
        self.client = OpenOPC.client()
        self.client.connect(OPC_SERVER)

    def __del__(self):
        self.client.close()

    def close(self):
        self.client.close()

    def write(self, itemList):
        for item in itemList:
            self.client.write(item)

    def readValue(self, var, defaultReturn=None):
        try:
            val = defaultReturn
            value, quality, _time = self.client.read(OPC_PATH + var)
            if quality == 'Good':
                val = value
        except OpenOPC.TimeoutError:
            val = defaultReturn
        except ValueError:
            val = defaultReturn
        return val

    def readInt(self, var):
        return self.readValue(var, 0)

    def readBool(self, var):
        return self.readValue(var, False)

    def readValues(self):
        return self.client.read(self.client.list(OPC_PATH))

    def showTrace(self, trace):
        print trace


class OPCReadingThread(QtCore.QThread):
    """
    OPCReadingThread is a thread that reads values from OPC server
    """
    dataReady = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.opc = OpenOPC.client()
        self.exiting = False

    def __del__(self):
        self.exiting = True
        self.wait()

    def run(self):
        self.exiting = False
        # TODO: catch exception (Unreachable OPC server, etc ...) and emit error signal
        self.opc.connect(OPC_SERVER)
        while not self.exiting:
            # tags = self.opc.list(OPC_PATH + "*")
            tags = self.opc.list(OPC_PATH + "Configured Aliases")
            # We use a group to avoid memory leaks : http://sourceforge.net/p/openopc/bugs/9/
            self.dataReady.emit(self.opc.read(tags, group="dummyGroup"))
            self.msleep(100)
        self.opc.close()
