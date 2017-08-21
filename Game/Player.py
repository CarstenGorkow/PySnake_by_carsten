from PyQt5 import QtGui ,QtWidgets, QtCore,Qt

class Player(object):
    """description of class"""

    def __init__(self,client=None,name="Player"):        
        self.name = name
        self._direction = 0
        self._direction_old = 0
        self._last_direction = 0
        self._growth = 0
        self.color = QtGui.QPen(QtGui.QColor(0,0,0))
        self.pos_point_list = []
        self.client = client
        self.pen = QtGui.QPen(QtGui.QColor(100,100,100))
        self.pen.setWidth(1)
        self.item_group = None


    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self,dir):
        self._direction = dir


    def set_start_position(self,point_list):
        """ setting the initial positon of a player -> on server """
        self.pos_point_list.clear()
        for p in point_list:
            self.pos_point_list.append(p)


    def update_position(self,coor_list):
        self.pos_point_list.clear()
        for coor in coor_list:
            self.pos_point_list.append(Qt.QPoint(coor[0],coor[1]))


    def draw_object(self):
        """ create grafiks group item with all grafik pyqt elements of the player """
        self.item_group = QtWidgets.QGraphicsItemGroup()

        for i in range(1,len(self.pos_point_list)):
            # -> mulitplay pos with line with -> move to upper field corner
            p1 = self.pos_point_list[i-1]
            p2 = self.pos_point_list[i]
            
            l = QtWidgets.QGraphicsLineItem()
            l.setLine(p1.x(),p2.y(),p2.x(),p2.y())
            l.setPen(self.pen)
            self.item_group.addToGroup(l)

        return self.item_group


    #def calculate_position(self):
    #    pass

    def make_step(self):
        """ making a step with the snake """
        # if no direction
        if self._direction == 0: return
        
        # if direction chaned
        if self._direction_old != self._direction:
            last_end = self.pos_point_list[-1]
            new_end_1 = Qt.QPoint(last_end.x(),last_end.y())
            #new_end_2 = Qt.QPoint(last_end.x(),last_end.y())
            self.pos_point_list.append(new_end_1)
            self._direction_old = self._direction

        # move haead
        print(self.pos_point_list)
        cur_end_point = self.pos_point_list[-1]
        
        if self._direction == 1:                        # w
            cur_end_point.setY(cur_end_point.y()+1)
        elif self._direction == 2:                      # a
            cur_end_point.setX(cur_end_point.x()-1)
        elif self._direction == 3:                      # s 
            cur_end_point.setY(cur_end_point.y()-1)
        elif self._direction == 4:                      # d
            cur_end_point.setX(cur_end_point.x()+1)

        # move tail
        if self._growth == 0 :
            remaining_length = self._shrink(self.pos_point_list[0])
            if remaining_length == 0: self.pos_point_list.pop(0)
            pass
        else:
            self._growth = self._growth -1


    def _shrink(self,point_pair):
        """ calculates the direction and length of the tail
        -> shrinks the tail by one
        returns the length of the remaining last part """

        # 1. calculate tail length 
        first_point = self.pos_point_list[0]
        sec_point = self.pos_point_list[1]
        # 2. calculate direction
        delta_x = sec_point.x() - first_point.x() 
        delta_y = sec_point.y() - first_point.y()
        length = delta_x + delta_y

        print(delta_x,delta_y)
        # 3. shink tail by one
        if delta_x > 0.5 :
            first_point.setX(first_point.x()+1)
        elif delta_x < -0.5:
            first_point.setX(first_point.x()-1)
        elif delta_y > 0.5:
            first_point.setY(first_point.x()+1)
        elif delta_y < -0.5:
            first_point.setY(first_point.x()-1)
        else:
            print("error - tail has no direction -> no shrink possible")

        return length