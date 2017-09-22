import GrafikObjects
from PyQt5 import QtGui ,QtWidgets, QtCore,Qt

class Player(GrafikObjects.CanvasObject):
    """description of class"""

    def __init__(self,client=None,pl_data = {}):
        super().__init__()

        self.client = client
        self._eval_pl_data(pl_data)

        #self.color = QtGui.QPen(QtGui.QColor(0,0,0))

        self._direction = 4
        self._direction_old = 4
        #self._last_direction = 0
        
        self._growth = 0
        self.raster_size = 1


    def _eval_pl_data(self,data_dict):
        if 'name' in data_dict:
            self.name = data_dict['name']
        else:
            self.name = 'player'

        if 'id' in data_dict:
            self.id = data_dict['id']
        else:
            self.id = ""

        if 'color' in data_dict:
            print(" ==> ",data_dict['color'])
            self.color = data_dict['color']
        else:
            self.color = None


    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self,dir):
        self._set_direction(dir)


    def _set_direction(self,new_dir):
        dir_change = abs(self._direction_old - new_dir)%2
        if dir_change == 1:
            self._direction = new_dir


    def override_direction(self,new_dir):
        self._direction = new_dir


    def set_start_position(self,point_list):
        """ setting the initial positon of a player -> on server """
        self._line_list.clear()
        for i in range(1,len(point_list)):
            self.add_line(GrafikObjects.Line(point_list[i-1],point_list[i],self.magnification))


    def update_position(self,coor_list):
        self._line_list.clear()
        for l in coor_list: 
            p1 = Qt.QPoint(l[0][0],l[0][1])
            p2 = Qt.QPoint(l[1][0],l[1][1])
            self.add_line(GrafikObjects.Line(p1,p2,self.magnification))


    def make_step(self):
        """ making a step with the snake """
        # if no direction
        dir = self._direction
        if dir== 0: return
        if len(self._line_list) == 0: return
        
        # if direction chaned
        if self._direction_old != dir:
            last_end = self._line_list[-1].p2
            new_end_1 = Qt.QPoint(last_end.x(),last_end.y())
            new_end_2 = Qt.QPoint(last_end.x(),last_end.y())
            new_end_line = GrafikObjects.Line(new_end_1,new_end_2,self.magnification)
            self._line_list.append(new_end_line)
            self._direction_old = dir
        # move haead
        cur_end_point = self._line_list[-1].p2
        
        if dir == 1:                        # w
            cur_end_point.setY(cur_end_point.y()-self.raster_size)
        elif dir == 2:                      # a
            cur_end_point.setX(cur_end_point.x()-self.raster_size)
        elif dir == 3:                      # s 
            cur_end_point.setY(cur_end_point.y()+self.raster_size)
        elif dir == 4:                      # d
            cur_end_point.setX(cur_end_point.x()+self.raster_size)

        # move tail
        if self._growth == 0 :
            remaining_length = self._shrink(self._line_list[0])
            if abs(remaining_length) < 0.5 : 
                self._line_list.pop(0)
                remaining_length = self._shrink(self._line_list[0])
            pass
        else:
            self._growth = self._growth -1


    def _shrink(self,line):
        """ calculates the direction and length of the tail
        -> shrinks the tail by one
        returns the length of the remaining last part """

        # 1. calculate tail length 
        first_point = line.p1
        sec_point = line.p2
        # 2. calculate direction
        length = line.get_length()
        delta_x = line.get_length_x()
        delta_y = line.get_length_y()

        # 3. shink tail by one
        if delta_x > 0.5 :
            first_point.setX(first_point.x()+self.raster_size)
        elif delta_x < -0.5:
            first_point.setX(first_point.x()-self.raster_size)
        elif delta_y > 0.5:
            first_point.setY(first_point.y()+self.raster_size)
        elif delta_y < -0.5:
            first_point.setY(first_point.y()-self.raster_size)
        else:
            pass

        return length


    def check_for_intersection(self,canvas_object_list):
        """ checks for intersection with the objects in the list 
        - only the head of the player is checked for intersection
        - if intersection happen
            -> game finish?
            -> player gets attributes from the object
        """
        
        if len(self._line_list) == 0: return

        player_head = self._line_list[-1].p2

        for canvas_object in canvas_object_list:
            # get grafik objects
            line_list = canvas_object.get_line_list()
            point_list = canvas_object.get_point_list()
            #self.get_line_list()
            #self.get_point_list()

            for l in line_list:
                p_on_line = l.is_point_on_line(player_head)
                if p_on_line:
                    self.status_remove = True
                    print("removev set")

            for p in point_list:
                if player_head.x() == p.x():
                    if player_head.y() == p.y():
                        print(canvas_object.type)
                        if canvas_object.type == "food":
                            self._growth = canvas_object.value
                            canvas_object.status_remove = True
            

    def get_data_dict(self):
        data_dict = {}
        data_dict['name'] = self.name
        data_dict['id'] = self.id
        data_dict['color'] = self.color
        
        return data_dict