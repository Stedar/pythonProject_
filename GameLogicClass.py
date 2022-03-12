#класс игровой логики
from BoardClass import Board
from enum import Enum
import numpy as np
class PlayerType(Enum):
    HUMAN = 0
    RANDOM_AGENT = 1

class GameLogic():
    def __init__(self,board, player1_type,player2_type):
        self.board = board
        self.players = []
        self.players.append({"player":1,"type":player1_type})
        self.players.append({"player":2,"type":player1_type})
        #если требуется создать ботов, то создам их

        self.current_player = 1  #- 1 первый,2 - второй
    #ход.
    def turn(self, column, side):
        result =  self.get_unoccupied_sector(column)
        if result!=-1:
            self.board.grid[result][column] = side
            return True
        else:
            return False
    #тут проверка на победу

    def get_unoccupied_sector(self,column):
        #мы должны вычислить куда поставить диск в колонке
        result = np.where(self.board.grid[:,column]==0)
        if len(result[0]):
            last_index = len(result[0])-1
            return last_index
        else:
            return -1

    def MakeTurn(self,column):
        #если это игрок человек - просто кидаем диск в колонку
        #если это бот, то делаем вычисления
        if  self.players[self.current_player-1]["type"] == PlayerType.HUMAN:
            result = self.turn(column,self.current_player)
            if result: #меняем
                self.current_player = self.current_player%2+1


