#Q learning agent--------
import numpy as np
import random
from BoardClass import Board
from AgentClass import Agent
import sqlite3

WIN_REWARD = 200
LOSE_REWARD = -200
DRAW_REWARD = 50
DEFAULT_REWARD = -0.05


class QTable:
    def __init__(self, action_space):
        self.table = dict()
        self.action_space = action_space
        self.load_q_table()

    def load_q_table(self):
        self.table = {}
        try:

            con = sqlite3.connect('q_table.db')
            cursor = con.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS states
                           (col0 real,col1 real, col2 real,col3 real,col4 real, col5 real, col6 real, id text PRIMARY KEY)''')
            # Save (commit) the changes
            con.commit()
            # We can also close the connection if we are done with it.
            # Just be sure any changes have been committed or they will be lost.

            sqlite_select_query = "SELECT * from states"
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()

            for i in records:
                self.table[i[7]] = list(i[:7])
        except Exception as e:
            print("Error while loading data")
        finally:
            con.close()

    def get_state_key(self,board,side):
        board = board.copy().flatten() # Get a copy
        board = np.append(board,side)
        state_key = np.array(board).astype(str)
        state_key = hex(int(''.join(state_key), 3))[2:]
        return state_key

    def get_state(self,board,side):
        state_key = self.get_state_key(board,side)
        if state_key not in self.table.keys():
            q_list = list(np.zeros(self.action_space))
            self.table[state_key] = q_list
            # save_list = q_list.copy()
            # save_list.append(state_key)
            self.save_qtable_state(state_key)
        return self.table[state_key]

    def save_qtable_state(self, state_key):
        try:
            list_row = self.table[state_key]
            con = sqlite3.connect('q_table.db')
            cursor = con.cursor()
            values = str(list_row[0]) + "," + str(list_row[1]) + "," + str(list_row[2]) + "," + str(list_row[3]) + "," + str(list_row[4]) + "," + str(list_row[5]) + "," + str(list_row[6]) + ",'" + state_key + "'"
            query = "INSERT INTO states VALUES  (" + values + ") ON CONFLICT(id) DO UPDATE SET col0=excluded.col0,col1=excluded.col1,col2=excluded.col2,col3=excluded.col3,col4=excluded.col4,col5=excluded.col5,col6=excluded.col6; "
            cursor.execute(query)
            con.commit()
        except Exception as e:
            print("error while save data to sql")
        finally:
            con.close()



class AgentRLQ_learn(Agent):
    def __init__(self,board):
        Agent.__init__(self,board)
        self.prev_board = board.grid.copy()
        self.train_turn = 0
        self.Q_table = QTable(board.grid.shape[1])
        self.lr = 0.2
        self.decay_gamma = 0.9

    def train(self,status,side):
        self.update_Q_table(status,side)

    def update_Q_table(self,status, side):
     #получаем результат текущего тура. (оба игрока походили). определяем reward тура
     #  # status - 0 - game is running, draw = 1  lose= -1, win = 2
    #reward = current_q_value + self.lr * (self.decay_gamma * reward - current_q_value)
        if status == 0:
            reward = DEFAULT_REWARD
        elif status == 1:
            reward = WIN_REWARD
        else:
            reward = LOSE_REWARD

        #получаем предыущее значение reward на этот action
        old_value = self.Q_table.get_state(self.prev_board,side) [self.train_turn]
        #фиксирем ситуацию по текущему стейту и выбираем наиболее дорогое действие

        next_max = max(self.Q_table.get_state(self.board.grid,side))
        #делаем апдейт reward
        reward = old_value + self.lr * (self.decay_gamma * reward - next_max)
        self.Q_table.get_state(self.prev_board, side)[self.train_turn] = reward
        # записываем его в таблицу
        self.Q_table.save_qtable_state(self.Q_table.get_state_key(self.prev_board, side))



    def make_turn(self,side):
        #сохраняем карту и выбранный ход
        result = self.random_move()
        self.prev_board = self.board.grid.copy()
        self.train_turn = result[1]
        return result

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

