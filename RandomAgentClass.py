#агент который делает случайные ходы

import random
from BoardClass import Board
from AgentClass import Agent

class RandomAgent(Agent):
    def __init__(self,board):
        Agent.__init__(self,board)

    def make_turn(self,side):
        return self.random_move()

    def random_move(self):
        #выбираем все колонки, где можно сделать ход
        #берем случайную из них
        valid_moves = []
        for col in range(self.board.columns):
            window = list(self.board.grid[:, col])
            if window.count(0) > 0:
                valid_moves.append(col)

        if len(valid_moves)>0:
            return True,random.choice(valid_moves)
        else:
            return False, None

