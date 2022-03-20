# агент который делает случайные ходы

import random
import numpy as np
from BoardClass import Board
from AgentClass import Agent


class RandomAgentAdvanced(Agent):
    def __init__(self, board):
        Agent.__init__(self, board)

    def make_turn(self, side):
        return self.best_random_move(side)

    def best_random_move(self,side):
        # выбираем все колонки, где можно сделать ход
        valid_moves = []
        for col in range(self.board.columns):
            window = list(self.board.grid[:, col])
            if window.count(0) > 0:
                valid_moves.append(col)

        #проверяем каждый вариант на победу
        for i in valid_moves:
            temp_grid = np.copy(self.board.grid)
            if self.check_turn(temp_grid,i,side):
                if self.check_winning_move(temp_grid,side):
                    return True,i
        #проверяем каждый вариант на победу соперника, чтобы помешать ему
        for i in valid_moves:
            temp_grid = np.copy(self.board.grid)
            if self.check_turn(temp_grid,i,side% 2 + 1):
                if self.check_winning_move(temp_grid,side% 2 + 1):
                    return True,i

        #в противном случае возвращаем случайно
        if len(valid_moves)>0:
            return True,random.choice(valid_moves)
        else:
            return False, None


    #ход.
    def check_turn(self, grid, column, side):
        result =  self.get_unoccupied_sector(grid,column)
        if result!=-1:
            grid[result][column] = side
            return True
        else:
            return False

    def get_unoccupied_sector(self,grid,column):
        #мы должны вычислить куда поставить диск в колонке
        result = np.where(grid[:,column]==0)
        if len(result[0]):
            return len(result[0])-1
        else:
            return -1

    #функция, которая проверяет наличие нужного количества "в ряд" по условиям
    def check_winning_move(self, grid, side):

        #horizontal----
        for row in range(self.board.rows):
            for col in range(self.board.columns - (self.board.inarow - 1)):
                window = list(grid[row, col:col + self.board.inarow])
                if window.count(side) == self.board.inarow:
                    return True
        #vertical----
        for row in range(self.board.rows - (self.board.inarow-1)):
            for col in range(self.board.columns):
                window = list(grid[row:row + self.board.inarow, col])
                if window.count(side) == self.board.inarow:
                    return True

        # positive diagonal
        for row in range(self.board.rows - (self.board.inarow-1)):
            for col in range(self.board.columns - (self.board.inarow - 1)):
                window = list(grid[range(row, row+self.board.inarow), range(col, col+self.board.inarow)])
                if window.count(side) == self.board.inarow:
                    return True
        # negative diagonal
        for row in range(self.board.inarow-1, self.board.rows):
            for col in range(self.board.columns - (self.board.inarow - 1)):
                window = list(grid[range(row, row - self.board.inarow,-1), range(col, col + self.board.inarow)])
                if window.count(side) == self.board.inarow:
                    return True

