import sys
import time

#from Graphics.Graphics_main import *
from Brain_main import *
import numpy as np
from numba import typed
import numba
from numba import typed, types

from deap import base, algorithms
from deap import creator
from deap import tools

import algelitism

import random
import matplotlib.pyplot as plt
import numpy as np


@njit(cache=True)
def minimax_for_genetic(board_condition, depth, last_variants_move_and_motion, maximizingPlayer, coeficent, alpha=float('-inf'), beta=float('inf'), count_variants=0):
    if board_condition.check_colors_win() != -1:
        return (board_condition.find_win_position_score(), (-1,-1), count_variants)
    if depth <= 0:
        bl_line = board_condition.now_all_line_blackplayer
        wh_line = board_condition.now_all_line_whiteplayer
        all_coord = board_condition.now_coord_all_move_and_color
        return (find_position_score(bl_line, wh_line, all_coord), (-1,-1), count_variants)
    if count_variants == max_count_variants:
        return (0, (-1, -1), count_variants)

    if maximizingPlayer:
        value = float('-inf')
        possible_moves_white_pl, possible_moves_black_pl = new_generator_motion_for_genetic(last_variants_move_and_motion[0], board_condition.now_coord_all_move_and_color, create_independent_dict(last_variants_move_and_motion[2]), create_independent_dict(last_variants_move_and_motion[1]), black, coeficent)

        for move, change_depth in possible_moves_white_pl.items():
            child = board_condition.get_new_state(move, black)

            count_variants += 1
            #print("#@%", count_variants)
            next_variants_move_and_motion = (move, create_independent_dict(possible_moves_black_pl), create_independent_dict(possible_moves_white_pl))
            tmp, _, count_variants = minimax_for_genetic(child, depth - 1 + change_depth, next_variants_move_and_motion, not maximizingPlayer, coeficent, alpha, beta, count_variants)

            if count_variants >= max_count_variants:
                break

            if tmp > value:
                value = tmp
                best_movement = move

            if value >= beta:
                break
            alpha = max(alpha, value)

    else:
        value = float('inf')
        possible_moves_black_pl, possible_moves_white_pl = new_generator_motion_for_genetic(last_variants_move_and_motion[0], board_condition.now_coord_all_move_and_color, create_independent_dict(last_variants_move_and_motion[1]), create_independent_dict(last_variants_move_and_motion[2]), white, coeficent)

        for move, change_depth in possible_moves_black_pl.items():
            child = board_condition.get_new_state(move, white)

            count_variants += 1
            #print("#@%", count_variants)
            next_variants_move_and_motion = (move, create_independent_dict(possible_moves_black_pl), create_independent_dict(possible_moves_white_pl))
            tmp, _, count_variants = minimax_for_genetic(child, depth - 1 + change_depth, next_variants_move_and_motion, not maximizingPlayer, coeficent, alpha, beta, count_variants)

            if count_variants >= max_count_variants:
                break

            if tmp < value:
                value = tmp
                best_movement = move

            if value <= alpha:
                break
            beta = min(beta, value)

    return value, best_movement, count_variants


@njit(cache=True)
def new_generator_motion_for_genetic(new_coord_motion, now_coord_all_move_and_color, dict_with_variants_for_player, dict_with_variants_for_enemy, color_enemy, coeficent):
    cell_qty = 14
    template_chip = np.array([-1, -1, -1], dtype=np.int8)
    if dict_with_variants_for_enemy.get(new_coord_motion) is not None:
        dict_with_variants_for_enemy.pop(new_coord_motion)
    if dict_with_variants_for_player.get(new_coord_motion) is not None:
        dict_with_variants_for_player.pop(new_coord_motion)

    #Анализ вертикальной линии и горизоньальной
    for a,b in [[0,1], [1,0]]:
        count_chip_enemy = 0
        list_with_sgen_chip_for_enemy = []
        for i in range(cell_qty+1):

            chip_enemy = template_chip.copy()
            chip_enemy[a] = new_coord_motion[a]
            chip_enemy[b] = i
            chip_enemy[2] = color_enemy
            if check_in_2D_array(chip_enemy, now_coord_all_move_and_color):
                count_chip_enemy += 1
                cop_b = chip_enemy[b]
                for j in (-1, 1):
                    chip_enemy[b] = cop_b + j
                    if check_motion_for_generator(chip_enemy, now_coord_all_move_and_color):
                        new_chip_list = [-1, -1]
                        new_chip_list[a], new_chip_list[b] = chip_enemy[a], chip_enemy[b]
                        new_chip = (new_chip_list[0], new_chip_list[1])
                        list_with_sgen_chip_for_enemy.append(new_chip)

        for chip in list_with_sgen_chip_for_enemy:
            if dict_with_variants_for_enemy.get(chip) is not None:
                if count_chip_enemy >= 2:
                    if dict_with_variants_for_enemy.get(chip) < 0:
                        dict_with_variants_for_enemy[chip] += coeficent[0]
                        dict_with_variants_for_player[chip] = dict_with_variants_for_enemy[chip]
            else:
                if count_chip_enemy == 1:
                    dict_with_variants_for_enemy[chip] = -coeficent[1]
                    dict_with_variants_for_player[chip] = -coeficent[1]
                if count_chip_enemy == 2:
                    dict_with_variants_for_enemy[chip] = -coeficent[2]
                if count_chip_enemy == 3:
                    dict_with_variants_for_enemy[chip] = -coeficent[3]
                    dict_with_variants_for_player[chip] = -coeficent[3]
                if count_chip_enemy > 3:
                    dict_with_variants_for_enemy[chip] = -coeficent[4]
                    dict_with_variants_for_player[chip] = -coeficent[4]

    #Анализ диагональных линий
    for flag in (0,1):
        count_chip_enemy = 0
        list_with_sgen_chip_for_enemy = []

        chip_enemy = template_chip.copy()

        chip_enemy[0], chip_enemy[1] = find_start_line(new_coord_motion[0], new_coord_motion[1], flag)
        chip_enemy[2] = color_enemy
        if flag == 0:
            for_j = [(-1, -1), (1, 1)]
            next_x = 1
            next_y = 1
        else:
            for_j = [(-1, 1), (1, -1)]
            next_x = -1
            next_y = 1

        while chip_enemy[0] <= cell_qty and chip_enemy[0] >= 0 and chip_enemy[1] <= cell_qty:
            cop_for_j1, cop_for_j2 = chip_enemy[0], chip_enemy[1]

            if check_in_2D_array(chip_enemy, now_coord_all_move_and_color):
                count_chip_enemy += 1
                for j1, j2 in for_j:
                    chip_enemy[0], chip_enemy[1] = cop_for_j1 + j1, cop_for_j2 + j2
                    if check_motion_for_generator(chip_enemy, now_coord_all_move_and_color):
                        new_chip = (chip_enemy[0], chip_enemy[1])
                        list_with_sgen_chip_for_enemy.append(new_chip)

            chip_enemy[0] = cop_for_j1 + next_x
            chip_enemy[1] = cop_for_j2 + next_y

        for chip in list_with_sgen_chip_for_enemy:
            if dict_with_variants_for_enemy.get(chip) is not None:
                if count_chip_enemy >= 2:
                    if dict_with_variants_for_enemy.get(chip) < 0:
                        dict_with_variants_for_enemy[chip] += coeficent[0]
                        dict_with_variants_for_player[chip] = dict_with_variants_for_enemy[chip]
            else:
                if count_chip_enemy == 1:
                    dict_with_variants_for_enemy[chip] = -coeficent[1]
                    dict_with_variants_for_player[chip] = -coeficent[1]
                if count_chip_enemy == 2:
                    dict_with_variants_for_enemy[chip] = -coeficent[2]
                if count_chip_enemy == 3:
                    dict_with_variants_for_enemy[chip] = -coeficent[3]
                    dict_with_variants_for_player[chip] = -coeficent[3]
                if count_chip_enemy > 3:
                    dict_with_variants_for_enemy[chip] = -coeficent[4]
                    dict_with_variants_for_player[chip] = -coeficent[4]

    return dict_with_variants_for_player, dict_with_variants_for_enemy




def Find_evulate(individual):
    win_color = -1
    color_computer = black
    color_individual = white
    number_of_movies = 0
    index_x_rect, index_y_rect = 7, 7
    move_color = black

    possible_moves_white_pl = typed.Dict.empty(
        key_type=types.UniTuple(types.int64, 2),
        value_type=numba.types.int64
    )
    possible_moves_black_pl = typed.Dict.empty(
        key_type=types.UniTuple(types.int64, 2),
        value_type=numba.types.int64
    )

    board = Board(color_computer)

    maximiz = False
    color_computer = black

    run = True
    while win_color == -1:
        Board_MinMax = Board(color_computer, board.give_all_line_blackplayer(),
                             board.give_all_line_whiteplayer(), board.give_chips())
        if possible_moves_black_pl.get((index_x_rect, index_y_rect)) is not None:
            possible_moves_black_pl.pop((index_x_rect, index_y_rect))
        if possible_moves_white_pl.get((index_x_rect, index_y_rect)) is not None:
            possible_moves_white_pl.pop((index_x_rect, index_y_rect))
        next_variants_move_and_motion = (
            (index_x_rect, index_y_rect), create_independent_dict(possible_moves_black_pl),
            create_independent_dict(possible_moves_white_pl))

        if number_of_movies == 0:
            coord_best_move = (6, 6)
            count_all_variants = 0
        else:
            if move_color == color_computer:
                best_value, coord_best_move, count_all_variants = minimax(Board_MinMax, 5,
                                                                          next_variants_move_and_motion, maximiz,
                                                                          float('-inf'), float('inf'), 0)
            else:
                best_value, coord_best_move, count_all_variants = minimax_for_genetic(Board_MinMax, individual[0],
                                                                          next_variants_move_and_motion, maximiz, individual[1:],
                                                                          float('-inf'), float('inf'), 0)
                if count_all_variants >= max_count_variants:
                    return 1000,

        index_x_rect, index_y_rect = coord_best_move


        board.set_coord(coord_best_move[0], coord_best_move[1], color_computer)

        if move_color == white:
            possible_moves_black_pl, possible_moves_white_pl = new_generator_motion_for_genetic(coord_best_move,
                                                                                    board.give_chips(),
                                                                                    create_independent_dict(
                                                                                        possible_moves_black_pl),
                                                                                    create_independent_dict(
                                                                                        possible_moves_white_pl),
                                                                                    white, individual[1:])
        else:
            possible_moves_white_pl, possible_moves_black_pl = new_generator_motion(coord_best_move,
                                                                                    board.give_chips(),
                                                                                    create_independent_dict(
                                                                                        possible_moves_white_pl),
                                                                                    create_independent_dict(
                                                                                        possible_moves_black_pl),
                                                                                    black)


        board.adding_lines(coord_best_move[0], coord_best_move[1], color_computer)

        win_color = board.check_colors_win()
        maximiz = not maximiz
        number_of_movies += 1
        if move_color == white:
            move_color = black
        else:
            move_color = white

    if win_color == 0:
        return number_of_movies*(abs(30-number_of_movies)),
    else:
        return number_of_movies,






max_count_variants = 5000
LOW, UP = 0, 10
ETA = 20
LENGTH_CHROM = 6

POPULATION_SIZE = 200   # количество индивидуумов в популяции
P_CROSSOVER = 0.9       # вероятность скрещивания
P_MUTATION = 0.2        # вероятность мутации индивидуума
MAX_GENERATIONS = 15    # максимальное количество поколений
HALL_OF_FAME_SIZE = 5

hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

def randomPoint(a, b):
    return [random.randint(a, b), random.randint(a, b), random.randint(a, b), random.randint(a, b), random.randint(a, b), random.randint(a, b)]

toolbox = base.Toolbox()
toolbox.register("randomPoint", randomPoint, LOW, UP)
toolbox.register("individualCreator", tools.initIterate, creator.Individual, toolbox.randomPoint)
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

population = toolbox.populationCreator(n=POPULATION_SIZE)


# def mutPolynomialBoundedInt(individual, eta, low, up, indpb):
#     size = len(individual)
#     for i in range(size):
#         if random.random() <= indpb:
#             x = individual[i]
#             if random.random() < 0.5:
#                 delta = (x - low) / (up - low)
#                 power = (2.0 * random.random() + (1.0 - 2.0 * random.random()) * (1.0 - delta)**(eta + 1.0))**(1.0 / (eta + 1.0))
#                 x = x - power * (x - low)
#             else:
#                 delta = (up - x) / (up - low)
#                 power = (2.0 * random.random() + (1.0 - 2.0 * random.random()) * (1.0 - delta)**(eta + 1.0))**(1.0 / (eta + 1.0))
#                 x = x + power * (up - x)
#             x = round(x)
#             x = min(max(x, low), up)
#             individual[i] = x
#     return individual,


toolbox.register("evaluate", Find_evulate)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", tools.cxUniform, indpb=1.0/LENGTH_CHROM)
toolbox.register("mutate", tools.mutUniformInt, low=LOW, up=UP, indpb=1.0/LENGTH_CHROM)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("min", np.min)
stats.register("avg", np.mean)

population, logbook = algelitism.eaSimpleElitism(population, toolbox,
                                        cxpb=P_CROSSOVER,
                                        mutpb=P_MUTATION,
                                        ngen=MAX_GENERATIONS,
                                        halloffame=hof,
                                        stats=stats,
                                        verbose=True)

maxFitnessValues, meanFitnessValues = logbook.select("min", "avg")

best = hof.items[0]
print(hof)
print(best)


