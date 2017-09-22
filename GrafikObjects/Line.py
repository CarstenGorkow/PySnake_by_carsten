from PyQt5 import QtGui ,QtWidgets, QtCore,Qt

import PyQt_Gui

class Line(QtWidgets.QGraphicsLineItem):
    """description of class"""
    def __init__(self,p1,p2,magnification):
        super().__init__()
        self.p1 = p1
        self.p2 = p2
        self.magnification = magnification


    def get_q_line_item(self):
        l = QtWidgets.QGraphicsLineItem()
        l.setLine(self.p1.x()*self.magnification,self.p1.y()*self.magnification,self.p2.x()*self.magnification,self.p2.y()*self.magnification)
        #l.setPen(self.pen)
        #self.item_group.addToGroup(l)
        return l


    def get_length(self):
        delta_x = self.p2.x() - self.p1.x() 
        delta_y = self.p2.y() - self.p1.y()
        length = abs(delta_x) + abs(delta_y)
        return length 


    def get_length_x(self):
        delta_x = self.p2.x() - self.p1.x() 
        return delta_x 


    def get_length_y(self):
        delta_y = self.p2.y() - self.p1.y()
        return delta_y 


    def is_point_on_line(self,point):
        """ claculates the relative position and normal distance of a pyqt5.Qpoint object to the line"""
        
        x = point.x()
        y = point.y()
        dx = self.p2.x() - self.p1.x()
        dy = self.p2.y() - self.p1.y()

        p_on_line =  False
        if dx == 0 and dy == 0:
            if x == self.p1.x() and y == self.p1.y(): p_on_line = True
        elif dx == 0:
            dxp = x-self.p1.x()           
            y_pos = ( y-self.p1.y() ) / dy 
            if dxp == 0 and y_pos >= 0 and y_pos < 1 : p_on_line = True
        elif dy == 0:
            x_pos = ( x-self.p1.x() ) / dx
            dyp = y-self.p1.y()
            if dyp == 0 and x_pos >= 0 and x_pos < 1 : p_on_line = True
        else:
            x_pos = ( x-self.p1.x() ) / dx
            y_pos = ( y-self.p1.y() ) / dy 
            if x_pos == y_pos and x_pos >= 0 and x_pos <= 1 : p_on_line = True

        #(x - x1) / (x2 - x1) = (y - y1) / (y2 - y1)
        return p_on_line
