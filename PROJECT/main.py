import sys
import time

from Graphics.Graphics_main import *
from Brain_main import *
import numpy as np
from numba import typed
import numba
from numba import typed, types

def now_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return event

        if event.type == pygame.MOUSEBUTTONDOWN:
            return event

def main():
    win_color = -1
    color_user = black
    color_computer = white
    number_of_movies = 0
    index_x_rect, index_y_rect = 7, 7

    possible_moves_white_pl = typed.Dict.empty(
        key_type=types.UniTuple(types.int64, 2),
        value_type=numba.types.int64
    )
    possible_moves_black_pl = typed.Dict.empty(
        key_type=types.UniTuple(types.int64, 2),
        value_type=numba.types.int64
    )

    game_graphics = Game_Graphics(number_of_movies)
    game_graphics.draw_all_game(win_color)

    board = Board(color_user)
    
    Player_play = False
    if not Player_play:
        maximiz = False
        color_computer = black
    else:
        if color_computer == white:
            comp_move = False
            maximiz = True
        else:
            comp_move = True
            maximiz = False

    run = True
    while run:
        if Player_play:
            event = now_event()
            if comp_move != 0 and win_color == -1:
                Board_MinMax = Board(color_computer, board.give_all_line_blackplayer(), board.give_all_line_whiteplayer(), board.give_chips())
                if possible_moves_black_pl.get((index_x_rect, index_y_rect)) is not None:
                    possible_moves_black_pl.pop((index_x_rect, index_y_rect))
                if possible_moves_white_pl.get((index_x_rect, index_y_rect)) is not None:
                    possible_moves_white_pl.pop((index_x_rect, index_y_rect))
                next_variants_move_and_motion = ( (index_x_rect, index_y_rect),create_independent_dict(possible_moves_black_pl), create_independent_dict(possible_moves_white_pl))

                if game_graphics.give_number_move() == 0:
                    coord_best_move = (6, 6)
                    count_all_variants = 0
                else:
                    best_value, coord_best_move, count_all_variants = minimax(Board_MinMax, 5, next_variants_move_and_motion, maximiz, float('-inf'), float('inf'), 0)
    
                print("3#@#", count_all_variants)
    
                game_graphics.set_coord(coord_best_move[0], coord_best_move[1], color_computer)
                board.set_coord(coord_best_move[0], coord_best_move[1], color_computer)

                if color_computer == white:
                    possible_moves_black_pl, possible_moves_white_pl = new_generator_motion(coord_best_move,board.give_chips(),create_independent_dict(possible_moves_black_pl),create_independent_dict(possible_moves_white_pl),white)
                else:
                    possible_moves_white_pl, possible_moves_black_pl = new_generator_motion(coord_best_move,board.give_chips(),create_independent_dict(possible_moves_white_pl),create_independent_dict(possible_moves_black_pl),black)
    
                game_graphics.set_number_move()
    
                board.adding_lines(coord_best_move[0], coord_best_move[1], color_computer)
    
                win_color = board.check_colors_win()
                comp_move = not comp_move

            else:
                if event != None:
                    if event.type == pygame.QUIT:
                        run = False
                        sys.exit()
    
                    if event.button == 1:
                        check_x, check_y = give_coord(event)
    
                        check_correct_motion = board.check_motion(check_x, check_y)
                        if check_correct_motion == True and win_color == -1:
                            index_x_rect, index_y_rect = give_coord_rect(event)
                            game_graphics.set_coord(index_x_rect, index_y_rect, color_user)
                            board.set_coord(index_x_rect, index_y_rect, color_user)
    
                            game_graphics.set_number_move()
                            board.adding_lines(index_x_rect, index_y_rect, color_user)
    
                            #print("Black", board.give_all_line_blackplayer())
                            win_color = board.check_colors_win()
                            comp_move = not comp_move
    
                        check_newgame = check_want_newgame(check_x, check_y)
                        if check_newgame == True:
                            del game_graphics
                            del board
    
                            win_color = -1
                            number_of_movies = 0
    
                            game_graphics = Game_Graphics( number_of_movies)
    
                            board = Board(color_user)
    
            game_graphics.draw_all_game(win_color)
            
        else:
            if win_color == -1:
                Board_MinMax = Board(color_computer, board.give_all_line_blackplayer(),board.give_all_line_whiteplayer(), board.give_chips())
                if possible_moves_black_pl.get((index_x_rect, index_y_rect)) is not None:
                    possible_moves_black_pl.pop((index_x_rect, index_y_rect))
                if possible_moves_white_pl.get((index_x_rect, index_y_rect)) is not None:
                    possible_moves_white_pl.pop((index_x_rect, index_y_rect))
                next_variants_move_and_motion = ((index_x_rect, index_y_rect), create_independent_dict(possible_moves_black_pl),create_independent_dict(possible_moves_white_pl))

                if number_of_movies == 0:
                    coord_best_move = (6, 6)
                    count_all_variants = 0
                else:
                    best_value, coord_best_move, count_all_variants = minimax(Board_MinMax, 5,next_variants_move_and_motion, maximiz, float('-inf'), float('inf'), 0)

                index_x_rect, index_y_rect = coord_best_move
                print("3#@#", count_all_variants)
    
                game_graphics.set_coord(coord_best_move[0], coord_best_move[1], color_computer)
                board.set_coord(coord_best_move[0], coord_best_move[1], color_computer)

                if color_computer == white:
                    possible_moves_black_pl, possible_moves_white_pl = new_generator_motion(coord_best_move,board.give_chips(),create_independent_dict(possible_moves_black_pl),create_independent_dict(possible_moves_white_pl), white)
                else:
                    possible_moves_white_pl, possible_moves_black_pl = new_generator_motion(coord_best_move,board.give_chips(),create_independent_dict(possible_moves_white_pl),create_independent_dict(possible_moves_black_pl), black)
    
                game_graphics.set_number_move()
    
                board.adding_lines(coord_best_move[0], coord_best_move[1], color_computer)
    
                win_color = board.check_colors_win()
                maximiz = not maximiz
                number_of_movies += 1
                if color_computer == white:
                    color_computer = black
                else:
                    color_computer = white

            game_graphics.draw_all_game(win_color)
            time.sleep(0.5)


if __name__ == "__main__":
    main()

