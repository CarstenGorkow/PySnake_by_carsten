#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys

import Snake_main_window as design

from PyQt5 import QtGui 
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import PyQt5

#from PyQt5 import QtCore, QtGui, QtWidgets
#from firstgui import Ui_myfirstgui
 
class MyFirstGuiProgram(design.Ui_MainWindow):
    def __init__(self, dialog):
        design.Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
 
        # Connect "add" button with a custom function (addInputTextToListbox)
        #self.addBtn.clicked.connect(self.addInputTextToListbox)
 
    #def addInputTextToListbox(self):
    #    txt = self.myTextInput.text()
    #    self.listWidget.addItem(txt)
 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    #dialog = QtWidgets.QDialog()
    # to use a central widget
    dialog = QtWidgets.QMainWindow()

    prog = MyFirstGuiProgram(dialog)

    dialog.show()
    sys.exit(app.exec_())


#class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
#    def __init__(self, parent=None):
#        super(ExampleApp, self).__init__(parent)
#        self.setupUi(self)

#def main():
#    app = QtGui.QApplication(sys.argv)
#    form = ExampleApp()
#    form.show()
#    app.exec_()


