#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys

from PyQt5 import QtGui 
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import Qt

from PyQt5.QtWidgets import (QApplication,  QGraphicsScene,qApp,
                             QGraphicsView, QMainWindow, QPushButton)

from PyQt5.QtCore import QTimer,QAbstractTableModel
from PyQt5.Qt import QListWidgetItem


import PyQt_Gui
import GrafikObjects
import Network
import threading
import MyGui
import Game
import time

""" ================ Access to the home network ======================

1
down vote
Step 1: Run this command "python -m SimpleHTTPServer". Note that python -m SimpleHTTPServer works only with python 2. With python 3, you should use: python -m http.server

Step 2: Edit your router's configuration to forward port 8000 to the computer on which you ran the python command.

Step 3: Determine your home network's IP address, for example, 203.0.113.47

One convenient way to determine your home network's IP address is to consult any of the what-is-my-ip websites, for example https://www.whatismyip.com/.

Step 4: From outside your network, visit (for example) http://203.0.113.47:8000/
"""

"""
QThread* somethread = new QThread(this);
QTimer* timer = new QTimer(0); //parent must be null
timer->setInterval(1);
timer->moveToThread(somethread);
//connect what you want
somethread->start();


pip install pyinstaller
pinstaller --onefile StartPySnake.py    


"""



class MyFirstGuiProgram(QMainWindow,PyQt_Gui.Ui_MainWindow):
    

    def __init__(self,dialog):
        #super(MyFirstGuiProgram, self).__init__(None)  
        QMainWindow.__init__(self)
        PyQt_Gui.Ui_MainWindow.__init__(self)
        self.setupUi(dialog)
        self.app = None

        qApp.installEventFilter(self)
        
        self.open_games= []
        self.timer_queue_exec_interval = 200

        self.init_events()
        self.init_view()

        self.client = Network.GameClient(self)
        self.client.signal_status_message.connect(self.set_status_message)
        self.client.signalCommand.connect(self.eval_command_from_server)
        self.client.color = Qt.QColor("#ff0000")
        self.update_color()
        self.client.connect_client()

        #self.widget_open_game.hide()
        self.widget_join_game.hide()

        self.widget_game_options = None


    def init_events(self):
        self.push_button_open_new_game_dialog.clicked.connect(self.toggle_visibility_open_new_game_dialog)
        self.push_button_start_server.clicked.connect(self.start_server)
        self.push_button_open_games_dialog.clicked.connect(self.toggle_visibility_open_games) 
        self.push_button_open_game.clicked.connect(self.open_new_game)
        self.push_button_join_game.clicked.connect(self.join_game)
        self.push_button_color_select.clicked.connect(self.color_picker)
        self.push_button_options.toggled.connect(self.show_options)


    def init_view(self):
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.widget_open_game.show()
        self.widget_join_game.show()
        

    # bubbelt den ganzen element baum hoch
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            #if event_key() == QtCore.Qt.Key_W:
            if obj == self.scene:
                self.client.prozess_key_event(event.key())

            if event.key() == QtCore.Qt.Key_Escape:
                self.close()
        return super(MyFirstGuiProgram, self).eventFilter(obj, event)
            

    def start_server(self):
        thread = threading.Thread(target=self.start_server_bkg, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()     
        self.set_status_message("Start Server on this client!")


    def start_server_bkg(self):
        """ creats a server for the game
        - the server must run in background and is unknown to the host/client/.."""
        Network.GameServer()


    def start_client(self):
        """ creats a client for the local player
        - must connect to the server"""
        if self.client !=  None and not self.client.is_connected():
                self.client.connect_client()


    def toggle_visibility_open_new_game_dialog(self,hide=True):
        """ toggles the visibility of the dialog to open a new game"""
        if self.widget_open_game.isVisible() or hide == True:
            self.widget_open_game.hide()
        else:
            if not self.client.open_game_owner:
                self.widget_open_game.show()


    def toggle_visibility_open_games(self,hide=False):
        """toggels the visiblity of the dialog with open games on the server """
        self.start_client()
        if self.widget_join_game.isVisible() or hide == True:
            self.widget_join_game.hide()
        else:
            self.open_games_table.setSelectionBehavior(QtWidgets.QTableView.SelectRows)
            self.widget_join_game.show()
            self.client.request_open_games()


    @QtCore.pyqtSlot(bool)  #<<== the missing link
    def show_options(self,checked): 
        """ opens the menu with game optiones """
        if checked:
            if self.widget_game_options == None:
                self.widget_game_options = PyQt_Gui.Widget_Game_options(self.client)
                #self.widget_game_options.slider_speed.sliderReleased.connect(self.test)
                self.verticalLayout_3.addWidget(self.widget_game_options)
            self.widget_game_options.set_values(self.client.get_game_options())
            self.widget_game_options.show()
        elif not checked:
            self.widget_game_options.hide()
            self.widget_game_options.send_game_options()


    def open_new_game(self):
        """ uses the client to create a new game on the server 
        the client automaticaly joins the game
        """
        self.start_client()
        game_name = self.line_edit_open_game.text()
        self.client.open_new_game(game_name)


    def join_game(self):
        """ sends a request to the server to join the game """
        indexes = self.open_games_table.selectionModel().selectedRows()

        if len(indexes) == 0:
            self.set_status_message(" -> no game selected")
        else:
            selected_row= indexes[0]
            m = self.open_games_table.model()
            index = m.index(selected_row.row(),0)
            game_name = m.data(index)
            self.set_status_message(" -> connecting to game : "+game_name)
            self.toggle_visibility_open_games(True)
            self.toggle_visibility_open_new_game_dialog(True)
            self.app.processEvents(QtCore.QEventLoop.AllEvents)
            self.client.start_game_grafik_interface(game_name,self.graphicsView)


    @QtCore.pyqtSlot(list)
    def eval_command_from_server(self, status):
        self._command_eval(status[0],status[1])


    def _command_eval(self,client_source,data_element_tree):
        """ private function to evaluate the command that are comming from the server
        """
        tree_dict = {}
        tree_dict = data_element_tree

        for command_key in tree_dict:
            if command_key == "open_games":
                self.update_all_open_games(tree_dict[command_key])
            elif command_key == "game_was_opened":
                self.client.open_game_owner = True
                self.on_open_game_confirm(tree_dict[command_key])
            else:
                print("ERROR - Server - Command key not knwon '%s'"%command_key)


    def update_all_open_games(self,open_game_dict):
        """ updates the open games list """
        self.open_games.clear()
        for game in open_game_dict:
            new_game = (game,len(open_game_dict[game]))
            self.open_games.append(new_game)
        self.add_entrys()
        self.client.update_open_game_player_data(open_game_dict)


    def on_open_game_confirm(self,game_name):
        """ if the server sends the message that a game is opened, this methode is executed """
        self.toggle_visibility_open_games(True)
        self.toggle_visibility_open_new_game_dialog(True)
        self.app.processEvents(QtCore.QEventLoop.AllEvents)
        self.client.start_game_grafik_interface(game_name,self.graphicsView)

        # show grafik game
        # -> etra class for graifik game derifed from Qobject
        # -> game loop is run inside this object


    def add_entrys(self):
#        data_list = [('XYLENES', 139.1)]
        header = ['Game Name', 'Player']
        table_model = MyGui.TableModel(self, self.open_games, header)
        self.open_games_table.setModel(table_model)
        self.open_games_table.resizeColumnsToContents()
        # enable sorting
        self.open_games_table.setSortingEnabled(True)

 
    def color_picker(self):
        color = QtWidgets.QColorDialog.getColor()
        self.client.color=color
        self.update_color()


    def update_color(self):
        """ updates the grafik items that are connected to the player color"""

        #self.push_button_color_select.setStyleSheet("color: %s"%"#ffffff")
        r = self.client.color.red()
        g = self.client.color.green()
        b = self.client.color.blue()
        col_sum = r+g+b
        text_color = "#ffffff" if col_sum < 650 else "#000000"
        ss_command = "background-color: %s; color: %s"%(self.client.color.name(),text_color)
        self.push_button_color_select.setStyleSheet(ss_command)


    def set_status_message(self,message):
        self.label_fooder.setText(message)




"""
game logic for server client connection
- GUI -> with client
-> client -> connected to server
-> listens to server -> filles command queue
-> when is the queue executed? -> execution timer in GUI (QTimer)
"""


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    #dialog = QtWidgets.QDialog()
    # to use a central widget
    dialog = QtWidgets.QMainWindow()

    prog = MyFirstGuiProgram(dialog)
    prog.app = app
    #prog.do()

    dialog.show()
    sys.exit(app.exec_())




