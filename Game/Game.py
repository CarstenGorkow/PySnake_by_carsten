from PyQt5 import QtCore
import queue

import GrafikObjects


class Game(QtCore.QObject):
    """description of class"""

    def __init__(self,name): 
        super().__init__()       
        self.name = name
        self.player_nr = 0
        self.player_list = []

        self.task_queue = queue.Queue()


    def join_game(self,player):
        if player not in self.player_list:
            self.player_list.append(player)
            self.player_nr = len(self.player_list)
            return True
        return False


    def consolidate_player(self,data_dict):
        """ consolidating the player data that cames from the server / removing player and adding new """
        self.remove_player_not_in_list( [p['id'] for p in data_dict])
        for pl_data in data_dict:
            pl_id = pl_data['id']
            if not self.is_player_joined(pl_id):
                self.join_game(GrafikObjects.Player(None,pl_data))
            else:
                self.get_player(pl_id).update_player_data(pl_data)


    def remove_player_not_in_list(self,player_list):
        """ removes all player that are not in the list """
        remove_list = []
        for pl in self.player_list:
            if pl.id not in player_list:
                remove_list.append(pl)
        for pl in remove_list:
            self.player_list.remove(pl)


    def is_player_joined(self,player_name):
        """ checkes if a player with a specific name has joined the game """
        for pl in self.player_list:
            if pl.id == player_name: return True
        return False
    

    def get_player(self,player_id):
        for pl in self.player_list:
            if pl.id == player_id: return pl
        return None


    def start_game(self):
        pass


    def reset_game(self):
        pass


    def pause_game(self):
        pass


    def stop_game(self):
        pass