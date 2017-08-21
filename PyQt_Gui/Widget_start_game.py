
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtGui, QtWidgets,Qt

import PyQt_Gui

import MyGui


class Widget_Start_game(QDialog,PyQt_Gui.Ui_Start_game):
    """description of class"""

    def __init__(self):
        QDialog.__init__(self)
        PyQt_Gui.Ui_Start_game.__init__(self)
        self.setupUi(self)
        self._palyer_list = []
        

    def update_player_list(self,player_list):
        self._palyer_list = player_list.copy()

        list_entrys = [pl.name for pl in player_list]
        self.label_player_nr.setText(str(len(list_entrys)))

        model = QtCore.QStringListModel(list_entrys)
        self.list_view_player.setModel(model)
        self.list_view_player.setSelectionMode(QtWidgets.QListView.NoSelection)
        self.list_view_player.setEditTriggers(QtWidgets.QListWidget.NoEditTriggers)
