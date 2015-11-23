# coding=utf-8

from PyQt4 import QtGui
from ui.aboutDialog import Ui_aboutDialog


class MyAboutDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_aboutDialog()
        self.ui.setupUi(self)
