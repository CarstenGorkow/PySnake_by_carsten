#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys

from PyQt5 import QtGui 
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from PyQt5.QtWidgets import (QApplication,  QGraphicsScene,qApp,
                             QGraphicsView, QMainWindow, QPushButton)

from PyQt5.QtCore import Qt, QEvent, QTimer,QAbstractTableModel
import PyQt5
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

        self.start_server()
        self.start_client()
        self.start_timer()


    def init_events(self):
        self.pushButton_2.clicked.connect(self.show_open_new_game_dialog)
        #self.pushButton.clicked.connect(self.start_server)
        self.push_button_join.clicked.connect(self.show_open_games) 
        self.push_button_open_game.clicked.connect(self.open_new_game)


    def init_view(self):
        self.scene = QtWidgets.QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.widget_open_game.show()
        self.widget_join_game.show()


    # bubbelt den ganzen element baum hoch
    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            #if obj == self:
            #print("key_event",str(obj))
            #print(self)
            if event.key() == Qt.Key_Escape:
                self.close()
        return super(MyFirstGuiProgram, self).eventFilter(obj, event)

    
    def start_game(self):

        self.b_rect = self.graphicsView.mapToScene(self.graphicsView.viewport().geometry()).boundingRect()
        x1 =self.b_rect.x()
        y1 =self.b_rect.y()
        x2 =self.b_rect.x() + self.b_rect.width()
        y2 = self.b_rect.y()  +self.b_rect.height()
        print(x1,y1,x2,y2)

        #self.b_rect.getCoords(x1, y1, x2, y2)
        p = QtGui.QPen(QtGui.QColor(100,100,100))
        p.setWidth(5)
        l = QtWidgets.QGraphicsLineItem()
        l.setLine(x1,y1,x2,y2)
        l.setPen(p)
        self.scene.addItem(l)

    def start_server(self):
        thread = threading.Thread(target=self.start_server_bkg, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()     


    def start_server_bkg(self):
        """ creats a server for the game
        - the server must run in background and is unknown to the host/client/.."""
        Network.GameServer()


    def start_client(self):
        """ creats a client for the local player
        - must connect to the server"""
        self.client = Network.GameClient()
        self.client.connect_client()


    def start_timer(self):
        self.timer_queue_exec = QTimer(self)
        self.timer_queue_exec.timeout.connect(self._execute_queue_commands)
        self.timer_queue_exec.start(self.timer_queue_exec_interval)


    def show_open_new_game_dialog(self,hide=False):
        """ toggles the visibility of the dialog to open a new game"""
        if self.widget_open_game.isVisible() or hide == True:
            self.widget_open_game.hide()
        else:
            if not self.client.open_game_owner:
                self.widget_open_game.show()


    def show_open_games(self,hide=False):
        """toggels the visiblity of the dialog with open games on the server """
        if self.widget_join_game.isVisible() or hide == True:
            self.widget_join_game.hide()
        else:
            self.widget_join_game.show()
            self.add_entrys()


    def open_new_game(self):
        """ uses the client to create a new game on the server 
        the client automaticaly joins the game
        """
        game_name = self.line_edit_open_game.text()
        self.client.open_new_game(game_name)


    def _execute_queue_commands(self):
        """ execution of the commands stores in the queue 
        -> inifinite loop until listen is stoped with self.timer_queue_execution=False"""
        while not self.client.task_queue.empty():
                [client,queue_command] = self.client.task_queue.get()
                self._command_eval(client,queue_command)
                self.client.task_queue.task_done()


    def _command_eval(self,client_source,data_element_tree):
        """ private function to evaluate the command that are comming from the server
        """
        tree_dict = {}
        #tree_dict = data_element_tree.tree_dict
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
        game_dict = open_game_dict
        for game in game_dict:
            new_game = (game,game_dict[game][0])
            self.open_games.append(new_game)
            self.add_entrys()
        self.client.update_open_game_player_data(open_game_dict)


    def on_open_game_confirm(self,game_name):
        """ if the server sends the message that a game is opened, this methode is executed """
        self.show_open_games(False)
        self.show_open_new_game_dialog(False)
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




