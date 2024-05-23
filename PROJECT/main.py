import pygame
import sys
from Graphics.Graphics_main import *
from analitycs.analitycs_main import *
from Brain.Brain_main import *
from Const import *

draw_main_board(cell_qty,cell_size,cell_size_ramka)
pygame.display.update()

win_color = None
color_player = BLACK
color_computer = WHITE
number_of_movies = 0


run = True
while run:

    event = now_event()

    if number_of_movies % 2 != 0 and win_color == None:
        index_x_rect, index_y_rect = generator_motion(color_computer)
        coord_all_move_and_color.append((index_x_rect, index_y_rect, color_computer))

        number_of_movies += 1

        adding_lines(index_x_rect, index_y_rect, color_computer, coord_all_move_and_color)
        win_color = check_colors_win()

    else:
        if event != None:
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            if event.button == 1:

                if win_color == None:
                    check_x, check_y = give_coord(event)
                    check_correct_motion = check_motion(check_x, check_y, coord_all_move_and_color)
                    if check_correct_motion == True:
                        index_x_rect, index_y_rect = give_coord_rect(event)
                        coord_all_move_and_color.append((index_x_rect, index_y_rect, color_player))

                        number_of_movies += 1

                        adding_lines(index_x_rect, index_y_rect, color_player, coord_all_move_and_color)
                        win_color = check_colors_win()


    draw_all_game(win_color,number_of_movies, coord_all_move_and_color)

