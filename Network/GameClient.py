
from PyQt5 import QtCore


import Network
import Game

class GameClient(Network.Client):
    """description of class"""

    signalCommand = QtCore.pyqtSignal(list)

    def __init__(self):
        Network.Client.__init__(self)
        self.name = "player1"
        self.open_games = []
        self._open_game_owner  = False
        self.callback_on_game_start = None
        self.game = None


    @property
    def open_game_owner(self):
        return self._open_game_owner

    @open_game_owner.setter
    def open_game_owner(self,val):
        self._open_game_owner = val
        # should be empty -> not used in the current version
        if self.callback_on_game_start != None: self.callback_on_game_start()


    def send_player_data(self):
        """ sending client data to the server """
        self.client_wrap.send_msg({"client_data":{"name":self.name}})
    

    def connect_client(self):
        super().connect_client()
        self.send_player_data()


    def open_new_game(self,game_name):
        """ send an open new game command to the server """
        self.client_wrap.send_msg({"open_game":game_name})
        self.client_wrap.send_msg({"join_game":game_name})


    def on_send_game_data_to_server(self,msg_dict):
        self.client_wrap.send_msg(msg_dict)


    def put_task_to_queue(self, task):
        """ task redirecting of server data
        -> overwritten from parent class 
        -> running on background threat """
        tree_dict = task[1]
        if "game" in tree_dict.keys():
            #self.game.task_queue.put([task[0],tree_dict["game"]])
            self.signalCommand.emit([task[0],tree_dict["game"]])
            tree_dict.pop("game")
        if len(tree_dict) > 0 :
            super().put_task_to_queue(task)
    

    def start_game_grafik_interface(self,game_name,graphics_view):
        """ creats game object """
        self.game = Game.GameOnClient(game_name,graphics_view,self.open_game_owner,self.on_send_game_data_to_server)
        self.signalCommand.connect(self.game.updateCommand)

    def update_open_game_player_data(self,open_game_dict):
        """ if a game is open then, update the player information 
        - removes player that are not in the list from game
        - adds player that are in the list, but not in the game """
        if isinstance(self.game,Game.GameOnClient):
            print("update game data")
            for ga in open_game_dict:
                if ga == self.game.name:
                    self.game.remove_player_not_in_list( open_game_dict[ga][1])
                    for pl in open_game_dict[ga][1]:
                        if not self.game.is_player_joined(pl):
                            self.game.join_game(Game.Player(self.client_wrap,pl))




