# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from ui.tagsSelectorDialog import Ui_tagsSelectorDialog


class TagSelectorDialog(QtGui.QDialog):
    def __init__(self, opc, parent=None, currentItems=None):
        super(TagSelectorDialog, self).__init__(parent)
        self.ui = Ui_tagsSelectorDialog()
        self.ui.setupUi(self)

        self.opc = opc

        QtCore.QObject.connect(self.ui.avblItemsTreeView,
                               QtCore.SIGNAL("clicked(QModelIndex)"),
                               self.onAvblItemsClicked)
        QtCore.QObject.connect(self.ui.avblTagsListView,
                               QtCore.SIGNAL("activated(QModelIndex)"),
                               self.onAvblTagsActivated)

        if currentItems:
            #self.populateTagToReadListView()
            model = QtGui.QStandardItemModel()
            self.ui.tagsToReadListView.setModel(model)
            for tag in currentItems:
                model.appendRow(QtGui.QStandardItem(tag))
        self.populateAvblItemsTreeview()

    def getItems(self, parent=None):
        if not parent:
            return [item for item in self.opc.client.list("*")]
        else:
            return [item for item in self.opc.client.list(parent)]

    def getTags(self, item, parent):
        return [tag for tag in self.opc.client.list(u"%s.%s.*" % (parent, item))]

    def populateAvblItemsTreeview(self):
        model = QtGui.QStandardItemModel()
        self.ui.avblItemsTreeView.setModel(model)
        for parent in self.getItems():
            parentItem = QtGui.QStandardItem(parent)
            self.appendChildItems(parent, parentItem)
            model.appendRow(parentItem)

    def appendChildItems(self, parent, parentItem):
        for child in self.getItems(parent):
            childItem = QtGui.QStandardItem(child)
            childItem.setData(parent, QtCore.Qt.UserRole)
            parentItem.appendRow(childItem)
            self.appendChildItems(child, childItem)

    def onAvblItemsClicked(self, activatedItemIndex):
        model = QtGui.QStandardItemModel()
        self.ui.avblTagsListView.setModel(model)

        avblItemsModelIdx = self.ui.avblItemsTreeView.model().itemFromIndex(activatedItemIndex)
        item = avblItemsModelIdx.data(QtCore.Qt.DisplayRole).toString()
        itemPath = avblItemsModelIdx.data(QtCore.Qt.UserRole).toString()
        if itemPath != "":
            for tag in self.getTags(item, itemPath):
                tagItem = QtGui.QStandardItem(tag)
                tagItem.setData(itemPath, QtCore.Qt.UserRole)
                model.appendRow(tagItem)

    def onAvblTagsActivated(self, activatedTagIndex):
        avblTagsModelIdx = self.ui.avblTagsListView.model().itemFromIndex(activatedTagIndex)
        parent = avblTagsModelIdx.data(QtCore.Qt.UserRole).toString()
        tag = avblTagsModelIdx.data(QtCore.Qt.DisplayRole).toString()
        self.appendTagToList("%s.%s" % (parent, tag))

    def appendTagToList(self, tag):
        model = self.ui.tagsToReadListView.model()
        if not model:
            model = QtGui.QStandardItemModel()
            self.ui.tagsToReadListView.setModel(model)

        # Check if tag is in list before append it
        for rowIdx in xrange(model.rowCount()):
            if model.data(model.index(rowIdx, 0), QtCore.Qt.DisplayRole).toString() == tag:
                return False  # Tag not added
        model.appendRow(QtGui.QStandardItem(tag))
        return True  # Tag added


class OPCNode:
    def __init__(self, parent=None):
        self.parent = parent
        self.path = None
        self.tags = []
        self.childItems = []

if __name__ == '__main__':
    import sys
    from opc import OPCHandler
    app = QtGui.QApplication(sys.argv)
    w = TagSelectorDialog(OPCHandler())
    w.open()
    sys.exit(app.exec_())
