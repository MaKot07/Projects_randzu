#import sys
import pygame
from Const import *
import copy
import numpy as np
#from numba import jit

black = 0
white = 1
cell_qty = 14
cell_size = 40
cell_size_ramka = 42
colors = (234, 237, 204)
board_shift = 30
WHITE = (255, 255, 255)
RED = (225, 0, 50)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)
BLACK = (10, 10, 10)
GRAY = (92, 87, 87)

class Game_Graphics:

    __cell_qty = 14
    __cell_size = 40
    __cell_size_ramka = 42
    __colors = (234, 237, 204)
    __board_shift = 30


    def __init__(self, number_of_movies):
        self.__now_coord_all_move_and_color = np.empty(0, dtype=np.int8)
        self.__number_of_movies = number_of_movies

    def set_number_move(self):
        self.__number_of_movies += 1

    def give_number_move(self):
        return self.__number_of_movies


    def draw_all_game(self, win_color):
        self.draw_screen()
        self.draw_main_board()
        if self.__now_coord_all_move_and_color.size > 0:
            self.draw_all_shashky()
        self.text_output_number_of_movies()
        if win_color != None:
            self.text_win(win_color)
        self.draw_button_newgame()

        pygame.display.update()
        # pygame.time.delay(120)

    #@staticmethod
    def draw_main_board(self):
        board_words = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

        for x in range(Game_Graphics.__cell_qty + 1):
            text1 = f1.render(f'{board_words[x]}', 1, BLACK)
            screen.blit(text1, (x * Game_Graphics.__cell_size_ramka + 23, 0))

        for y in range(Game_Graphics.__cell_qty):
            for x in range(Game_Graphics.__cell_qty):
                pygame.draw.rect(screen, colors, (x * (Game_Graphics.__cell_size + 2) + Game_Graphics.__board_shift, y * (Game_Graphics.__cell_size + 2) + Game_Graphics.__board_shift, Game_Graphics.__cell_size, Game_Graphics.__cell_size))
                pygame.draw.rect(screen, BLACK, (x * Game_Graphics.__cell_size_ramka + Game_Graphics.__board_shift, y * Game_Graphics.__cell_size_ramka + Game_Graphics.__board_shift, Game_Graphics.__cell_size_ramka, Game_Graphics.__cell_size_ramka),2)

                text1 = f1.render(f'{15 - y}', 1, BLACK)
            if 15 - y < 10:
                screen.blit(text1, (5, y * Game_Graphics.__cell_size_ramka + 20))
            else:

                screen.blit(text1, (0, y * Game_Graphics.__cell_size_ramka + 20))
            if y == Game_Graphics.__cell_qty - 1:
                text2 = f1.render('1', 1, BLACK)
                screen.blit(text2, (5, (y + 1) * Game_Graphics.__cell_size_ramka + 20))

    def draw_all_shashky(self):
        for index_x_rect, index_y_rect, color_player in self.__now_coord_all_move_and_color:
            if color_player == black:
                pygame.draw.circle(screen, BLACK, (index_x_rect * cell_size_ramka + board_shift, index_y_rect * cell_size_ramka + board_shift), 10)
            else:
                pygame.draw.circle(screen, WHITE, (index_x_rect * cell_size_ramka + board_shift, index_y_rect * cell_size_ramka + board_shift), 10)

    #@staticmethod
    def draw_screen(self):
        screen.fill((155, 155, 155))

    #@staticmethod
    def text_output_number_of_movies(self):
        text = f1.render(f'Количество ходов: {self.__number_of_movies}', 1, BLACK)
        screen.blit(text, (100, 700))

        # text_move = f1.render(f'Ходы: {coord_all_move_and_color}', 1, BLACK)
        # screen.blit(text_move, (100, 750))

    #@staticmethod
    def draw_button_newgame(self):
        pygame.draw.rect(screen, (40, 224, 132), (700, 180, 140, 70))
        text = f1.render(f'NEW GAME', 1, BLACK)
        screen.blit(text, (700, 200))

    def text_win(self, color):
        if color == black:
            text = f1.render(f'Игра закончилась. Победили черные!!', 1, BLACK)
            screen.blit(text, (100, 850))
        else:
            text = f1.render(f'Игра закончилась. Победили белые!!', 1, BLACK)
            screen.blit(text, (100, 850))

    def change_color_player(self, color_player):
        if color_player == black:
            color_player = white
        else:
            color_player = black

        return color_player

    def set_coord(self, x, y, color):
        if self.__now_coord_all_move_and_color.size == 0:
            self.__now_coord_all_move_and_color = np.array([[x,y,color]])
        else:
            self.__now_coord_all_move_and_color = np.vstack((self.__now_coord_all_move_and_color, np.array([[x, y, color]])))



def give_coord(events):
    x, y = events.pos
    x, y = x - board_shift, y - board_shift
    return x,y

def give_coord_rect(events):
    x,y = give_coord(events)

    index_x_rect = round(x / cell_size_ramka)
    index_y_rect = round(y / cell_size_ramka)

    return index_x_rect,index_y_rect

def check_in_2D_array(check_array, check_in_array):
    for i, sub in enumerate(check_in_array):
        if np.array_equal(sub, check_array):
            return True
    return False






pygame.init()
screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption("MY game")
#icon = pygame.image.load("images/icon.png")
#pygame.display.set_icon(icon)


f1 = pygame.font.Font(None, 36)
screen.fill((255, 255, 255))









