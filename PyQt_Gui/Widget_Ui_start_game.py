# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyQt_Gui\Widget_Ui_start_game.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Start_game(object):
    def setupUi(self, Start_game):
        Start_game.setObjectName("Start_game")
        Start_game.resize(400, 300)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Start_game.sizePolicy().hasHeightForWidth())
        Start_game.setSizePolicy(sizePolicy)
        self.verticalLayoutWidget = QtWidgets.QWidget(Start_game)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 381, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_game_name_text = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_game_name_text.setObjectName("label_game_name_text")
        self.horizontalLayout.addWidget(self.label_game_name_text)
        self.label_game_name = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_game_name.setText("")
        self.label_game_name.setObjectName("label_game_name")
        self.horizontalLayout.addWidget(self.label_game_name)
        self.label_player_rn_text = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_player_rn_text.setObjectName("label_player_rn_text")
        self.horizontalLayout.addWidget(self.label_player_rn_text)
        self.label_player_nr = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_player_nr.setText("")
        self.label_player_nr.setObjectName("label_player_nr")
        self.horizontalLayout.addWidget(self.label_player_nr)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.list_view_player = QtWidgets.QListView(self.verticalLayoutWidget)
        self.list_view_player.setObjectName("list_view_player")
        self.verticalLayout.addWidget(self.list_view_player)
        self.push_button_start_game = QtWidgets.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.push_button_start_game.sizePolicy().hasHeightForWidth())
        self.push_button_start_game.setSizePolicy(sizePolicy)
        self.push_button_start_game.setObjectName("push_button_start_game")
        self.verticalLayout.addWidget(self.push_button_start_game)

        self.retranslateUi(Start_game)
        QtCore.QMetaObject.connectSlotsByName(Start_game)

    def retranslateUi(self, Start_game):
        _translate = QtCore.QCoreApplication.translate
        Start_game.setWindowTitle(_translate("Start_game", "Form"))
        self.label_game_name_text.setText(_translate("Start_game", "Game name : "))
        self.label_player_rn_text.setText(_translate("Start_game", "Player Nr. :"))
        self.push_button_start_game.setText(_translate("Start_game", "Start Game"))

