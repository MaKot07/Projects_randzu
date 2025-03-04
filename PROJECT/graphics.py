import pickle

import numpy as np

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
                best_value, coord_best_move, count_all_variants = minimax(Board_MinMax, np.random.randint(9, 11),
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
    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\Banner\data1', 'a', newline='') as file:
        np.savetxt(file, [array], delimiter=',', newline='\n', fmt='%f')

def create_data_on_poses(n1,n2):
    positions = np.loadtxt(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data.csv',
                           delimiter=',',
                           dtype=int)

    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(black).csv',
              'rb') as file:
        all_black_lines = []
        while True:
            try:
                all_black_lines.append(pickle.load(file))
            except EOFError:
                break

    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(white).csv',
              'rb') as file:
        all_white_lines = []
        while True:
            try:
                all_white_lines.append(pickle.load(file))
            except EOFError:
                break

    possible_moves = typed.Dict.empty(
        key_type=types.UniTuple(types.int64, 2),
        value_type=numba.types.float64
    )

    time_array = [0] * 100

    for i in range(100):
        time_array[i] = []
    for sample in range(n1,n2):
        print(sample)

        position = convert_positions(positions[sample])

        if len(position) % 2 == 0:
            color_minmax = black
        else:
            color_minmax = white

        Board_MinMax_for_labels = Board(color_minmax, all_black_lines[sample],
                                        all_white_lines[sample], position)

        possible_moves = new_generator_motion_for_create_start_moves(
            Board_MinMax_for_labels.give_chips(), possible_moves,
            Board_MinMax_for_labels.give_all_line_whiteplayer(), white)

        possible_moves = new_generator_motion_for_create_start_moves(
            Board_MinMax_for_labels.give_chips(),
            create_independent_dict(possible_moves), Board_MinMax_for_labels.give_all_line_blackplayer(), black)

        next_variants_move_and_motion = ((-2, -2), create_independent_dict(possible_moves))

        time_start = time.time()

        maxim = True if color_minmax == white else False
        best_value, coord_best_move, count_all_variants = minimax(Board_MinMax_for_labels, 10,
                                                                  next_variants_move_and_motion,
                                                                  maxim, float('-inf'), float('inf'), 0)
        time_end = time.time()
        time_array[len(position)].append(time_end - time_start)

    print(time_array)
    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\Banner\data', 'ab') as file:
        pickle.dump(time_array, file)


def convert_positions(position):
    len_board = 15

    conv_pos = []

    for i in range(len_board):
        for j in range(len_board):
            if position[ i*len_board + j ] != 0:
                conv_pos.append(np.array(( j, i, position[ i*len_board + j ] )))

    return np.array(conv_pos, dtype=np.int8)

@njit
def new_generator_motion_for_create_start_moves(now_coord_all_move_and_color, dict_with_variants, line_enemy, color_enemy):
    if not now_coord_all_move_and_color.any():
        dict_with_variants[(7, 7)] = 0.001
        return dict_with_variants

    coefficent = [0.3, 0.5, 0.6, 0.7]
    empty = np.array([-1, -1], dtype=np.int8)

    all_coords = []
    for coord in now_coord_all_move_and_color:
        if coord[2] == color_enemy:
            all_coords.append((coord[0], coord[1]))

    for new_coord_motion in all_coords:
        new_coord_motion = np.array(new_coord_motion)
        for line in line_enemy:
            if not check_in_2D_array(new_coord_motion, line):
                continue
            if np.array_equal(line[1], empty):
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        chip = (new_coord_motion[0] + i, new_coord_motion[1] + j)

                        if chip not in dict_with_variants and check_motion_for_brain(chip[0], chip[1],
                                                                                     now_coord_all_move_and_color):
                            dict_with_variants[chip] = coefficent[0]

                continue

            line_length = give_len_line(line)
            x_progressive = line[1][0] - line[0][0]
            y_progressive = line[1][1] - line[0][1]

            coord_new_max = (
                x_progressive + line[line_length - 1][0], y_progressive + line[line_length - 1][1])
            coord_new_min = (line[0][0] - x_progressive, line[0][1] - y_progressive)

            for coord in [coord_new_max, coord_new_min]:
                if check_motion_for_brain(coord[0], coord[1], now_coord_all_move_and_color):
                    if dict_with_variants.get(coord) is not None:
                        if dict_with_variants.get(coord) >= coefficent[1]:
                            dict_with_variants[coord] = coefficent[3]
                            continue

                        if line_length == 2:
                            dict_with_variants[coord] = coefficent[1]
                        elif line_length >= 3:
                            dict_with_variants[coord] = coefficent[2]

                    else:
                        if line_length == 2:
                            dict_with_variants[coord] = coefficent[1]
                        elif line_length >= 3:
                            dict_with_variants[coord] = coefficent[2]

    return dict_with_variants




create_data(10, 100)
# create_data_on_poses(0, 100)

