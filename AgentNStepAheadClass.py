import numpy as np
import random
from BoardClass import Board
from AgentClass import Agent

NUM_FOUR_POINT_SCORE  = 10000
NUM_THREES_POINT_SСORE = 10
NUM_THEЕRS_OPPONENT_POINT_SCORE = -100
NUM_FOUR_OPPONENT_POINT_SCORE = -1000
N_STEPS = 3

class AgentNStepAhead(Agent):
    def __init__(self,board):
        Agent.__init__(self,board)

    def make_turn(self, side):
        return self.get_n_step(side)


    # Helper function for minimax: checks if game has ended
    def is_terminal_node(self, grid):
        #horizontal----
        for row in range(self.board.rows):
            for col in range(self.board.columns - (self.board.inarow - 1)):
                window = list(grid[row, col:col + self.board.inarow])
                if window.count(1) == self.board.inarow or window.count(2) == self.board.inarow:
                    return True
        #vertical----
        for row in range(self.board.rows - (self.board.inarow-1)):
            for col in range(self.board.columns):
                window = list(grid[row:row + self.board.inarow, col])
                if window.count(1) == self.board.inarow or window.count(2) == self.board.inarow:
                    return True

        # positive diagonal
        for row in range(self.board.rows - (self.board.inarow-1)):
            for col in range(self.board.columns - (self.board.inarow - 1)):
                window = list(grid[range(row, row+self.board.inarow), range(col, col+self.board.inarow)])
                if window.count(1) == self.board.inarow or window.count(2) == self.board.inarow:
                    return True
        # negative diagonal
        for row in range(self.board.inarow-1, self.board.rows):
            for col in range(self.board.columns - (self.board.inarow - 1)):
                window = list(grid[range(row, row - self.board.inarow,-1), range(col, col + self.board.inarow)])
                if window.count(1) == self.board.inarow or window.count(2) == self.board.inarow:
                    return True

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

    # Helper function for minimax: calculates value of heuristic for grid
    def get_heuristic(self,grid, side):
        score = 0
        num_threes = self.count_windows(grid, side, 3)
        num_fours = self.count_windows(grid, side, 4)
        num_threes_opp = self.count_windows(grid, side % 2 + 1, 3)
        num_four_opp = self.count_windows(grid, side % 2 + 1, 4)
        score = (num_threes * NUM_THREES_POINT_SСORE)  + (NUM_FOUR_POINT_SCORE  * num_fours) + (NUM_THEЕRS_OPPONENT_POINT_SCORE * num_threes_opp) + (NUM_FOUR_OPPONENT_POINT_SCORE * num_four_opp)
        return score

    # Minimax implementation
    def minimax(self,node, depth, maximizingPlayer, side):
        is_terminal = self.is_terminal_node(node)
        valid_moves = [c for c in range(self.board.columns) if self.board.grid[0][c]== 0]
        if depth == 0 or is_terminal:
            return self.get_heuristic(node, side)
        if maximizingPlayer:
            value = -np.Inf
            for col in valid_moves:
                child = self.get_new_grid(node,col,side)
                value = max(value, self.minimax(child, depth - 1, False, side))
            return value
        else:
            value = np.Inf
            for col in valid_moves:
                child = self.get_new_grid(node, col, side % 2 + 1)
                value = min(value, self.minimax(child, depth - 1, True, side))
            return value

    def get_n_step(self,side):
        #получаем все колонки, куда можно бросить диск
        valid_moves = [c for c in range(self.board.columns) if self.board.grid[0][c]== 0]
        scores = {}
        #подсчитываем очки за каждый сделанный ход
        for col in valid_moves:
            temp_grid = np.copy(self.board.grid)
            score = self.score_move(temp_grid,col,side,N_STEPS)
            scores[col] = score
        #получаем список максимально больших значений
        max_cols = [key for key in scores.keys() if scores[key] == max(scores.values())]
        return True,random.choice(max_cols)

    def score_move(self, grid,col,side,n_steps):
        next_grid = self.get_new_grid(grid, col, side)
        score = self.minimax(next_grid, n_steps - 1, False, side)
        return score

    def get_new_grid(self,grid,column,side):
        #мы должны вычислить куда поставить диск в колонке
        result = np.where(grid[:,column]==0)
        #возвращаем новую карту с поставленным диском
        new_grid = np.copy(grid)
        new_grid[len(result[0])-1][column] = side
        return new_grid
