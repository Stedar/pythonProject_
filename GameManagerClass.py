import time

import pygame as pg
from BoardClass import Board
from MediaManagerClass import MediaManager
from GameLogicClass import GameLogic
from GameLogicClass import PlayerType

SECTOR_SIZE = 100

#управляющий класс

class GameManager():
    def __init__(self, columns, rows, inarow):
        self.board = Board(columns, rows, inarow)
        self.game_logic = GameLogic(self.board,PlayerType.AGENT_ONE_STEP_AHEAD,PlayerType.HUMAN)
        screen_size_w =  SECTOR_SIZE * columns
        screen_size_h =  SECTOR_SIZE * rows
        self.media_manager = MediaManager(screen_size_w,screen_size_h, self.board, SECTOR_SIZE)
        self.clock = pg.time.Clock()


    def run(self): #main loop
        going = True
        game_over = False

        while going:
            self.clock.tick(60)

            #если текущий игрок бот - делаем ход и немного отдыхаем)
            if not game_over and self.game_logic.if_current_player_is_bot():
                self.game_logic.MakeTurn()
                time.sleep(1)

            if self.game_logic.player_wins!=0:
                self.media_manager.set_winnner(self.game_logic.player_wins)
                game_over = True
            # Handle Input Events

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    going = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    going = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if not self.game_logic.if_current_player_is_bot() and not game_over:
                        pos = pg.mouse.get_pos()
                        self.game_logic.MakeTurn(int(pos[0]/SECTOR_SIZE))
                        #делаем ход

            self.media_manager.update_graphics()

game_manager_class = GameManager(7,6,4)
game_manager_class.run()