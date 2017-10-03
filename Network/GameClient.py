
from PyQt5 import QtCore
import time
import socket

import Network
import Game


class GameClient(Network.Client):
    """description of class"""

    signalCommandGame = QtCore.pyqtSignal(list)
    signalKeyEvent= QtCore.pyqtSignal(int)

    def __init__(self,parent):
        Network.Client.__init__(self,parent)
        self._name = "player1"
        self.open_games = []
        self._open_game_owner  = False
        self.callback_on_game_start = None
        self.game = None
        self._color = None
    
    # ================ properties ===================

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self,value):
        self._color = value
        self.send_player_data()


    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self,value):
        self._name = value
        self.send_player_data()


    @property
    def open_game_owner(self):
        return self._open_game_owner

    @open_game_owner.setter
    def open_game_owner(self,val):
        self._open_game_owner = val
        # should be empty -> not used in the current version
        if self.callback_on_game_start != None: self.callback_on_game_start()

    # ================ methodes ===================

    def send_player_data(self):
        """ sending client data to the server """
        if self.client_wrap != None:
            self.client_wrap.send_msg({"client_data":{"name":self.name,"color":self.color.name()}})
    

    def connect_client(self):
        super().connect_client()
        self.send_player_data()


    def open_new_game(self,game_name):
        """ send an open new game command to the server """
        if self.client_wrap != None:
            self.client_wrap.send_msg({"open_game":game_name})


    def request_open_games(self):
        if self.client_wrap != None:
            self.client_wrap.send_msg({"get_open_games":""})


    def on_send_game_data_to_server(self,msg_dict):
        """ =========== >>> durch signal ersetzen """
        self.client_wrap.send_msg(msg_dict)


    def put_task_to_queue(self, task):
        """ task redirecting of server data
        -> overwritten from parent class 
        -> running on background threat """
        tree_dict = task[1]

        if "time" in tree_dict:
            send_ms = int((tree_dict["time"]-time.time())*1000)
            tree_dict.pop("time")

        if "game" in tree_dict.keys():
            # signal to GameOnClient
            self.signalCommandGame.emit([task[0],tree_dict["game"],self.client_wrap.t_server,self.client_wrap.t_treedict])
            tree_dict.pop("game")
        if len(tree_dict) > 0 :
            super().put_task_to_queue(task)
    

    def start_game_grafik_interface(self,game_name,graphics_view):
        """ creats game object """
        self.game = Game.GameOnClient(game_name,graphics_view,self.open_game_owner,self.on_send_game_data_to_server)
        self.signalCommandGame.connect(self.game.eval_command_from_server)
        self.signalKeyEvent.connect(self.game.change_direction)
        self.game.signal_game_close.connect(self.on_close_game)
        self.client_wrap.send_msg({"join_game":game_name})


    def on_close_game(self):
        """ called if the server sends the message that the game was closed """
        # remove signals
        #self.signalCommandGame.remove(self.game.eval_command_from_server)
        #self.signalKeyEvent.remove(self.game.change_direction)
        # remove flag for game owner
        self.open_game_owner = False
        # message label 
        self.signal_status_message.emit("Game %s was closed."%self.game.name)
        self.game = None



    def update_open_game_player_data(self,open_game_dict):
        """ if a game is open then, update the player information 
        - removes player that are not in the list from game
        - adds player that are in the list, but not in the game """

        if isinstance(self.game,Game.GameOnClient):
            for ga in open_game_dict:
                if ga == self.game.name:
                    self.game.consolidate_player(open_game_dict[ga])
            self.game.update_start_game_dialog()


    def prozess_key_event(self,key_int):
        """ emits the keypress event to the running game """
        self.signalKeyEvent.emit(key_int)


    def get_game_options(self):
        """ retursn all relevant game options as a list"""
        game_options = [None,None,None,None]

        if self.game != None:
            game_options[0] = self.game.line_width
            game_options[1] = self.game.game_interval if self.game.is_host else None

        game_options[2] = self.name
        game_options[3] = self.host

        return game_options


    def set_line_width(self,line_width):
        if self.game != None:
            self.game.line_width = line_width

    def set_game_speed(self,speed):
        if self.game != None:
            self.game.game_interval = speed

    def set_player_name(self,name):
        self.name = name

    def set_server_ip(self,ip):
        self.host=ip