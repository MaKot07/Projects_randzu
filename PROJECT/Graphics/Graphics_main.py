import sys
import pygame
from Const import *



def draw_all_game(win_color,number_of_movies, coord_all_move_and_color):
    draw_screen()
    draw_main_board(cell_qty, cell_size, cell_size_ramka)
    draw_all_shashky(coord_all_move_and_color)
    text_output_number_of_movies(number_of_movies)
    if win_color != None:
        text_win(win_color)
    pygame.display.update()
    #pygame.time.delay(120)



def draw_main_board(cell_qty, cell_size, cell_size_ramka):
    global text1
    board_words = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']

    for x in range(cell_qty + 1):
        text1 = f1.render(f'{board_words[x]}', 1, BLACK)
        screen.blit(text1, (x * cell_size_ramka + 23, 0))

    for y in range(cell_qty):
        for x in range(cell_qty):
            pygame.draw.rect(screen, colors, (x * (cell_size + 2) + board_shift, y * (cell_size + 2) + board_shift, cell_size, cell_size))
            pygame.draw.rect(screen, BLACK,
                             (x * cell_size_ramka + board_shift, y * cell_size_ramka + board_shift, cell_size_ramka, cell_size_ramka), 2)

            text1 = f1.render(f'{15 - y}', 1, BLACK)
        if 15 - y < 10:
            screen.blit(text1, (5, y * cell_size_ramka + 20))
        else:

            screen.blit(text1, (0, y * cell_size_ramka + 20))
        if y == cell_qty - 1:
            text2 = f1.render('1', 1, BLACK)
            screen.blit(text2, (5, (y + 1) * cell_size_ramka + 20))

def draw_all_shashky(coord_all_move_and_color):
    for index_x_rect, index_y_rect, color_player in  coord_all_move_and_color:
        pygame.draw.circle(screen, color_player,(index_x_rect * cell_size_ramka + board_shift, index_y_rect * cell_size_ramka + board_shift), 10)

def draw_screen():
    screen.fill((255, 255, 255))

def text_output_number_of_movies(number_of_movies):
    text = f1.render(f'Количество ходов: {number_of_movies}', 1, BLACK)
    screen.blit(text, (100, 700))

    #text_move = f1.render(f'Ходы: {coord_all_move_and_color}', 1, BLACK)
    #screen.blit(text_move, (100, 750))

def text_win(color):
    if color == BLACK:
        text = f1.render(f'Игра закончилась. Победили черные!!', 1, BLACK)
        screen.blit(text, (100, 850))
    else:
        text = f1.render(f'Игра закончилась. Победили белые!!', 1, BLACK)
        screen.blit(text, (100, 850))


def give_coord(events):
    x, y = events.pos
    x, y = x - board_shift, y - board_shift
    return x,y

def give_coord_rect(events):
    x,y = give_coord(events)

    index_x_rect = round(x / cell_size_ramka)
    index_y_rect = round(y / cell_size_ramka)

    return index_x_rect,index_y_rect

def change_color_player(color_player):
    if color_player == BLACK:
        color_player = WHITE
    else:
        color_player = BLACK

    return color_player





pygame.init()
screen = pygame.display.set_mode((900, 900))
pygame.display.set_caption("MY game")
#icon = pygame.image.load("images/icon.png")
#pygame.display.set_icon(icon)


f1 = pygame.font.Font(None, 36)
screen.fill((255, 255, 255))









