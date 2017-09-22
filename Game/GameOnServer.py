from PyQt5 import Qt,QtCore
import time

import Game
import GrafikObjects

class GameOnServer(Game.SnakeGame):
    """description of class"""

    @QtCore.pyqtSlot(list)
    def updateCommand(self, status):
        self._command_eval(status[0],status[1])

    def __init__(self,host,name):
        super().__init__(name)
        self.host = host
        self.is_game_going = False
        self.game_interval = 100
        self.client_pl_dict = {}
        self.grafik_item_list = []

        self.start_y = 10
        self.start_length = 3

    # ======================= parent methodes

    def stop_game(self):
        self.on_data_to_all_clients({"game":{"game_over":""}})
        return super().stop_game()

    
    # ======================= game loop

    def gameLoop(self):
        """ timer event, that is called at timer timeout """
        #f = open("C:/Users/Carsten/Desktop/test.txt","a")
        #f.write(str(QtCore.QThread.currentThreadId()) + " - game on server game loop \n")
        #f.close()
        self.calculate_scene()
        self.send_scene_informations()


    def _command_eval(self,client_source,tree_dict):
        #print("game on server- command eval : ",tree_dict)
        #print(QtCore.QThread.currentThreadId()," game on server command eval",tree_dict)
        #print(tree_dict)
        for command_key in tree_dict:
            if command_key == "set_field_size":
                self.set_field_size(tree_dict[command_key][0],tree_dict[command_key][1])
                self.set_player_start_position()
                self.on_data_to_all_clients({"game":{"set_field_size":[self.field_size.x(),self.field_size.y()]}})
            elif command_key == "direction":
                self.update_player_direction(tree_dict[command_key])
            elif command_key == "start_game_on_hold":
                self.timer.start(self.game_interval)
            elif command_key == "go":
                self.on_game_go()
            elif command_key == "reset":
                self.reset_game()
            elif command_key == "change_dir":
                if client_source in self.client_pl_dict:
                    self.client_pl_dict[client_source].direction = tree_dict[command_key]
            else:
                print("ERROR - Server - Command key not knwon '%s'"%command_key)

                
    def update_player_direction(self,direction):
        """ updating the direction information, revived from the client """
        pass


    # ======================= game preparation

    def join_game(self, player):
        print(" -> join game server "+self.name+" -> "+player.name)
        join_result = super().join_game(player)
        self.set_player_start_position()
        self.on_data_to_player(player,{"game":{"set_field_size":[self.field_size.x(),self.field_size.y()]}})
        return join_result


    def set_player_start_position(self):
        """ set the inital position of the player, if a player joins the game """
        if self.field_size.x() == 0: return
        
        parts = len(self.player_list)
        y_list = []
        for p in range(1,parts+1):
            y_list.append(self.field_size.y()*p/(parts+1))

        for i,p in enumerate(self.player_list):
            p1 = Qt.QPoint(self.start_y,y_list[i])
            p2 = Qt.QPoint(self.start_y+self.start_length,y_list[i])
            p.set_start_position([p1,p2])
            p.status_remove = False
            p.override_direction(0)
       

    def reset_game(self):
        self.is_game_going = False
        self.set_player_start_position()
        self.on_data_to_all_clients({"game":{"reset_ready":""}})
        

    def on_game_go(self):
        """ game status is changed from hold to go , on game start """
        print("============game go")
        # create dict with players - defines the players that are playing
        self.on_data_to_all_clients({"game":{"hide_all_dialogs":""}})

        for pl in self.player_list:
            if pl.client not in self.client_pl_dict :
                self.client_pl_dict[pl.client] = pl
            pl.override_direction(4)

        self.add_food_item()

        self.is_game_going = True
        #for pl in self.player_list:
        #    pl.direction = 4


    def calculate_scene(self):
        """ culculats all status changes in the game for one game loop """
        
        if self.is_game_going:
            for pl in self.player_list:
                pl.make_step()

            #obj_list = self.player_list + self.foot_list + self.border_list
            obj_list = self.player_list + self.grafik_item_list
            for pl in self.player_list:
                pl.check_for_intersection(obj_list)

            for pl in self.player_list:
                if pl.status_remove:
                    print("x killll xxx")
                    self.stop_game()

            # filter removed/killed objecets
            for item in self.grafik_item_list:
                if item.status_remove:
                    if item.type == "food":
                        item.set_random_position()

            # end game if a player is removed
                
    
    # ======================= preparing data for send

    def send_scene_informations(self):
        """ sending all relevant scene information to all clients, for status update """
        self.send_player_position()
        self.send_player_direction()
        self.send_grafik_objects()


    def send_player_position(self):
        """ send positions of all player to all clients """
        pl_coor_dict = {}
        for pl in self.player_list:
            #coor_list = [[p.x(),p.y()] for p in pl._line_list]
            pl_coor_dict[pl.id] = pl.get_line_list_float()
        self.on_data_to_all_clients({"game":{"player_coor":pl_coor_dict}})


    def send_player_direction(self):
        """ send direction of all player to the server """
        pl_dir_dict = {}
        for pl in self.player_list:
            pl_dir_dict[pl.id] = pl.direction
        self.on_data_to_all_clients({"game":{"player_dir":pl_dir_dict}})


    def send_grafik_objects(self):
        grafik_item_list = []
        for item in self.grafik_item_list:
            grafik_item_list.append( {"name":item.name,"type":item.type,"points":item.get_point_list_float(),"lines":item.get_line_list()})

        self.on_data_to_all_clients({"game":{"grafik_objects":grafik_item_list}})


    # ======================= sending data

    def on_data_to_all_clients(self,data_dict):
        data_dict["time"] = time.time()
        for pl in self.player_list:
            pl.client.send_msg(data_dict)


    def on_data_to_player(self,pl,data_dict):
        pl.client.send_msg(data_dict)

    # ===================== add object

    def add_food_item(self):
        food = GrafikObjects.SnakeFood(self.field_size)
        food.set_random_position()
        food.name = "first_food"

        self.grafik_item_list.append(food)