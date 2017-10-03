# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyQt_Gui\Widget_Ui_game_options.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Game_options(object):
    def setupUi(self, Game_options):
        Game_options.setObjectName("Game_options")
        Game_options.resize(400, 200)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Game_options.sizePolicy().hasHeightForWidth())
        Game_options.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(240, 240, 240))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        Game_options.setPalette(palette)
        self.verticalLayout = QtWidgets.QVBoxLayout(Game_options)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Game_options)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label)
        self.slider_object_size = QtWidgets.QSlider(Game_options)
        self.slider_object_size.setMinimum(1)
        self.slider_object_size.setMaximum(30)
        self.slider_object_size.setPageStep(3)
        self.slider_object_size.setProperty("value", 1)
        self.slider_object_size.setOrientation(QtCore.Qt.Horizontal)
        self.slider_object_size.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider_object_size.setTickInterval(3)
        self.slider_object_size.setObjectName("slider_object_size")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.slider_object_size)
        self.label_2 = QtWidgets.QLabel(Game_options)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.label_3 = QtWidgets.QLabel(Game_options)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.line_edit_name = QtWidgets.QLineEdit(Game_options)
        self.line_edit_name.setObjectName("line_edit_name")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.line_edit_name)
        self.slider_speed = QtWidgets.QSlider(Game_options)
        self.slider_speed.setMinimum(50)
        self.slider_speed.setMaximum(300)
        self.slider_speed.setProperty("value", 80)
        self.slider_speed.setOrientation(QtCore.Qt.Horizontal)
        self.slider_speed.setInvertedAppearance(True)
        self.slider_speed.setInvertedControls(False)
        self.slider_speed.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider_speed.setTickInterval(20)
        self.slider_speed.setObjectName("slider_speed")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.slider_speed)
        self.label_4 = QtWidgets.QLabel(Game_options)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(Game_options)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.line_edit_ip = QtWidgets.QLineEdit(Game_options)
        self.line_edit_ip.setObjectName("line_edit_ip")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.line_edit_ip)
        self.line_edit_port = QtWidgets.QLineEdit(Game_options)
        self.line_edit_port.setObjectName("line_edit_port")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.line_edit_port)
        self.verticalLayout.addLayout(self.formLayout)

        self.retranslateUi(Game_options)
        QtCore.QMetaObject.connectSlotsByName(Game_options)

    def retranslateUi(self, Game_options):
        _translate = QtCore.QCoreApplication.translate
        Game_options.setWindowTitle(_translate("Game_options", "Form"))
        self.label.setText(_translate("Game_options", "Object Size"))
        self.label_2.setText(_translate("Game_options", "Speed"))
        self.label_3.setText(_translate("Game_options", "Player Name"))
        self.label_4.setText(_translate("Game_options", "Server Adress"))
        self.label_5.setText(_translate("Game_options", "Default Port"))

