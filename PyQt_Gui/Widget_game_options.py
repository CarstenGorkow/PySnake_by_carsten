
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtGui, QtWidgets,Qt

import PyQt_Gui

import MyGui


class Widget_Game_options(QDialog,PyQt_Gui.Ui_Game_options):
    """description of class"""

    def __init__(self,client):
        QDialog.__init__(self)
        PyQt_Gui.Ui_Game_options.__init__(self)
        self.setupUi(self)

        self.client = client
        self.slider_speed.valueChanged.connect(self.set_game_speed)
        self.slider_object_size.valueChanged.connect(self.set_object_size)
        self.line_edit_name.returnPressed.connect(self.set_player_name)
                

    def set_values(self,option_list):
        """options :  size,speed,player_name """
        if option_list[0] == None:
            self.slider_object_size.setEnabled(False)
        else:
            self.slider_object_size.setEnabled(True)
            self.slider_object_size.setValue(option_list[0])

        if option_list[1] == None:
            self.slider_speed.setEnabled(False)
        else:
            self.slider_speed.setEnabled(True)
            self.slider_speed.setValue(option_list[1])
        
        if option_list[2] == None:
            self.line_edit_name.setEnabled(False)
        else:
            self.line_edit_name.setEnabled(True)
            self.line_edit_name.setText(option_list[2])

        if option_list[3] == None:
            self.line_edit_ip.setEnabled(False)
        else:
            self.line_edit_ip.setEnabled(True)
            self.line_edit_ip.setText(option_list[3])

        

    def set_game_speed(self):
        print("value change",self.slider_speed.value())

    def set_object_size(self):
        print("value change",self.slider_object_size.value())
        
    def set_player_name(self):
        print("value cahnge",self.line_edit_name.text())


    def send_game_options(self):
        print("send all game options")

        if self.slider_object_size.isEnabled():
            self.client.set_line_width(self.slider_object_size.value())

        if self.slider_speed.isEnabled():
            self.client.set_game_speed(self.slider_speed.value())

        if self.line_edit_name.isEnabled():
            self.client.set_player_name(self.line_edit_name.text())

        if self.line_edit_ip.isEnabled():
            self.client.set_server_ip(self.line_edit_ip.text())

