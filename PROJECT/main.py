import pygame
import sys
from Graphics.Graphics_main import *
from analitycs.analitycs_main import *
from Brain.Brain_main import *
from Const import *
import copy

win_color = None
color_player = BLACK
color_computer = WHITE
number_of_movies = 0

game_graphics = Game_Graphics(now_coord_all_move_and_color, number_of_movies)
game_graphics.draw_all_game()

game_player_analityc = Analitycs(now_coord_all_move_and_color, color_player)


run = True
while run:

    event = game_player_analityc.now_event()

    if number_of_movies % 2 != 0 and win_color == None and False:
        print("!@")
        #best_value, (index_x_rect, index_y_rect) = minimax(((game_player_analityc.give_line(), copy.copy(all_line_whiteplayer)), copy.copy(now_coord_all_move_and_color)), 5, True, float('-inf'), float('inf'))
        #game_graphics.set_coord(index_x_rect, index_y_rect, color_computer)
        #number_of_movies += 1

        #if color_computer == WHITE:
            #adding_lines(index_x_rect, index_y_rect, all_line_whiteplayer, color_computer, all_coord_all_move_and_color)
        #else:
            #adding_lines(index_x_rect, index_y_rect, all_line_blackplayer, color_computer, all_coord_all_move_and_color)
        #win_color = check_colors_win(all_coord_all_move_and_color, all_line_blackplayer, all_line_whiteplayer)

        #position_score = find_position_score((all_line_blackplayer, all_line_whiteplayer), all_coord_all_move_and_color)
        #print(position_score, "!@#@#", best_value)

    else:
        if event != None:
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            if event.button == 1:
                check_x, check_y = give_coord(event)

                check_correct_motion = game_player_analityc.check_motion(check_x, check_y)
                if check_correct_motion == True and win_color == None:
                    index_x_rect, index_y_rect = give_coord_rect(event)
                    game_graphics.set_coord(index_x_rect, index_y_rect, color_player)

                    number_of_movies += 1
                    if color_player == WHITE:
                        game_player_analityc.adding_lines(index_x_rect, index_y_rect, color_player)
                    else:
                        game_player_analityc.adding_lines(index_x_rect, index_y_rect, color_player)

                    print(game_player_analityc.give_all_line_blackplayer())
                    win_color = game_player_analityc.check_colors_win()


                check_newgame = check_want_newgame(check_x, check_y)
                if check_newgame == True:
                    win_color = None
                    number_of_movies = 0
                    all_line_whiteplayer = []
                    all_line_blackplayer = []
                    check_win_black = False
                    check_win_white = False
                    coord_all_move_and_color = []

    game_graphics.draw_all_game()

