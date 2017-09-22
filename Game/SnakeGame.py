from PyQt5 import Qt,QtCore

import Game



class SnakeGame(Game.Game):
    """description of class"""

    def __init__(self,name):
        super().__init__(name)

        self.field_size = Qt.QPoint(0,0)
        self.line_width = 10

        self.step = 0
        self.timer = QtCore.QTimer()

        self.food_list = []
        self.border_list = []


    def set_field_size(self,w,h):
        self.field_size.setX(w)
        self.field_size.setY(h)


    def stop_game(self):
        self.timer.stop()
        return super().stop_game()