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
        QtCore.QObject.connect(self.ui.tagsToReadListWidget,
                               QtCore.SIGNAL("customContextMenuRequested(const QPoint &)"),
                               self.displayContextMenu)

        for tag in currentItems:
            self.ui.tagsToReadListWidget.addItem(tag)
        self.populateAvblItemsTreeview()

    def getItems(self, parent=None):
        itemsList = []
        i = -1
        for i, item in enumerate(self.opc.client.list("*" if not parent else parent)):
            itemsList.append(item)
        return i + 1, itemsList

    def hasChildItems(self, parent):
        """
        Check if item has children
        :param parent: OPC tag
        :return: True if item has children else False
        """
        return True if len(self.opc.client.list(parent)) > 0 else False

    def getTags(self, item, parent):
        return [tag for tag in self.opc.client.list(u"%s.%s.*" % (parent, item))]

    def populateAvblItemsTreeview(self):
        model = QtGui.QStandardItemModel()
        self.ui.avblItemsTreeView.setModel(model)
        itemsNb, itemsList = self.getItems()
        for parent in itemsList:
            parentItem = QtGui.QStandardItem(parent)
            self.appendChildItems(parent, parentItem)
            model.appendRow(parentItem)

    def appendChildItems(self, parentPath, parentItem, itemsList=None):
        """

        :param parentPath: String
        :param parentItem: QStandardItem
        :param itemsList: List
        :return:
        """
        if itemsList is None:
            itemsNb, itemsList = self.getItems(parentPath)
        for child in itemsList:
            childPath = "%s.%s" % (parentPath, child)
            childItemsNb, childItemsList = self.getItems(childPath)
            # Check if item has children
            # If current item doesn't have any child, it's a tag and we skip it
            if childItemsNb > 0:
                childItem = QtGui.QStandardItem(child)
                childItem.setData(parentPath, QtCore.Qt.UserRole)
                parentItem.appendRow(childItem)
                self.appendChildItems(childPath, childItem, childItemsList)

    def onAvblItemsClicked(self, activatedItemIndex):
        model = QtGui.QStandardItemModel()
        self.ui.avblTagsListView.setModel(model)

        avblItemsModelIdx = self.ui.avblItemsTreeView.model().itemFromIndex(activatedItemIndex)
        item = avblItemsModelIdx.data(QtCore.Qt.DisplayRole).toString()
        itemPath = avblItemsModelIdx.data(QtCore.Qt.UserRole).toString()
        if itemPath != "":
            for tag in self.getTags(item, itemPath):
                path = "%s.%s." % (itemPath, item)
                tagWoPath = tag[len(path):]
                if len(tagWoPath) > 0:
                    tagItem = QtGui.QStandardItem(tagWoPath)
                    tagItem.setData(tag, QtCore.Qt.UserRole)
                    model.appendRow(tagItem)

    def onAvblTagsActivated(self, activatedTagIndex):
        avblTagsModelIdx = self.ui.avblTagsListView.model().itemFromIndex(activatedTagIndex)
        self.appendTagToList(avblTagsModelIdx.data(QtCore.Qt.UserRole).toString())

    def appendTagToList(self, tag):
        listWidget = self.ui.tagsToReadListWidget
        if len(listWidget.findItems(tag, QtCore.Qt.MatchExactly)) == 0:
            item = QtGui.QListWidgetItem(tag)
            item.setBackgroundColor(QtGui.QColor(255, 255, 127))
            listWidget.addItem(item)

    def displayContextMenu(self, position):
        selectedItems = self.ui.tagsToReadListWidget.selectedItems()
        if len(selectedItems) == 1:
            tag = selectedItems[0].text()
            menu = QtGui.QMenu()
            menu.addAction("&Change plot color", lambda: self.pickPlotColor(selectedItems[0], tag))
            menu.exec_(self.ui.tagsToReadListWidget.viewport().mapToGlobal(position))

    def pickPlotColor(self, listItem, tag):
        color = QtGui.QColorDialog.getColor()
        listItem.setBackground(color)


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
