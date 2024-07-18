import sys
from Graphics.Graphics_main import *
from PROJECT.Brain_main import *
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
    color_user = white
    color_computer = black
    IsMaximing_computer = False
    is_now_computer = True
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

    board_player = Board(color_user)

    run = True
    while run:
        event = now_event()

        if is_now_computer and win_color == -1:
            Board_MinMax = Board(color_computer, board_player.give_all_line_blackplayer(), board_player.give_all_line_whiteplayer(), board_player.give_chips())
            if possible_moves_black_pl.get((index_x_rect, index_y_rect)) is not None:
                possible_moves_black_pl.pop((index_x_rect, index_y_rect))
            if possible_moves_white_pl.get((index_x_rect, index_y_rect)) is not None:
                possible_moves_white_pl.pop((index_x_rect, index_y_rect))
            next_variants_move_and_motion = ( (index_x_rect, index_y_rect),create_independent_dict(possible_moves_black_pl), create_independent_dict(possible_moves_white_pl))

            if game_graphics.give_number_move() > 0:
                best_value, coord_best_move, count_all_variants = minimax(Board_MinMax, 7, next_variants_move_and_motion, IsMaximing_computer, float('-inf'), float('inf'), 0)
            else:
                coord_best_move = (6,6)
                count_all_variants = 0

            print("3#@#", count_all_variants)

            game_graphics.set_coord(coord_best_move[0], coord_best_move[1], color_computer)
            board_player.set_coord(coord_best_move[0], coord_best_move[1], color_computer)

            if color_computer == white:
                possible_moves_black_pl, possible_moves_white_pl = new_generator_motion(coord_best_move, board_player.give_chips(), create_independent_dict(possible_moves_black_pl), create_independent_dict(possible_moves_white_pl), white)
            else:
                possible_moves_white_pl, possible_moves_black_pl = new_generator_motion(coord_best_move, board_player.give_chips(), create_independent_dict(possible_moves_white_pl), create_independent_dict(possible_moves_black_pl), black)

            game_graphics.set_number_move()

            board_player.adding_lines(coord_best_move[0], coord_best_move[1], color_computer)

            win_color = board_player.check_colors_win()
            is_now_computer = not is_now_computer

        else:
            if event != None:
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.button == 1:
                    check_x, check_y = give_coord(event)

                    check_correct_motion = board_player.check_motion(check_x, check_y)
                    if check_correct_motion == True and win_color == -1:
                        index_x_rect, index_y_rect = give_coord_rect(event)
                        game_graphics.set_coord(index_x_rect, index_y_rect, color_user)
                        board_player.set_coord(index_x_rect, index_y_rect, color_user)

                        game_graphics.set_number_move()
                        board_player.adding_lines(index_x_rect, index_y_rect, color_user)

                        #print("Black", board_player.give_all_line_blackplayer())
                        win_color = board_player.check_colors_win()
                        is_now_computer = not is_now_computer

                    check_newgame = check_want_newgame(check_x, check_y)
                    if check_newgame == True:
                        del game_graphics
                        del board_player

                        win_color = -1
                        number_of_movies = 0

                        game_graphics = Game_Graphics( number_of_movies)

                        board_player = Board(color_user)

        game_graphics.draw_all_game(win_color)


if __name__ == "__main__":
    main()

