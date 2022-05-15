#абсртактный класс для общих методов
from BoardClass import Board

class Agent():
    def __init__(self,board):
        self.board = board
        self.name = 'noname'

    def make_turn(self,side):
        pass

    def train(self,status,side):
        pass

