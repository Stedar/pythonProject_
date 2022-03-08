import pygame as pg
from BoardClass import Board
from MediaManagerClass import MediaManager

SECTOR_SIZE = 100

#управляющий класс

class GameManager():
    def __init__(self, columns, rows, inarow):
        self.board = Board(columns, rows, inarow)
        screen_size_w =  SECTOR_SIZE * columns
        screen_size_h =  SECTOR_SIZE * rows
        self.media_manager = MediaManager(screen_size_w,screen_size_h, self.board, SECTOR_SIZE)
        self.clock = pg.time.Clock()


    def run(self): #main loop
        going = True
        while going:
            self.clock.tick(60)
            # Handle Input Events

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    going = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    going = False

            self.media_manager.update_graphics()

game_manager_class = GameManager(7,6,4)
game_manager_class.run()