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
        self.players.append({"player":2,"type":player2_type})
        #если требуется создать ботов, то создам их
        self.current_player = 1  #- 1 первый,2 - второй
        self.player_wins = 0
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
            return len(result[0])-1
        else:
            return -1

    def MakeTurn(self,column):
        #если это игрок человек - просто кидаем диск в колонку
        #если это бот, то делаем вычисления
        if  self.players[self.current_player-1]["type"] == PlayerType.HUMAN:
            result = self.turn(column,self.current_player)
            if self.check_winning_move(self.current_player):
                self.player_wins = self.current_player
            else: #меняем
                self.current_player = self.current_player%2+1



    #функция, которая проверяет наличие нужного количества "в ряд" по условиям
    def check_winning_move(self, side):
        #horizontal----
        for row in range(self.board.rows):
            for col in range(self.board.columns - (self.board.inarow - 1)):
                window = list(self.board.grid[row, col:col + self.board.inarow])
                if window.count(side) == self.board.inarow:
                    return True
        #vertical----
        for row in range(self.board.rows - (self.board.inarow-1)):
            for col in range(self.board.columns):
                window = list(self.board.grid[row:row + self.board.inarow, col])
                if window.count(side) == self.board.inarow:
                    return True

        # positive diagonal
        for row in range(self.board.rows - (self.board.inarow-1)):
            for col in range(self.board.columns - (self.board.inarow - 1)):
                window = list(self.board.grid[range(row, row+self.board.inarow), range(col, col+self.board.inarow)])
                if window.count(side) == self.board.inarow:
                    return True
        # negative diagonal
        for row in range(self.board.inarow-1, self.board.rows):
            for col in range(self.board.columns - (self.board.inarow - 1)):
                window = list(self.board.grid[range(row, row - self.board.inarow,-1), range(col, col + self.board.inarow)])
                if window.count(side) == self.board.inarow:
                    return True

