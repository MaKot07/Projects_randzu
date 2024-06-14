import pygame
import sys
from Graphics.Graphics_main import *
from analitycs.analitycs_main import *
from Brain.Brain_main import *
from Const import *
import copy

win_color = None
color_user = BLACK
color_computer = WHITE
number_of_movies = 0

game_graphics = Game_Graphics(now_coord_all_move_and_color, number_of_movies)
game_graphics.draw_all_game(win_color)

game_player_analityc = Analitycs(now_coord_all_move_and_color, color_user)


run = True
while run:

    event = game_player_analityc.now_event()

    if game_graphics.give_number_move() % 2 != 0 and win_color == None:
        MinMax = Intelect(game_player_analityc.give_all_line_blackplayer(), game_player_analityc.give_all_line_whiteplayer(), game_player_analityc.give_chips(), color_computer)
        best_value, (index_x_rect, index_y_rect) = MinMax.minimax(3, True, float('-inf'), float('inf'))

        game_graphics.set_coord(index_x_rect, index_y_rect, color_computer)
        game_player_analityc.set_coord(index_x_rect, index_y_rect, color_computer)

        game_graphics.set_number_move()

        game_player_analityc.adding_lines(index_x_rect, index_y_rect, color_computer)


        win_color = game_player_analityc.check_colors_win()

        del MinMax

        now_pose_score = Intelect(game_player_analityc.give_all_line_blackplayer(), game_player_analityc.now_all_line_whiteplayer,game_player_analityc.now_coord_all_move_and_color, game_player_analityc.color)
        print("Score ", now_pose_score.find_position_score())
        del now_pose_score

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
                    game_graphics.set_coord(index_x_rect, index_y_rect, color_user)
                    game_player_analityc.set_coord(index_x_rect, index_y_rect, color_user)


                    game_graphics.set_number_move()
                    game_player_analityc.adding_lines(index_x_rect, index_y_rect, color_user)


                    print("Black",game_player_analityc.give_all_line_blackplayer())
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

    game_graphics.draw_all_game(win_color)

