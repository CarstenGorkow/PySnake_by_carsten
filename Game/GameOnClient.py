from PyQt5 import QtGui ,QtWidgets, QtCore,Qt

from PyQt5.QtCore import QTimer

import PyQt_Gui
import Game
import GrafikObjects
import time

class GameOnClient(Game.SnakeGame):
    """description of class"""

    signal_game_close = QtCore.pyqtSignal()    

    @QtCore.pyqtSlot(list)
    def eval_command_from_server(self, status):
        self.command_eval(status[0],status[1])
        self.t_server_list.append(status[2])
        self.t_treedict_list.append(status[3])

    @QtCore.pyqtSlot(int)
    def change_direction(self, key_int):
        dir = 0
        if key_int == QtCore.Qt.Key_W:
            dir = 1
        elif key_int == QtCore.Qt.Key_A:
            dir = 2
        elif key_int == QtCore.Qt.Key_S:
            dir = 3
        elif key_int == QtCore.Qt.Key_D:
            dir = 4
        self.on_data_to_server({"game":{"change_dir":dir}})


    def __init__(self,name,graphics_view,is_host,callback_data_to_server):
        super().__init__(name)
        self.graphics_view = graphics_view
        self.scene = self.graphics_view.scene()
        self.is_host = is_host
        self.callback_data_to_server = callback_data_to_server

        self.grafik_object_dict = {}

        self.timer.timeout.connect(self.gameLoop)
        self.timer_interval_listen = 50
        self._game_interval = 100
        
        self._line_width = 10

        # grafik items
        self.game_start_dialog = PyQt_Gui.Widget_Start_game()
        self.game_start_dialog.push_button_start_game.clicked.connect(self.start_game)
        self.game_start_dialog.push_button_close_game.clicked.connect(self.close_game)
        self.game_over_dialog = PyQt_Gui.Widget_Game_over()
        self.game_over_dialog.push_button_new_game.clicked.connect(self._on_new_game)
        self.game_over_dialog.push_button_close_game.clicked.connect(self.close_game)

        self.info_label_GUI = None

        self._fps = 0
        self._fps_temp = 0
        self._ping = 0
        self.timer_sec_ellapsed = QtCore.QTimer()  
        self.timer_sec_ellapsed.timeout.connect(self.on_sec_ellapsed)
        self.timer_sec_ellapsed.start(1000)
        self.t_server_list = []
        self.t_server = 0
        self.t_treedict_list = []
        self.t_treedict = 0

        self.init_view_size()


    # ================ properties ===================

    @property
    def game_interval(self):
        return self._game_interval
    
    @game_interval.setter
    def game_interval(self,value):
        self._game_interval = value
        self.on_data_to_server({"game":{"set_game_interval":self._game_interval}})

    @property
    def line_width(self):
        return self._line_width
    
    @line_width.setter
    def line_width(self,value):
        self._line_width = value
        self.set_graphics_view_size()

    # ======================= server game commands

    def command_eval(self,client,tree_dict):

        for command_key in tree_dict:
            if command_key == "set_field_size":
                self.set_field_size(tree_dict[command_key][0],tree_dict[command_key][1])
                self.init_view()
                self._insert_start_game_dialog()
            elif command_key == "player_coor":
                coor_dict = tree_dict[command_key]
                self.update_player_coordinates(coor_dict)
            elif command_key == "player_dir":
                self.update_player_direction(tree_dict[command_key])
            elif command_key == "grafik_objects":
                self.update_grafik_objects(tree_dict[command_key])
            elif command_key == "game_over":
                self.on_game_over()
            elif command_key == "reset_ready":
                self.init_view()
                self._on_game_is_ready()
            elif command_key == "hide_all_dialogs":
                self._hide_all_dialods()
            elif command_key == "close_game":
                self.on_game_close()
            else:
                print("ERROR - Gmae Client - Command key not knwon '%s'"%command_key)

    def update_player_coordinates(self,player_coor_dict):
        """ updating all player coordinates """
        self._fps_temp = self._fps_temp +1 
        pl_dict = {}
        for pl in self.player_list:
            pl_dict[pl.id] = pl
        for pl_name in player_coor_dict:
            if pl_name in pl_dict:
                pl_dict[pl_name].update_position(player_coor_dict[pl_name])


    def update_player_direction(self,player_dir_dict):
        """ function is executed on game start -> player chaned from hold to go """
        pl_dict = {}
        for pl in self.player_list:
            pl_dict[pl.name] = pl

        #for pl_name in player_dir_dict:
        #    if pl_name in pl_dict:
        #        pl_dict[pl_name].direction = player_dir_dict[pl_name]


    def update_grafik_objects(self,grafic_object_list):
        """ updates all objects in the object list with servser data """
        for obj_dict in grafic_object_list:
            name = obj_dict["name"]
            if name in self.grafik_object_dict:
                obj = self.grafik_object_dict[name]
                if obj.type == obj_dict["type"]:
                    pass
                else:
                    print("error")
            else:
                if obj_dict["type"] == "food":
                    obj = GrafikObjects.SnakeFood([0,0])
                    obj.name = obj_dict["name"]
                self.grafik_object_dict[name] = obj

            obj.set_point_list_fload(obj_dict["points"])
            obj.set_line_list_fload(obj_dict["lines"])
    # ======================= game preparation

    def init_view_size(self):
        """ init view as game owner -> send field size to server 
        ---> start timer <--- """
        # calculate field size
        self._calculate_field_size()
        #time.sleep(1)
        self.on_data_to_server({"game":{"start_game_on_hold":""}})


    def init_view(self):
        """ inti view, if field size is given """
        #self._set_field_size()
        self._insert_info_label()
        self.timer.start(self.timer_interval_listen)



    def _calculate_field_size(self):
        """ calculates the logical field size and sends to server """
        w = round( self.graphics_view.width() /self.line_width)
        h = round( self.graphics_view.height()/self.line_width)
        # send field size to server
        self.on_data_to_server({"game":{"set_field_size":[w,h]}})


    def set_field_size(self,w,h):
        res = super().set_field_size(w,h)
        self.graphics_view.centerOn(0,0)
        self.set_graphics_view_size()
        self.graphics_view.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.graphics_view.setSceneRect(QtCore.QRectF(0,0,100,100))
        self.graphics_view.update()
        self._update_size_dimension()
        return res


    def set_graphics_view_size(self):
        self.graphics_view.setFixedWidth (self.field_size.x()*self.line_width)
        self.graphics_view.setFixedHeight(self.field_size.y()*self.line_width)


    def _insert_start_game_dialog(self):
        """ insert start game dialog """

        #self.widget_game_options = PyQt_Gui.Widget_Game_options()
        #self.game_start_dialog_GUI = self.scene.addWidget(self.widget_game_options)
        #self.game_start_dialog_GUI.setPos(5,5)

        print( self.game_start_dialog.parent())
        self.game_start_dialog_GUI = self.scene.addWidget(self.game_start_dialog)
        x = self.x1+ self.w/2 - self.game_start_dialog.width()/2
        y = self.y1+ self.h/2 -  self.game_start_dialog.height()/2
        self.game_start_dialog_GUI.setPos(x,y)
        self.game_start_dialog.show()
        self.update_start_game_dialog()


    def _insert_info_label(self):
        """ insert label for devlope information """
        if self.info_label_GUI == None:
            self.info_label_GUI = self.scene.addText("")
        x = self.x1+self.w*0.8 
        y = self.y1+self.h*0.75
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
        print(" -> join game client "+self.name+" -> "+player.name)
        join_result = super().join_game(player)
        self.update_start_game_dialog()
        return join_result


    def start_game(self):
        """ executed if a game run is startet -> game loop already running """
        self.on_data_to_server({"game":{"go":""}})


    def _hide_all_dialods(self):
        """ hides all dialogs directly before the game starts"""
        self.game_start_dialog.hide()
        self.game_over_dialog.hide()


    def close_game(self):
        """ closes the game on the server"""
        self.on_data_to_server({"game":{"close_game":""}})

    # ======================= game over dialog
    def on_game_over(self):
        self.timer.stop()
        self.show_game_over_dialog()


    def show_game_over_dialog(self):
        """ called on game over - show dialog """
        self._insert_game_over_dialog()


    def _insert_game_over_dialog(self):
        """ insert start game dialog """        
        self.game_over_dialog_GUI = self.scene.addWidget(self.game_over_dialog)
        x = self.x1+ self.w/2 - self.game_over_dialog.width()/2
        y = self.y1+ self.h/2 -  self.game_over_dialog.height()/2
        self.game_over_dialog_GUI.setPos(x,y)
        self.game_over_dialog.show()
        #self.update_start_game_dialog()
        

    def _on_new_game(self):
        self.on_data_to_server({"game":{"reset":""}})
        

    def _on_game_is_ready(self):
        self.on_data_to_server({"game":{"start_game_on_hold":""}})
        self.on_data_to_server({"game":{"go":""}})


    def on_game_close(self):
        """ called if the server sends the signal to close the game """
        # clear screen
        self.scene.clear()
        # remove fixed canvas size
        self.graphics_view.setSizePolicy(QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        self.graphics_view.setMinimumSize(0,0)
        self.graphics_view.setMaximumSize(9999,9999)
        # send signal to client
        self.signal_game_close.emit()
        

    # ======================= game loop

    def gameLoop(self):
        if self.info_label_GUI != None:
            status_text =('Running              : %4i'%(self.step) + 
                          "\nServer signal time :  %3i"%(self.t_server) + 
                          "\nData tansform time :  %3i"%(self.t_treedict) +
                          "\nFPS                :  %3i"%(self._fps) )
            self.info_label_GUI.setPlainText(status_text)    
        self.step = self.step + 1
        #self.execute_queue_commands()
        self.plot_scene() 


    def plot_scene(self):
        """ plots all grafik objects in the viewport """

        transform2 = QtGui.QTransform()
        transform2.translate(self.x1,self.y1)

        for p in self.player_list:
            if p.item_group in self.scene.items():
                self.scene.removeItem(p.item_group)
                
            grafik_object = p.plot()
            grafik_object.setTransform(transform2)
            #grafik_object.setTransform(transform,True)
            self.scene.addItem(grafik_object)

        for name in self.grafik_object_dict:
            grafik_item = self.grafik_object_dict[name]
            if grafik_item.item_group in self.scene.items():
                self.scene.removeItem(grafik_item.item_group)

            grafik_object = grafik_item.plot()
            grafik_object.setTransform(transform2)
            self.scene.addItem(grafik_object)
        
        self.graphics_view.update()


    # ======================= sending data

    def on_data_to_server(self,data_dict):
        """ checks the data thats goes to the server """
        if self.callback_data_to_server != None:
            self.callback_data_to_server(data_dict)


    # ======================= network status
    def on_sec_ellapsed(self):
        self.t_server = 999 if len(self.t_server_list) == 0 else max(self.t_server_list)
        self.t_treedict = 999 if len(self.t_treedict_list) == 0 else max(self.t_treedict_list)
        
        self.t_server_list.clear()
        self.t_treedict_list.clear()

        self._fps = self._fps_temp
        self._fps_temp = 0