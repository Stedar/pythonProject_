#класс, который хранит всю инфу по доске  и графику
import numpy as np

class Board():
    def __init__(self, rows,columns, inarow) :
        self.grid = np.zeros((columns,rows),dtype=int) #создаем 2d массив
        self.columns = columns
        self.rows = rows
        self.inarow = inarow
        #12


