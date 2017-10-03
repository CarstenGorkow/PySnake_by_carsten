from PyQt5 import Qt,QtCore

import Network
import Game
import GrafikObjects


class GameThread(QtCore.QThread):

    signalCommand = QtCore.pyqtSignal(list)
    signal_game_closed = QtCore.pyqtSignal(Game.Game)

    def __init__(self,game):
        QtCore.QThread.__init__(self)
        self.game = game
        self.game.set_thread(self)

    def __del__(self):
        self.wait()

    def run(self):
        print(QtCore.QThread.currentThreadId(),"game thread")

        # http://blog.debao.me/2013/08/how-to-use-qthread-in-the-right-way-part-1/
        self.timer = QtCore.QTimer()
        self.timer.moveToThread(self)
        self.timer.timeout.connect(self.game.gameLoop)
        self.game.timer = self.timer
        self.exec()
        print("game thread finished")


class GameServer(Network.Server):
    """description of class"""


    def __init__(self):
        Network.Server.__init__(self)

        self.client_player_dict = {}

        self.open_game_list = []
        self.client_game_dict = {}
        self.game_name_dict = {}
        self.player_max_id = 0
       

    def command_eval(self,client,data_element_tree):
        tree_dict = {}
        #tree_dict = data_element_tree.tree_dict
        tree_dict = data_element_tree

        for command_key in tree_dict:
            if command_key == "client_data":
                self.set_player_data(client,tree_dict[command_key])
            elif command_key == "open_game":
                game_name = tree_dict[command_key]
                self.open_game(client,game_name) 
                self.send_all_open_games()
            elif command_key == "join_game":
                self.join_game(self.client_player_dict[client],tree_dict[command_key])
                self.send_all_open_games()
            elif command_key == "get_open_games":
                self.send_all_open_games()
            elif command_key == "game":
                #self.client_game_dict[client].command_eval(tree_dict[command_key])
                # must be a dict -> otherwise empty
                self.game_thread.signalCommand.emit([client,tree_dict[command_key]])
            else:
                print("ERROR - Server - Command key not knwon '%s'"%key)


    def _attach_client(self, c, addr):
        """ overwriten methode from server
        creats a list for networkclient to player"""
        client = super()._attach_client(c, addr)

        self.client_player_dict[client] = GrafikObjects.Player(client,{"id":"p%i"%self.player_max_id})
        self.player_max_id = self.player_max_id +1 

        return client


    def set_player_data(self,client,data_dict):
        """ evaluating the client information and writing to the player object """
        if client in self.client_player_dict:
            player = self.client_player_dict[client]
            for cl_key in data_dict:
                if cl_key == "name":
                    player.name = data_dict[cl_key]
                elif cl_key == "color":
                    player.color = data_dict[cl_key]
        # distribute the player information to clients
        self.send_all_open_games()


    def open_game(self,game_host,game_name):
        """ opens a game, adds the host to the user list and send the open game list to the clients"""
        game = Game.GameOnServer(game_host,game_name)

        ##print(QtCore.QThread.currentThreadId(),"server thread")
        self.game_thread = GameThread(game)
        game.moveToThread(self.game_thread)
        self.game_thread.signalCommand.connect(game.updateCommand)
        #self.game_thread.signal_game_closed.connect(self.on_game_closed)
        #self.game_thread.finished.connect(self.on_game_closed)
        self.game_thread.start()



        ## ============
        #self.game_thread2 = QtCore.QThread()

        #self.timer = QtCore.QTimer()
        #self.timer.moveToThread(self.game_thread2)
        #self.timer.timeout.connect(game.gameLoop)
        #game.timer = self.timer
        ##self.exec()
        #self.game_thread2.finished.connect(self.on_game_closed)
        #self.game_thread2.start()
        ## ==========

        self.open_game_list.append(game)
        self.client_game_dict[game_host] = game
        self.game_name_dict[game_name] = game
        
        self.send_client(game_host,{"game_was_opened":game_name})
        

    def join_game(self,player,game_name):
        if game_name in self.game_name_dict:
            self.game_name_dict[game_name].join_game(player)
            return True
        return False


    def send_all_open_games(self):
        """ sending the open games to all hosts """
        open_games_dict = {}
        finished_games = []
        for g in self.open_game_list:
            if g.parent_thread.isFinished():
                finished_games.append(g)
                continue
            open_games_dict[g.name] = [p.get_data_dict() for p in g.player_list]
        self.send_clients({"open_games":open_games_dict})
        self.remove_finished_games(finished_games)


    def remove_finished_games(self,finished_games):
        for g in finished_games:
            if g in self.open_game_list:
                self.open_game_list.remove(g)


    def on_game_closed(self,game):
        """ removing game refenreces from game list """
        print("on_game_closed")
        if game in self.open_game_list:
            self.open_game_list.remove(game)
    

