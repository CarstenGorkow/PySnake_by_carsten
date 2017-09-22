import random
from PyQt5 import Qt

import GrafikObjects

class SnakeFood(GrafikObjects.CanvasObject):
    """description of class"""

    def __init__(self,pos_range):
        super().__init__()
        self.pos_range = pos_range
        self.type = "food"
        self.value = 10

    def set_random_position(self):
        pos_x = random.randint(0,self.pos_range.x())
        pos_y = random.randint(0,self.pos_range.y())
        
        self._point_list.clear()
        self._point_list.append(Qt.QPoint(pos_x,pos_y))
        self.status_remove = False

    def set_position(self):
        pass

