

from Brain_main import *
import time
import numba
from numba import typed, types

def create_graphics():
    print()




def create_data(n, number_move):

    black = -1
    white = 1
    cell_qty = 14
    color_move = black


    ni = 0
    while ni < n:
        print(f'{ni} из {n}')
        sgen_board = Board(black)
        possible_moves = typed.Dict.empty(
            key_type=types.UniTuple(types.int64, 2),
            value_type=numba.types.float64
        )
        coord_best_move = [-1,-1]

        time_array = np.zeros((number_move))
        for i in range(number_move):
            print(i)
            time_start = time.time()

            if color_move == black:
                Board_MinMax = Board(color_move, sgen_board.give_all_line_blackplayer(),
                                     sgen_board.give_all_line_whiteplayer(), sgen_board.give_chips())

                possible_moves.pop((coord_best_move[0], coord_best_move[1]), None)

                next_variants_move_and_motion = ((coord_best_move[0], coord_best_move[1]), create_independent_dict(possible_moves))

                maxim = False
                best_value, coord_best_move, count_all_variants = minimax(Board_MinMax, 15,
                                                                          next_variants_move_and_motion, maxim,
                                                                          float('-inf'), float('inf'), 0)


                possible_moves = new_generator_motion_for_minmax(
                    next_variants_move_and_motion[0], sgen_board.give_chips(),
                    create_independent_dict(next_variants_move_and_motion[1]),
                    sgen_board.give_all_line_whiteplayer())

                sgen_board.set_coord(coord_best_move[0], coord_best_move[1], color_move)

                sgen_board.adding_lines(coord_best_move[0], coord_best_move[1], color_move)


                possible_moves = new_generator_motion_for_minmax(coord_best_move,
                                                                 sgen_board.give_chips(),
                                                                 create_independent_dict(
                                                                     possible_moves),
                                                                 sgen_board.give_all_line_blackplayer())
            else:
                Board_MinMax = Board(color_move, sgen_board.give_all_line_blackplayer(),
                                     sgen_board.give_all_line_whiteplayer(), sgen_board.give_chips())

                possible_moves.pop((coord_best_move[0], coord_best_move[1]), None)

                next_variants_move_and_motion = (
                (coord_best_move[0], coord_best_move[1]), create_independent_dict(possible_moves))

                maxim = True
                best_value, coord_best_move, count_all_variants = minimax(Board_MinMax, 15,
                                                                          next_variants_move_and_motion, maxim,
                                                                          float('-inf'), float('inf'), 0)

                possible_moves = new_generator_motion_for_minmax(
                    next_variants_move_and_motion[0], sgen_board.give_chips(),
                    create_independent_dict(next_variants_move_and_motion[1]), sgen_board.give_all_line_blackplayer())

                sgen_board.set_coord(coord_best_move[0], coord_best_move[1], color_move)

                sgen_board.adding_lines(coord_best_move[0], coord_best_move[1], color_move)

                possible_moves = new_generator_motion_for_minmax(coord_best_move,
                                                                 sgen_board.give_chips(),
                                                                 create_independent_dict(
                                                                     possible_moves),
                                                                 sgen_board.give_all_line_whiteplayer())

            win_color = sgen_board.check_colors_win()
            if win_color != 0:
                break

            if color_move == black:
                color_move = white
            else:
                color_move = black

            time_end = time.time()

            time_array[i] = time_end - time_start


        ni += 1
        print(time_array)
        add_data(time_array)


def add_data(array):
    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\Banner\data', 'a', newline='') as file:
        np.savetxt(file, [array], delimiter=',', newline='\n', fmt='%f')


create_data(10, 100)