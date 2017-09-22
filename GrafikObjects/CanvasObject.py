
from PyQt5 import Qt,QtWidgets,QtGui


class CanvasObject(object):
    """base class for an object for the QGraphicsView"""

    def __init__(self):
        self.name = ""



        self._line_list = []
        self._point_list = []
        self.type = ""

        self.item_group = QtWidgets.QGraphicsItemGroup()
        self.raster_size = 1
        self.magnification=10



        # -> muss über eine property gemacht werden

        self.pen = QtGui.QPen()
        self.pen.setWidth(self.magnification)
        self.color = '#000000'

        self.status_remove = False

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self,c):
        self._set_color(c)

    def _set_color(self,c):
        self._color = c
        self.qcolor = QtGui.QColor(self._color)
        self.pen.setColor(self.qcolor)

    # ===================== excess to grafik coordinates ===========================

    def get_line_list(self):
        return self._line_list
   

    def get_line_list_float(self):
        """ updates the point positions from fload lists with coor pairs"""
        return [[[l.p1.x(),l.p1.y()],[l.p2.x(),l.p2.y()]] for l in self._line_list]


    def add_line(self,line):
        """ adds a line object to the line list """
        self._line_list.append(line)
        
        
    def set_line_list_fload(self,line_list):
        """ updates the point positions from fload lists with coor pairs
        - only use when sending data via bit stream"""
        pass


    def get_point_list(self):
        return self._point_list
    
    
    def get_point_list_float(self):
        """ returns the QPoint objects as list [x,y] pairs
        - only use when sending data via bit stream"""
        return [[p.x(),p.y()] for p in self._point_list]


    def set_point_list_fload(self,point_list):
        """ updates the point positions from fload lists with coor pairs"""
        self._point_list.clear()
        for p in point_list:
             self._point_list.append(Qt.QPoint(p[0],p[1]))
    

    # ===================== plot grafik object ===========================
    def plot(self):
        """ create grafiks group item with all grafik pyqt elements of the player """
        self.item_group = QtWidgets.QGraphicsItemGroup()
        #for i in range(1,len(self._line_list)):
        #    # -> mulitplay pos with line with -> move to upper field corner
        #    p1 = self._line_list[i-1]
        #    p2 = self._line_list[i]
            
        #    l = QtWidgets.QGraphicsLineItem()
        #    l.setLine(p1.x()*self.magnification,p1.y()*self.magnification,p2.x()*self.magnification,p2.y()*self.magnification)
        #    l.setPen(self.pen)
        #    self.item_group.addToGroup(l)
        for l in self._line_list:
            ql = l.get_q_line_item()
            ql.setPen(self.pen)
            self.item_group.addToGroup(ql)

        for i in range(0,len(self._point_list)):
            # -> mulitplay pos with line with -> move to upper field corner
            p = self._point_list[i]
            
            l = QtWidgets.QGraphicsEllipseItem()
            l.setRect((p.x()-0.5)*self.magnification,(p.y()-0.5)*self.magnification,self.magnification,self.magnification)
            #l.setLine(p1.x()*self.magnification,p1.y()*self.magnification,p2.x()*self.magnification,p2.y()*self.magnification)
            #l.setPen(self.pen)
            l.setBrush(QtGui.QColor(255,0,0))
            self.item_group.addToGroup(l)

        return self.item_group


