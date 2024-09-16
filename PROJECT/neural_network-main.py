import numpy as np
import copy
from Graphics.Graphics_main import *
import sys
from Brain_main import *
import pandas as pd

def generation_position_and_save(n, number_move):
    if n%number_move != 0:
        raise SystemExit("n не делится на number_move")

    black = -1
    white = 1
    cell_qty = 14
    color_move = black
    percent_random = 0.1
    percent_depth1 = 0.5


    for sample in range(int(n/number_move)):
        sgen_board = Board(black)

        coord_move = (np.random.randint(0, 11), np.random.randint(0, 11))
        sgen_board.set_coord(coord_move[0], coord_move[1], black)
        sgen_board.adding_lines(coord_move[0], coord_move[1], black)

        variants_move = P_generator_motion(coord_move, sgen_board.give_chips())
        coord_move = variants_move[np.random.randint(0, len(variants_move)-1)]
        sgen_board.set_coord(coord_move[0], coord_move[1], white)
        sgen_board.adding_lines(coord_move[0], coord_move[1], white)

        for i in range(number_move-2):
            level_choice = np.random.random()

            if level_choice <= percent_random:
                variants_move = P_generator_motion(coord_move, sgen_board.give_chips(), variants_move)
                coord_move = variants_move[np.random.randint(0, len(variants_move)-1)]

                try:
                    sgen_board.set_coord(coord_move[0], coord_move[1], color_move)
                    sgen_board.adding_lines(coord_move[0], coord_move[1], color_move)
                except  Exception:
                    print(coord_move, " Слишком мал")

                make_position(sgen_board.give_chips())

            elif level_choice <= 0.4:
                maximizing = True if color_move == white else False
                _, coord_move, _ = sily_minimax(sgen_board, 1, variants_move, maximizing)


                sgen_board.set_coord(coord_move[0], coord_move[1], color_move)
                sgen_board.adding_lines(coord_move[0], coord_move[1], color_move)

                variants_move = P_generator_motion(coord_move, sgen_board.give_chips(), variants_move)

                make_position(sgen_board.give_chips())

            else:
                maximizing = True if color_move == white else False
                _, coord_move, _ = sily_minimax(sgen_board, 2, variants_move, maximizing)

                sgen_board.set_coord(coord_move[0], coord_move[1], color_move)
                sgen_board.adding_lines(coord_move[0], coord_move[1], color_move)

                variants_move = P_generator_motion(coord_move, sgen_board.give_chips(), variants_move)

                make_position(sgen_board.give_chips())

            if color_move == black:
                color_move = white
            else:
                color_move = black


def make_position(all_coords):
    len_board = 14
    position = np.zeros((255), dtype=np.int8)

    for i in range(len(all_coords)):
        position[ all_coords[i][1]*len_board + all_coords[i][0] ] = all_coords[i][2]


    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data.csv', 'a', newline='') as file:
        np.savetxt(file, [position], delimiter=',', newline='\n', fmt='%d')


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
            new_variants_move = P_generator_motion(move, board_condition.give_chips(), last_variants)

            tmp, _, count_variants = sily_minimax(child, 0, new_variants_move, not maximizingPlayer, alpha, beta, count_variants)
            if tmp >= 1000000:
                return (tmp, move, count_variants)

        for move in last_variants:
            child = board_condition.get_new_state(move, black)
            new_variants_move = P_generator_motion(move, board_condition.give_chips(), last_variants)

            count_variants += 1
            #print("#@%", count_variants)
            tmp, _, count_variants = sily_minimax(child, depth - 1, new_variants_move, not maximizingPlayer, alpha, beta, count_variants)

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
            new_variants_move = P_generator_motion(move, board_condition.give_chips(), last_variants)
            tmp, _, count_variants = sily_minimax(child, 0, new_variants_move, not maximizingPlayer, alpha, beta, count_variants)
            if tmp <= -1000000:
                return (tmp, move, count_variants)

        for move in last_variants:
            child = board_condition.get_new_state(move, white)
            new_variants_move = P_generator_motion(move, board_condition.give_chips(), last_variants)

            count_variants += 1
            #print("#@%", count_variants)
            tmp, _, count_variants = sily_minimax(child, depth - 1, new_variants_move, not maximizingPlayer, alpha, beta, count_variants)

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
                Visual_board.draw_all_game(-1)

                i +=1
                if i > len(positions):
                    sys.exit()

def now_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return event

        if event.type == pygame.MOUSEBUTTONDOWN:
            return event

def convert_positions(position):
    len_board = 14

    conv_pos = []

    for i in range(len_board+1):
        for j in range(len_board+1):
            if position[ i*len_board + j] != 0:
                conv_pos.append(( j, i, position[ i*len_board + j] ))

    return conv_pos



generation_position_and_save(100, 50)



show_positions()