from PyQt5 import QtGui ,QtWidgets, QtCore,Qt

from PyQt5.QtCore import QTimer

import PyQt_Gui
import Game

class GameOnClient(Game.SnakeGame):
    """description of class"""

    @QtCore.pyqtSlot(list)
    def updateCommand(self, status):
        #print(QtCore.QThread.currentThreadId(),"signal  thread ")
        #print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",status)
        self.command_eval(status[0],status[1])


    def __init__(self,name,graphics_view,is_host,callback_data_to_server):
        super().__init__(name)
        self.graphics_view = graphics_view
        self.scene = self.graphics_view.scene()
        self.is_host = is_host
        self.callback_data_to_server = callback_data_to_server

        print(QtCore.QThread.currentThreadId(),"client game thread ")

        self.timer.timeout.connect(self.gameLoop)

        # grafik items
        self.game_start_dialog = None
        self.info_label_GUI = None

        self.init_view_size()


    def command_eval(self,client,tree_dict):
        #print("game on client - command eval : ",tree_dict)

        for command_key in tree_dict:
            if command_key == "set_field_size":
                self.set_field_size(tree_dict[command_key][0],tree_dict[command_key][1])
                self.init_view()
            elif command_key == "player_coor":
                coor_dict = tree_dict[command_key]
                self.update_player_coordinates(coor_dict)
            elif command_key == "player_dir":
                self.update_player_direction(tree_dict[command_key])
            else:
                print("ERROR - Server - Command key not knwon '%s'"%key)

    # ======================= game preparation

    def init_view_size(self):
        """ init view as game owner -> send field size to server 
        ---> start timer <--- """
        # calculate field size
        self._calculate_field_size()
        self.on_data_to_server({"game":{"start_game_on_hold":""}})


    def init_view(self):
        """ inti view, if field size is given """
        self._set_field_size()
        self._insert_start_game_dialog()
        self._insert_info_label()
        self.timer.start(250)


    def _calculate_field_size(self):
        """ calculates the logical field size and sends to server """
        w = round( self.graphics_view.width() /self.line_width)
        h = round( self.graphics_view.height()/self.line_width)
        #print("initial view size :  %i %i"%(w,h))
        # send field size to server
        self.on_data_to_server({"game":{"set_field_size":[w,h]}})


    def _set_field_size(self):
        """ sets the real size of the field widget """
        self.graphics_view.setFixedWidth (self.field_size.x()*self.line_width)
        self.graphics_view.setFixedHeight(self.field_size.y()*self.line_width)
        self.graphics_view.centerOn(0,0)
        self.graphics_view.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.graphics_view.setSceneRect(QtCore.QRectF(0,0,100,100))
        self.graphics_view.update()

        self._update_size_dimension()
        #print("%i %i %i %i %i %i"%(self.x1,self.y1,self.x2,self.y2,self.h,self.w))


    def _insert_start_game_dialog(self):
        """ insert start game dialog """
        self.game_start_dialog = PyQt_Gui.Widget_Start_game()
        self.game_start_dialog_GUI = self.scene.addWidget(self.game_start_dialog)
        x = self.x1+ self.w/2 - self.game_start_dialog.width()/2
        y = self.y1+ self.h/2 -  self.game_start_dialog.height()/2
        self.game_start_dialog_GUI.setPos(x,y)
        self.game_start_dialog.push_button_start_game.clicked.connect(self.start_game)
        self.update_start_game_dialog()


    def _insert_info_label(self):
        """ insert label for devlope information """
        self.info_label_GUI = self.scene.addText("")
        x = self.x1+self.w*0.90 
        y = self.y1+self.h*0.95
        self.info_label_GUI.setPos(x,y)
        self.graphics_view.update()


    def _update_size_dimension(self):
        """ saves the corner points and size of the viewport to a game variable """
        self.b_rect = self.graphics_view.mapToScene(self.graphics_view.viewport().geometry()).boundingRect()
        self.x1 =self.b_rect.x()
        self.y1 =self.b_rect.y()
        self.x2 =self.b_rect.x() + self.b_rect.width()
        self.y2 = self.b_rect.y()  +self.b_rect.height()
        self.h = self.b_rect.height()
        self.w = self.b_rect.width()


    def update_start_game_dialog(self):
        if self.game_start_dialog != None:
            self.game_start_dialog.label_game_name.setText(self.name)
            self.game_start_dialog.push_button_start_game.setEnabled(self.is_host)
            self.game_start_dialog.update_player_list(self.player_list)


    def join_game(self, player):
        join_result = super().join_game(player)
        self.update_start_game_dialog()
        return join_result


    def start_game(self):
        """ executed if a game run is startet -> game loop already running """
        self.game_start_dialog.hide()
        self.on_data_to_server({"game":{"go":""}})


    def gameLoop(self):
        #print(self.step)
        if self.info_label_GUI != None:
            status_text = 'Running '+str(self.step)
            self.info_label_GUI.setPlainText(status_text)    
        self.step = self.step + 1
        self.execute_queue_commands()
        self.plot_scene()


    #def timerEvent(self, e):
    #    print(self.step)
    #    if self.info_label_GUI != None:
    #        status_text = 'Running '+str(self.step)
    #        self.info_label_GUI.setPlainText(status_text)    
    #    self.step = self.step + 1
    #    print("r")
    #    self.execute_queue_commands()
    #    self.plot_scene()

    # -> qeueue is not reached -> ceate signal -> more dicevt and ?faster?
    # -> no event loop on client -> not running case background thread
    def execute_queue_commands(self):
        """ execution of the commands stores in the queue e"""
        while not self.task_queue.empty():
            [client,queue_command] = self.task_queue.get()
            print("x",queue_command)
            self.command_eval(client,queue_command)
            self.task_queue.task_done()


    def update_player_coordinates(self,player_coor_dict):
        """ updating all player coordinates """
        pl_dict = {}
        for pl in self.player_list:
            pl_dict[pl.name] = pl

        for pl_name in player_coor_dict:
            pl_dict[pl_name].update_position(player_coor_dict[pl_name])


    def update_player_direction(self,player_dir_dict):
        """ function is executed on game start -> player chaned from hold to go """
        pl_dict = {}
        for pl in self.player_list:
            pl_dict[pl.name] = pl

        for pl_name in player_dir_dict:
            pl_dict[pl_name].direction = player_dir_dict[pl_name]


    def plot_scene(self):
        """ plots all grafik objects in the viewport """

        transform = QtGui.QTransform()
        transform.scale(self.line_width,self.line_width)

        transform2 = QtGui.QTransform()
        transform2.translate(self.x1,self.y1)

        for p in self.player_list:
            if p.item_group in self.scene.items():
                self.scene.removeItem(p.item_group)
            grafik_object = p.draw_object()
            grafik_object.setTransform(transform2)
            grafik_object.setTransform(transform,True)
            self.scene.addItem(grafik_object)
        self.graphics_view.update()

    # ======================= sending data

    def on_data_to_server(self,data_dict):
        """ checks the data thats goes to the server """
        if self.callback_data_to_server != None:
            self.callback_data_to_server(data_dict)