#технический класс для загрузки звуков и графики и их отрисовки

import os, sys
import pygame as pg
# from pygame.locals import *
# if not pg.font: print('Warning, fonts disabled')
# if not pg.mixer: print('Warning, sound disabled')


class MediaManager():

    def __init__(self,screen_size_w,screen_size_h, board,sector_size):
        pg.init()
        self.screen = pg.display.set_mode((screen_size_w, screen_size_h))
        self.sector_size = sector_size;
        self.board = board
        pg.display.set_caption("4 in a row")
        #pg.mouse.set_visible(False)

        # Create The Backgound
        self.background = pg.Surface(self.screen.get_size())
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))

        #data grapics
        self.sector_image = self.load_image("cell.png") #клетка поля
        self.dics1_image = self.load_image("disc1.png") #клетка 1 игрока
        self.dics2_image = self.load_image("disc2.png") #клетка 2 игрока

    def draw_board(self):
        #рисуем доску из фрагментов на данных массива карты. если нет
        for i in range(len(self.board.grid)):
            for j in range(len(self.board.grid[i])):
                self.draw_tile(j,i,self.board.grid[i][j])

    def draw_tile(self, x,y,value):
        image = None
        if value == 0: #пустое поле
            image = self.sector_image
        elif value == 1: #первый игрок
            image = self.dics1_image
        elif value == 2:  # первый игрок
            image = self.dics2_image

        rect = self.sector_image.get_rect()
        rect.topleft = (x * self.sector_size,y*self.sector_size)
        self.screen.blit(image,rect)




    def update_graphics(self): #выполняем апдейт всей графики
        # Draw Everything
        self.screen.blit(self.background, (0, 0))
        self.draw_board()
        pg.display.flip()


    # functions to create our resources
    def load_image(self,name):
        fullname = os.path.join('data', name)
        try:
            image = pg.image.load(fullname)
        except Exception as e:
            print("Cannot load  image",name,e)
            return None
        if image.get_alpha() is not None:
            image = image.convert_alpha()
        else:
            image = image.convert()
        return image