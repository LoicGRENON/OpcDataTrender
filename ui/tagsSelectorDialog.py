# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tagsSelectorDialog.ui'
#
# Created: Sat Nov 28 09:36:48 2015
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_tagsSelectorDialog(object):
    def setupUi(self, tagsSelectorDialog):
        tagsSelectorDialog.setObjectName(_fromUtf8("tagsSelectorDialog"))
        tagsSelectorDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        tagsSelectorDialog.resize(717, 468)
        tagsSelectorDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(tagsSelectorDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(tagsSelectorDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(tagsSelectorDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtGui.QLabel(tagsSelectorDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.avblItemsTreeView = QtGui.QTreeView(tagsSelectorDialog)
        self.avblItemsTreeView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.avblItemsTreeView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.avblItemsTreeView.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.avblItemsTreeView.setHeaderHidden(True)
        self.avblItemsTreeView.setObjectName(_fromUtf8("avblItemsTreeView"))
        self.gridLayout.addWidget(self.avblItemsTreeView, 1, 0, 1, 1)
        self.avblTagsListView = QtGui.QListView(tagsSelectorDialog)
        self.avblTagsListView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.avblTagsListView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.avblTagsListView.setObjectName(_fromUtf8("avblTagsListView"))
        self.gridLayout.addWidget(self.avblTagsListView, 3, 0, 2, 1)
        self.buttonBox = QtGui.QDialogButtonBox(tagsSelectorDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setFocusPolicy(QtCore.Qt.TabFocus)
        self.buttonBox.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setAutoFillBackground(False)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)
        self.tagsToReadListView = QtGui.QListView(tagsSelectorDialog)
        self.tagsToReadListView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tagsToReadListView.setViewMode(QtGui.QListView.ListMode)
        self.tagsToReadListView.setObjectName(_fromUtf8("tagsToReadListView"))
        self.gridLayout.addWidget(self.tagsToReadListView, 1, 1, 4, 1)

        self.retranslateUi(tagsSelectorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), tagsSelectorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), tagsSelectorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(tagsSelectorDialog)

    def retranslateUi(self, tagsSelectorDialog):
        tagsSelectorDialog.setWindowTitle(_translate("tagsSelectorDialog", "OpcDataTrender - Add tags", None))
        self.label.setText(_translate("tagsSelectorDialog", "Tags to read:", None))
        self.label_3.setText(_translate("tagsSelectorDialog", "Available tags:", None))
        self.label_2.setText(_translate("tagsSelectorDialog", "Available items in server:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    tagsSelectorDialog = QtGui.QDialog()
    ui = Ui_tagsSelectorDialog()
    ui.setupUi(tagsSelectorDialog)
    tagsSelectorDialog.show()
    sys.exit(app.exec_())

