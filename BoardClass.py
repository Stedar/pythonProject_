#класс, который хранит всю инфу по доске  и графику
import numpy as np

class Board():
    def __init__(self, columns,rows, inarow) :
        self.grid = np.zeros((rows,columns),dtype=int) #создаем 2d массив
        self.columns = columns
        self.rows = rows
        self.inarow = inarow
        #12


