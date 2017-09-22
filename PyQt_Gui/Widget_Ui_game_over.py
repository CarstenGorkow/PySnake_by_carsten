# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyQt_Gui\Widget_Ui_game_over.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Game_over(object):
    def setupUi(self, Game_over):
        Game_over.setObjectName("Game_over")
        Game_over.resize(400, 300)
        self.verticalLayoutWidget = QtWidgets.QWidget(Game_over)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 9, 371, 281))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Game_over_text_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.Game_over_text_label.setText("")
        self.Game_over_text_label.setAlignment(QtCore.Qt.AlignCenter)
        self.Game_over_text_label.setObjectName("Game_over_text_label")
        self.verticalLayout.addWidget(self.Game_over_text_label)
        self.Button_wait_for_player = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_wait_for_player.setObjectName("Button_wait_for_player")
        self.verticalLayout.addWidget(self.Button_wait_for_player)
        self.Button_new_game = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_new_game.setObjectName("Button_new_game")
        self.verticalLayout.addWidget(self.Button_new_game)

        self.retranslateUi(Game_over)
        QtCore.QMetaObject.connectSlotsByName(Game_over)

    def retranslateUi(self, Game_over):
        _translate = QtCore.QCoreApplication.translate
        Game_over.setWindowTitle(_translate("Game_over", "Form"))
        self.Button_wait_for_player.setText(_translate("Game_over", "Wait For \n"
"New Player"))
        self.Button_new_game.setText(_translate("Game_over", "New Game"))

