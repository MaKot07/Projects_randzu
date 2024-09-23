import numpy as np
import copy
from Graphics.Graphics_main import *
import sys
from Brain_main import *
import pandas as pd
import pickle

def generation_position_and_save(n, number_move):

    black = -1
    white = 1
    cell_qty = 14
    color_move = black
    percent_random = 0.1
    percent_depth1 = 0.4

    ni = 0
    while ni < n:
        sgen_board = Board(black)

        coord_move = (np.random.randint(5, 7), np.random.randint(5, 7))
        sgen_board.set_coord(coord_move[0], coord_move[1], black)
        sgen_board.adding_lines(coord_move[0], coord_move[1], black)

        variants_move = P_generator_motion(coord_move, sgen_board.give_chips())
        coord_move = variants_move[np.random.randint(0, len(variants_move)-1)]
        sgen_board.set_coord(coord_move[0], coord_move[1], white)
        sgen_board.adding_lines(coord_move[0], coord_move[1], white)

        for i in range(number_move-2):
            level_choice = np.random.random()

            if level_choice <= percent_random:
                variants_move = P_generator_motion(coord_move, sgen_board.give_chips(), copy.copy(variants_move))
                coord_move = variants_move[np.random.randint(0, len(variants_move)-1)]


                sgen_board.set_coord(coord_move[0], coord_move[1], color_move)
                sgen_board.adding_lines(coord_move[0], coord_move[1], color_move)
                make_position(sgen_board.give_chips(), [sgen_board.give_all_line_blackplayer(), sgen_board.give_all_line_whiteplayer()])

            elif level_choice <= percent_depth1:
                maximizing = True if color_move == white else False
                variants_move = P_generator_motion(coord_move, sgen_board.give_chips(), copy.copy(variants_move))

                Board_SillyMinMax = Board(color_move, sgen_board.give_all_line_blackplayer(),
                                     sgen_board.give_all_line_whiteplayer(), sgen_board.give_chips())

                _, coord_move, c = sily_minimax(Board_SillyMinMax, 1, variants_move, maximizing)

                sgen_board.set_coord(coord_move[0], coord_move[1], color_move)
                sgen_board.adding_lines(coord_move[0], coord_move[1], color_move)

                make_position(sgen_board.give_chips(), [sgen_board.give_all_line_blackplayer(), sgen_board.give_all_line_whiteplayer()])

            else:
                maximizing = True if color_move == white else False
                variants_move = P_generator_motion(coord_move, sgen_board.give_chips(), copy.copy(variants_move))

                Board_SillyMinMax = Board(color_move, sgen_board.give_all_line_blackplayer(),
                                          sgen_board.give_all_line_whiteplayer(), sgen_board.give_chips())

                _, coord_move, _ = sily_minimax(Board_SillyMinMax, 2, variants_move, maximizing)

                sgen_board.set_coord(coord_move[0], coord_move[1], color_move)
                sgen_board.adding_lines(coord_move[0], coord_move[1], color_move)

                make_position(sgen_board.give_chips(), [sgen_board.give_all_line_blackplayer(), sgen_board.give_all_line_whiteplayer()])

            win_color = sgen_board.check_colors_win()
            if win_color != 0:
                break

            if color_move == black:
                color_move = white
            else:
                color_move = black

            ni += 1



def make_position(all_coords, all_lines):
    len_board = 15
    position = np.zeros((225), dtype=np.int8)

    for i in range(len(all_coords)):
        position[ all_coords[i][1]*len_board + all_coords[i][0] ] = all_coords[i][2]


    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data.csv', 'a', newline='') as file:
        np.savetxt(file, [position], delimiter=',', newline='\n', fmt='%d')

    # with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(black).csv', 'a', newline='') as file:
    #     np.savetxt(file, np.vstack(all_lines[0]), delimiter=',', newline='\n', fmt='%d')
    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(black).csv', 'ab') as file:
        pickle.dump(all_lines[0], file)


    # with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(white).csv', 'a', newline='') as file:
    #     np.savetxt(file, np.vstack(all_lines[1]), delimiter=',', newline='\n', fmt='%d')
    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(white).csv', 'ab') as file:
        pickle.dump(all_lines[1], file)

def sily_minimax(board_condition, depth, last_variants, maximizingPlayer, alpha=float('-inf'), beta=float('inf'), count_variants=0):

    if board_condition.check_colors_win() != 0:
        return (board_condition.find_win_position_score(), (-1,-1), count_variants)
    if depth <= 0:
        bl_line = board_condition.now_all_line_blackplayer
        wh_line = board_condition.now_all_line_whiteplayer
        all_coord = board_condition.now_coord_all_move_and_color
        return (find_position_score(bl_line, wh_line, all_coord), (-1,-1), count_variants)

    if maximizingPlayer:
        value = float('-inf')

        for move in last_variants:
            child = board_condition.get_new_state(move, black)
            new_variants_move = P_generator_motion(move, board_condition.give_chips(), copy.copy(last_variants))

            count_variants += 1
            #print("#@%", count_variants)
            tmp, _, count_variants = sily_minimax(child, depth - 1, copy.copy(new_variants_move), not maximizingPlayer, alpha, beta, count_variants)

            if tmp > value:
                value = tmp
                best_movement = move

            if value > beta:
                break
            alpha = max(alpha, value)

    else:
        value = float('inf')

        for move in last_variants:
            child = board_condition.get_new_state(move, white)
            new_variants_move = P_generator_motion(move, board_condition.give_chips(), copy.copy(last_variants))

            count_variants += 1
            #print("#@%", count_variants)
            tmp, _, count_variants = sily_minimax(child, depth - 1, copy.copy(new_variants_move), not maximizingPlayer, alpha, beta, count_variants)

            if tmp < value:
                value = tmp
                best_movement = move

            if value < alpha:
                break
            beta = min(beta, value)

    return value, best_movement, count_variants


#Visualisation
def show_positions():
    positions = np.loadtxt(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data.csv', delimiter=',',
                     dtype=int)

    # all_black_lines = np.loadtxt(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(black).csv', delimiter=',',
    #                  dtype=int)
    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(black).csv', 'rb') as file:
        all_black_lines = []
        while True:
            try:
                all_black_lines.append(pickle.load(file))
            except EOFError:
                break


    # all_white_lines = np.loadtxt(
    #     r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(white).csv', delimiter=',',
    #     dtype=int)
    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(white).csv', 'rb') as file:
        all_white_lines = []
        while True:
            try:
                all_white_lines.append(pickle.load(file))
            except EOFError:
                break

    i = 0

    Visual_board = Game_Graphics(0)
    Visual_board.draw_all_game(0)

    while True:
        event = now_event()

        if event != None:
            if event.type == pygame.QUIT:
                run = False
                sys.exit()

            if event.button == 1:
                Visual_board = Game_Graphics(0, convert_positions(positions[i]))
                Visual_board.draw_all_game(0)
                print("BLACK", all_black_lines[i])
                print("WHITE", all_white_lines[i])

                i +=1
                if i == len(positions):
                    sys.exit()

def now_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return event

        if event.type == pygame.MOUSEBUTTONDOWN:
            return event

def convert_positions(position):
    len_board = 15

    conv_pos = []

    for i in range(len_board):
        for j in range(len_board):
            if position[ i*len_board + j ] != 0:
                conv_pos.append(( j, i, position[ i*len_board + j ] ))

    return conv_pos


# def generation_labels():
#     positions = np.loadtxt(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data.csv',
#                            delimiter=',',
#                            dtype=int)
#
#     with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(black).csv', 'rb') as file:
#         all_black_lines = []
#         while True:
#             try:
#                 all_black_lines.append(pickle.load(file))
#             except EOFError:
#                 break
#
#     with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(white).csv', 'rb') as file:
#         all_white_lines = []
#         while True:
#             try:
#                 all_white_lines.append(pickle.load(file))
#             except EOFError:
#                 break
#
#     possible_moves_white_pl = typed.Dict.empty(
#         key_type=types.UniTuple(types.int64, 2),
#         value_type=numba.types.int64
#     )
#     possible_moves_black_pl = typed.Dict.empty(
#         key_type=types.UniTuple(types.int64, 2),
#         value_type=numba.types.int64
#     )
#
#     for sample in len(all_black_lines):
#         Board_MinMax = Board(positions[sample][-1],all_black_lines[sample],
#                              all_white_lines[sample], convert_positions(positions[sample]))
#
#
#
#         next_variants_move_and_motion = ((index_x_rect, index_y_rect), create_independent_dict(possible_moves_black_pl),
#                                          create_independent_dict(possible_moves_white_pl))
#
#         maxim = True if color_computer == white else False
#         best_value, coord_best_move, count_all_variants = minimax(Board_MinMax, 40, next_variants_move_and_motion,
#                                                                   maxim, float('-inf'), float('inf'), 0)






#generation_position_and_save(100, 50)



show_positions()