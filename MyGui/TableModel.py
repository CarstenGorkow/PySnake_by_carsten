import operator
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class TableModel(QAbstractTableModel):
    """ table to be shown in a QTabelView
    - helper class found in stackoverflow
    - base example for PySide
    https://stackoverflow.com/questions/19411101/pyside-qtableview-example
    - fix for Pyt5
    https://stackoverflow.com/questions/28660287/sort-qtableview-in-pyqt5
    """

    def __init__(self, parent, mylist, header, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.mylist = mylist
        self.header = header
    def rowCount(self, parent):
        return len(self.mylist)
    def columnCount(self, parent):
        if self.rowCount(parent) > 0:
            return len(self.mylist[0])
        else:
            return 1
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        elif role != Qt.DisplayRole:
            return None
        return self.mylist[index.row()][index.column()]
    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[col]
        return None
    def sort(self, col, order):
        """sort table by given column number col"""
        self.layoutAboutToBeChanged.emit()
        self.mylist = sorted(self.mylist, key=operator.itemgetter(col))        
        if order == Qt.DescendingOrder:
            self.mylist.reverse()
        self.layoutChanged.emit()
