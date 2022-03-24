import numpy as np
import random
from BoardClass import Board
from AgentClass import Agent

NUM_FOR_POINT_SCORE  = 1000
NUM_THREES_POINT_CSORE = 10
NUM_FOR_OPPONENT_POINT_SCORE = -100



class AgentOneStepAhead(Agent):
    def __init__(self,board):
        Agent.__init__(self,board)


    def make_turn(self,side):
        return self.get_heuristic(side)

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
    def count_windows(self, grid, side,num_discs):
        num_windows = 0

        #horizontal----
        for row in range(self.board.rows):
            for col in range(self.board.columns - (self.board.inarow - 1)):
                window = list(grid[row, col:col + self.board.inarow])
                if window.count(side) == num_discs and window.count(0)==self.board.inarow -num_discs:
                    num_windows+=1
        #vertical----
        for row in range(self.board.rows - (self.board.inarow-1)):
            for col in range(self.board.columns):
                window = list(grid[row:row + self.board.inarow, col])
                if window.count(side) == num_discs and window.count(0)==self.board.inarow -num_discs:
                    num_windows+=1

        # positive diagonal
        for row in range(self.board.rows - (self.board.inarow-1)):
            for col in range(self.board.columns - (self.board.inarow - 1)):
                window = list(grid[range(row, row+self.board.inarow), range(col, col+self.board.inarow)])
                if window.count(side) == num_discs and window.count(0)==self.board.inarow -num_discs:
                    num_windows+=1
        # negative diagonal
        for row in range(self.board.inarow-1, self.board.rows):
            for col in range(self.board.columns - (self.board.inarow - 1)):
                window = list(grid[range(row, row - self.board.inarow,-1), range(col, col + self.board.inarow)])
                if window.count(side) == num_discs and window.count(0)==self.board.inarow -num_discs:
                    num_windows+=1


        return num_windows

    def get_heuristic(self, side):
        #выбираем все колонки, где можно сделать ход
        valid_moves = []
        scores = {}

        for col in range(self.board.columns):
            window = list(self.board.grid[:, col])
            if window.count(0) > 0:
                valid_moves.append(col)
        if len(valid_moves)==0:
            return False,None
        #подсчитываем очки за каждый сделанный ход
        for col in valid_moves:
            #копируем карту.
            temp_grid = np.copy(self.board.grid)
            #вносим изменение в скопированную карту
            if self.check_turn(temp_grid,col,side):
                score = self.get_scores(temp_grid,side)
                scores[col] = score

        #получаем список максимально больших значений
        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        return True,random.choice(max_cols)

    def get_scores(self,grid,side):
        score = 0
        num_threes = self.count_windows(grid, side, 3)
        num_fours = self.count_windows(grid, side, 4)
        num_threes_opp = self.count_windows(grid, side % 2 + 1, 3)
        score = (num_threes * NUM_THREES_POINT_CSORE)  + (NUM_FOR_POINT_SCORE  * num_fours) + (NUM_FOR_OPPONENT_POINT_SCORE * num_threes_opp)
        return score
