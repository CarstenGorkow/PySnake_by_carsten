from PyQt5 import QtCore
import queue

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


    def remove_player_not_in_list(self,player_list):
        """ removes all player that are not in the list """
        remove_list = []
        for pl in self.player_list:
            if pl.name not in player_list:
                remove_list.append(pl)
        for pl in remove_list:
            self.player_list.remove(pl)


    def is_player_joined(self,player_name):
        """ checkes if a player with a specific name has joined the game """
        for pl in self.player_list:
            if pl.name == player_name: return True
        return False
    

    def start_game(self):
        pass


    def reset_game(self):
        pass


    def pause_game(self):
        pass


    def stop_game(self):
        pass