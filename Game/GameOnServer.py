from PyQt5 import Qt,QtCore

import Game

class GameOnServer(Game.SnakeGame):
    """description of class"""

    
    @QtCore.pyqtSlot(dict)
    def updateCommand(self, status):
        #print(QtCore.QThread.currentThreadId(),"signal thread ")
        #print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",status)
        self.command_eval(status)

    def gameLoop(self):
        #print(QtCore.QThread.currentThreadId(),"game loop ")
        self.calculate_scene()
        self.send_scene_informations()

    def __init__(self,host,name):
        super().__init__(name)
        self.host = host


    def command_eval(self,tree_dict):
        print("game on server- command eval : ",tree_dict)

        for command_key in tree_dict:
            if command_key == "set_field_size":
                self.set_field_size(tree_dict[command_key][0],tree_dict[command_key][1])
                self.set_player_start_position()
                self.on_data_to_all_clients({"game":{"set_field_size":[self.field_size.x(),self.field_size.y()]}})
            elif command_key == "direction":
                self.update_player_direction(tree_dict[command_key])
            elif command_key == "start_game_on_hold":
                print("start threat",QtCore.QThread.currentThreadId())
                self.timer.start(500)
            elif command_key == "go":
                self.on_game_go()
            else:
                print("ERROR - Server - Command key not knwon '%s'"%key)

                
    def update_player_direction(self,direction):
        """ updating the direction information, revived from the client """
        pass

    # ======================= game preparation

    def join_game(self, player):
        join_result = super().join_game(player)
        self.set_player_start_position()
        return join_result


    def set_player_start_position(self):
        """ set the inital position of the player, if a player joins the game """
        if self.field_size.x() == 0: return
        
        parts = len(self.player_list)
        x = 10
        y_list = []
        for p in range(1,parts+1):
            y_list.append(self.field_size.y()*p/(parts+1))
        for i,p in enumerate(self.player_list):
            p1 = Qt.QPoint(x,y_list[i])
            p2 = Qt.QPoint(x+3,y_list[i])
            p.set_start_position([p1,p2])
        #self.send_player_position()
        

    def on_game_go(self):
        """ game status is changed from hold to go , on game start """
        for pl in self.player_list:
            pl.direction = 4
        #self.send_player_direction()

    # ======================= game loop

    #def timerEvent(self, e):
    #    """ methode colled by the qtimer, for game loop """
    #    print("hallo welt")
    #    self.calculate_scene()
    #    self.send_scene_informations(self)


    def calculate_scene(self):
        """ culculats all status changes in the game for one game loop """
        for pl in self.player_list:
            pl.make_step()
    
    # ======================= preparing data for send

    def send_scene_informations(self):
        """ sending all relevant scene information to all clients, for status update """
        self.send_player_position()
        self.send_player_direction()


    def send_player_position(self):
        """ send positions of all player to all clients """
        pl_coor_dict = {}
        for pl in self.player_list:
            name = pl.name
            coor_list = [[p.x(),p.y()] for p in pl.pos_point_list]
            pl_coor_dict[name] = coor_list
        self.on_data_to_all_clients({"game":{"player_coor":pl_coor_dict}})


    def send_player_direction(self):
        """ send direction of all player to the server """
        pl_dir_dict = {}
        for pl in self.player_list:
            name = pl.name
            pl_dir_dict[name] = pl.direction
        self.on_data_to_all_clients({"game":{"player_dir":pl_dir_dict}})

    # ======================= sending data

    def on_data_to_all_clients(self,data_dict):
        for pl in self.player_list:
            pl.client.send_msg(data_dict)


    def on_data_to_player(self,pl,data_dict):
        pl.client.send_msg(data_dict)