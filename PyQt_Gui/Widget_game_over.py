
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtGui, QtWidgets,Qt

import PyQt_Gui

import MyGui


class Widget_Game_over(QDialog,PyQt_Gui.Ui_Game_over):
    """description of class"""

    def __init__(self):
        QDialog.__init__(self)
        PyQt_Gui.Ui_Game_over.__init__(self)
        self.setupUi(self)
        self._palyer_list = []
        
