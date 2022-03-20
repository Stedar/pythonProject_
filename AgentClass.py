#абсртактный класс для общих методов
from BoardClass import Board

class Agent():
    def __init__(self,board):
        self.board = board

    def make_turn(self,side):
        pass
