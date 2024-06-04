import pygame
import sys
from Graphics.Graphics_main import *
from analitycs.analitycs_main import *
from Brain.Brain_main import *
from Const import *
import copy

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
        best_value, (index_x_rect, index_y_rect) = minimax(((copy.copy(all_line_blackplayer), copy.copy(all_line_whiteplayer)), coord_all_move_and_color), 10, True, float('-inf'), float('inf'))
        coord_all_move_and_color.append(((index_x_rect, index_y_rect), color_computer))
        number_of_movies += 1

        if color_computer == WHITE:
            adding_lines(index_x_rect, index_y_rect, all_line_whiteplayer, color_computer, coord_all_move_and_color)
        else:
            adding_lines(index_x_rect, index_y_rect, all_line_blackplayer, color_computer, coord_all_move_and_color)
        win_color = check_colors_win(coord_all_move_and_color)

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
                        coord_all_move_and_color.append(((index_x_rect, index_y_rect), color_player))

                        number_of_movies += 1
                        if color_player == WHITE:
                            adding_lines(index_x_rect, index_y_rect, all_line_whiteplayer, color_player, coord_all_move_and_color)
                        else:
                            adding_lines(index_x_rect, index_y_rect, all_line_blackplayer, color_player, coord_all_move_and_color)
                        print(all_line_blackplayer)
                        win_color = check_colors_win(coord_all_move_and_color)

                        position_score = find_position_score((all_line_blackplayer, all_line_whiteplayer), coord_all_move_and_color)
                        print(position_score)


    draw_all_game(win_color,number_of_movies, coord_all_move_and_color)

