import sys
from Graphics.Graphics_main import *
from PROJECT.Brain_main import *
from neural_network import *
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
    win_color = 0
    color_user = black
    color_computer = white
    number_of_movies = 0
    index_x_rect, index_y_rect = 7, 7
    len_board = 15
    play_neural_network = True
    if play_neural_network:
        model = keras.models.load_model(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\best_model.keras')

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

    if color_computer == white:
        comp_move = False
    else:
        comp_move = True

    run = True
    while run:
        event = now_event()

        if comp_move and win_color == 0:
            if play_neural_network:
                if game_graphics.give_number_move() > 3:

                    position = np.zeros((1,225), dtype=np.int8)
                    for i in range(len(board_player.give_chips())):
                        position[0][board_player.give_chips()[i][1] * len_board + board_player.give_chips()[i][0]] = board_player.give_chips()[i][2]
                    if np.sum(position[0]) == 0:
                        for j in range(len(position[0])):
                            position[0][j] = 1 if position[0][j] == -1 else 0.5
                    else:
                        for j in range(len(position[0])):
                            position[0][j] = 1 if position[0][j] == 1 else 0.5

                    #для старой модели
                    # not_convert_coord = model.predict(position)[0]
                    # label = np.where(not_convert_coord == max(not_convert_coord))[0][0]
                    # coord_best_move = (label-(label//15)*15, label//15)

                    not_round_coord_best_move = model.predict(position)[0]
                    coord_best_move = (round(not_round_coord_best_move[0]), round(not_round_coord_best_move[1]))

                    game_graphics.set_coord(coord_best_move[0], coord_best_move[1], color_computer)
                    board_player.set_coord(coord_best_move[0], coord_best_move[1], color_computer)

                    game_graphics.set_number_move()

                    board_player.adding_lines(coord_best_move[0], coord_best_move[1], color_computer)

                    win_color = board_player.check_colors_win()
                    comp_move = not comp_move
                else:
                    maximizing = True if color_computer == white else False
                    variants_move = silly_P_generator_motion(board_player.give_chips())

                    Board_SillyMinMax = Board(color_computer, board_player.give_all_line_blackplayer(),
                                              board_player.give_all_line_whiteplayer(), board_player.give_chips())

                    _, coord_best_move, c = sily_minimax(Board_SillyMinMax, 1, variants_move, maximizing)

                    game_graphics.set_coord(coord_best_move[0], coord_best_move[1], color_computer)
                    board_player.set_coord(coord_best_move[0], coord_best_move[1], color_computer)

                    game_graphics.set_number_move()

                    board_player.adding_lines(coord_best_move[0], coord_best_move[1], color_computer)

                    win_color = board_player.check_colors_win()
                    comp_move = not comp_move

            else:
                Board_MinMax = Board(color_computer, board_player.give_all_line_blackplayer(), board_player.give_all_line_whiteplayer(), board_player.give_chips())
                if possible_moves_black_pl.get((index_x_rect, index_y_rect)) is not None:
                    possible_moves_black_pl.pop((index_x_rect, index_y_rect))
                if possible_moves_white_pl.get((index_x_rect, index_y_rect)) is not None:
                    possible_moves_white_pl.pop((index_x_rect, index_y_rect))
                next_variants_move_and_motion = ( (index_x_rect, index_y_rect),create_independent_dict(possible_moves_black_pl), create_independent_dict(possible_moves_white_pl))

                maxim = True if color_computer == white else False
                best_value, coord_best_move, count_all_variants = minimax(Board_MinMax, 35, next_variants_move_and_motion, maxim, float('-inf'), float('inf'), 0)

                print("3#@#", count_all_variants)

                game_graphics.set_coord(coord_best_move[0], coord_best_move[1], color_computer)
                board_player.set_coord(coord_best_move[0], coord_best_move[1], color_computer)

                possible_moves_black_pl, possible_moves_white_pl = new_generator_motion(coord_best_move, board_player.give_chips(), create_independent_dict(possible_moves_black_pl), create_independent_dict(possible_moves_white_pl), white)

                game_graphics.set_number_move()

                board_player.adding_lines(coord_best_move[0], coord_best_move[1], color_computer)

                win_color = board_player.check_colors_win()
                comp_move = not comp_move

        else:
            if event != None:
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit()

                if event.button == 1:
                    check_x, check_y = give_coord(event)

                    check_correct_motion = board_player.check_motion(check_x, check_y)
                    if check_correct_motion == True and win_color == 0:
                        index_x_rect, index_y_rect = give_coord_rect(event)
                        game_graphics.set_coord(index_x_rect, index_y_rect, color_user)
                        board_player.set_coord(index_x_rect, index_y_rect, color_user)

                        game_graphics.set_number_move()
                        board_player.adding_lines(index_x_rect, index_y_rect, color_user)

                        #print("Black", board_player.give_all_line_blackplayer())
                        win_color = board_player.check_colors_win()
                        comp_move = not comp_move

                    check_newgame = check_want_newgame(check_x, check_y)
                    if check_newgame == True:
                        del game_graphics
                        del board_player

                        win_color = 0
                        number_of_movies = 0

                        game_graphics = Game_Graphics( number_of_movies)

                        board_player = Board(color_user)

        game_graphics.draw_all_game(win_color)


if __name__ == "__main__":
    main()

