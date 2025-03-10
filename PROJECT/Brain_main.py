from analitycs_main import *
import numpy as np
from numba import njit, int8
from numba.experimental import jitclass

spec = [
    ('now_coord_all_move_and_color', int8[:, :]),
    ('now_all_line_blackplayer', int8[:, :, :]),
    ('now_all_line_whiteplayer', int8[:, :, :]),
    ('color', int8),
    ('new_move', int8[:]),
    ('need_color', int8),
    ('cell_qty', int8),
    ('black', int8),
    ('white', int8),
]

@jitclass(spec)
class Board:

    def __init__(self, color, now_all_line_blackplayer=np.empty((0,9,2), dtype=np.int8), now_all_line_whiteplayer=np.empty((0,9,2), dtype=np.int8), now_coord_all_move_and_color=np.empty((0,3), dtype=np.int8)):
        self.now_coord_all_move_and_color = np.copy(now_coord_all_move_and_color)
        self.now_all_line_blackplayer = np.copy(now_all_line_blackplayer)
        self.now_all_line_whiteplayer = np.copy(now_all_line_whiteplayer)
        self.color = color
        self.cell_qty = 14
        self.black = np.int8(-1)
        self.white = np.int8(1)


    def set_coord(self, x, y, color):
        new_arr = np.array([[x,y, color]], dtype=np.int8)
        if self.now_coord_all_move_and_color.size == 0:
            self.now_coord_all_move_and_color = new_arr
        else:
            self.now_coord_all_move_and_color = np.vstack((self.now_coord_all_move_and_color, new_arr))

    def give_all_line_blackplayer(self):
        return np.copy(self.now_all_line_blackplayer)

    def give_all_line_whiteplayer(self):
        return np.copy(self.now_all_line_whiteplayer)

    def give_color(self):
        return self.color

    def give_chips(self):
        return np.copy(self.now_coord_all_move_and_color)

    def adding_lines(self, index_x_rect, index_y_rect, color_player):
        if color_player == black:
            self.now_all_line_blackplayer = adding_lines(index_x_rect, index_y_rect, color_player, self.now_all_line_blackplayer, self.now_coord_all_move_and_color)
        else:
            self.now_all_line_whiteplayer = adding_lines(index_x_rect, index_y_rect, color_player, self.now_all_line_whiteplayer, self.now_coord_all_move_and_color)


    def check_motion(self, x, y):
        x_rect = np.round(x / cell_size_ramka)
        y_rect = np.round(y / cell_size_ramka)

        if x <= (cell_qty * cell_size_ramka) and x >= 0 and y <= (cell_qty * cell_size_ramka) and y >= 0:
            if not check_in_2D_array(np.array([x_rect, y_rect, white], dtype=np.int8), self.now_coord_all_move_and_color) and not check_in_2D_array(np.array([x_rect, y_rect, black], dtype=np.int8), self.now_coord_all_move_and_color):
                return True
        return False


    def check_condition_win(self, need_color):
        if need_color == black:
            all_line = self.now_all_line_blackplayer
        else:
            all_line = self.now_all_line_whiteplayer

        # if check_draw_njit(cell_qty, self.now_coord_all_move_and_color):
        #     return None

        if all_line.size == 0:
            return False

        return check_win_njit(all_line)

    def check_colors_win(self):
        check_win_white = self.check_condition_win(white)
        check_win_black = self.check_condition_win(black)

        if check_win_white:
            return white
        if check_win_black:
            return black

        return 0

    def find_win_position_score(self):
        pos_score = 0
        if self.check_colors_win() == white:
            pos_score += 1000000
        else:
            pos_score -= 1000000
        return pos_score



    def get_new_state(self, new_move, color_new_player):
        new_move_array = np.array([[new_move[0], new_move[1], self.color]], dtype=np.int8)

        new_coord_all_move_and_color = np.vstack((self.now_coord_all_move_and_color, new_move_array))

        if self.color == black:
            new_all_line_blackplayer = adding_lines(new_move[0], new_move[1], self.color, self.now_all_line_blackplayer, self.now_coord_all_move_and_color)
            new_all_line_whiteplayer = np.copy(self.now_all_line_whiteplayer)
        else:
            new_all_line_whiteplayer = adding_lines(new_move[0], new_move[1], self.color, self.now_all_line_whiteplayer, self.now_coord_all_move_and_color)
            new_all_line_blackplayer = np.copy(self.now_all_line_blackplayer)

        createn_new_state = Board(color_new_player, new_all_line_blackplayer, new_all_line_whiteplayer, new_coord_all_move_and_color)

        return createn_new_state



@njit
def minimax(board_condition, depth, last_variants_move_and_motion, maximizingPlayer, alpha=float('-inf'), beta=float('inf'), count_variants=0):

    if board_condition.check_colors_win() != 0:
        return (board_condition.find_win_position_score(), (-1,-1), count_variants)
    if depth <= 0:
        all_lines_black = board_condition.give_all_line_blackplayer()
        all_lines_white = board_condition.give_all_line_whiteplayer()
        chips = board_condition.give_chips()

        return (find_position_score(all_lines_black, all_lines_white, chips), (-1, -1), count_variants)

    if maximizingPlayer:
        value = float('-inf')
        new_possible_moves = new_generator_motion_for_minmax(last_variants_move_and_motion[0], board_condition.give_chips(), create_independent_dict(last_variants_move_and_motion[1]), board_condition.now_all_line_blackplayer)

        for move, change_depth in new_possible_moves.items():
            if change_depth >= 0.5:
                child = board_condition.get_new_state(move, black)
                tmp, _, count_variants = minimax(child, 0, last_variants_move_and_motion, not maximizingPlayer, alpha, beta, count_variants)
                if tmp >= 1000000:
                    return (tmp, move, count_variants)

        for move, change_depth in new_possible_moves.items():

            child = board_condition.get_new_state(move, black)

            count_variants += 1
            ##print("#@%", count_variants)
            next_variants_move_and_motion = (move, create_independent_dict(new_possible_moves))
            tmp, _, count_variants = minimax(child, depth*change_depth-1, next_variants_move_and_motion, not maximizingPlayer, alpha, beta, count_variants)

            if tmp > value:
                value = tmp
                best_movement = move

            if value > beta:
                break
            alpha = max(alpha, value)

    else:
        value = float('inf')
        new_possible_moves = new_generator_motion_for_minmax(last_variants_move_and_motion[0], board_condition.give_chips(), create_independent_dict(last_variants_move_and_motion[1]), board_condition.now_all_line_whiteplayer)

        for move, change_depth in new_possible_moves.items():
            if change_depth >= 0.5:
                child = board_condition.get_new_state(move, white)
                tmp, _, count_variants = minimax(child, 0, last_variants_move_and_motion, not maximizingPlayer, alpha, beta, count_variants)
                if tmp <= -1000000:
                    return (tmp, move, count_variants)

        for move, change_depth in new_possible_moves.items():
            child = board_condition.get_new_state(move, white)

            count_variants += 1
            ##print("#@%", count_variants)
            next_variants_move_and_motion = (move, create_independent_dict(new_possible_moves))
            tmp, _, count_variants = minimax(child, depth*change_depth-1, next_variants_move_and_motion, not maximizingPlayer, alpha, beta, count_variants)


            if tmp < value:
                value = tmp
                best_movement = move

            if value < alpha:
                break
            beta = min(beta, value)

    return value, best_movement, count_variants


@njit()
def new_generator_motion_for_minmax(new_coord_motion, now_coord_all_move_and_color, dict_with_variants, lines):
    if new_coord_motion == (-1, -1):
        dict_with_variants[(7,7)] = 0.001
        return dict_with_variants

    coefficent = [0.2, 0.5, 0.6, 0.7]

    empty = np.array([-1, -1], dtype=np.int8)

    dict_with_variants.pop(new_coord_motion, None)

    new_coord_motion = np.array(new_coord_motion)
    for line in lines:
        if not check_in_2D_array(new_coord_motion, line):
            continue


        if np.array_equal(line[1], empty):
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    chip = (new_coord_motion[0] + i, new_coord_motion[1] + j)

                    if chip not in dict_with_variants and check_motion_for_brain(chip[0], chip[1], now_coord_all_move_and_color):
                        dict_with_variants[chip] = coefficent[0]

            continue

        line_length = give_len_line(line)
        x_progressive = line[1][0] - line[0][0]
        y_progressive = line[1][1] - line[0][1]

        coord_new_max = (
        x_progressive + line[line_length-1][0], y_progressive + line[line_length-1][1])
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






# @njit
# def generator_motion_for_minmax(new_coord_motion, now_coord_all_move_and_color, dict_with_variants_for_player, dict_with_variants_for_enemy, color_enemy):
#     if new_coord_motion == (-1, -1):
#         return dict_with_variants_for_player, dict_with_variants_for_enemy
#
#     cell_qty = 14
#     coefficent = [0.1, 0.3, 0.1, 0.6]
#     template_chip = np.array([-1, -1, -1], dtype=np.int8)
#
#     dict_with_variants_for_enemy.pop(new_coord_motion, None)
#     dict_with_variants_for_player.pop(new_coord_motion, None)
#
#     # Анализ вертикальной и горизонтальной линий
#     for a, b in [[0, 1], [1, 0]]:
#         count_chip_enemy = 0
#         list_with_sgen_chip_for_enemy = []
#
#         for i in range(cell_qty + 1):
#             chip_enemy = template_chip.copy()
#             chip_enemy[a] = new_coord_motion[a]
#             chip_enemy[b] = i
#             chip_enemy[2] = color_enemy
#
#
#             if check_in_2D_array(chip_enemy, now_coord_all_move_and_color):
#                 count_chip_enemy += 1
#                 cop_b = chip_enemy[b]
#
#                 for j in (-1, 1):
#                     chip_enemy[b] = cop_b + j
#                     if check_motion_for_generator(chip_enemy, now_coord_all_move_and_color):
#                         new_chip_list = [-1, -1]
#                         new_chip_list[a], new_chip_list[b] = chip_enemy[a], chip_enemy[b]
#                         new_chip = (new_chip_list[0], new_chip_list[1])
#                         list_with_sgen_chip_for_enemy.append(new_chip)
#
#         for chip in list_with_sgen_chip_for_enemy:
#
#
#             if count_chip_enemy == 1:
#                 dict_with_variants_for_enemy[chip] = coefficent[0]
#                 dict_with_variants_for_player[chip] = coefficent[0]
#             elif count_chip_enemy == 2:
#                 dict_with_variants_for_enemy[chip] = coefficent[1]
#             elif count_chip_enemy >= 3:
#                 dict_with_variants_for_enemy[chip] = coefficent[3]
#                 dict_with_variants_for_player[chip] = coefficent[3]
#
#     # Анализ диагональных линий
#     for flag in (0, 1):
#         count_chip_enemy = 0
#         list_with_sgen_chip_for_enemy = []
#         chip_enemy = template_chip.copy()
#
#         chip_enemy[0], chip_enemy[1] = find_start_line(new_coord_motion[0], new_coord_motion[1], flag)
#         chip_enemy[2] = color_enemy
#
#         for_j = [(-1, -1), (1, 1)] if flag == 0 else [(-1, 1), (1, -1)]
#         next_x, next_y = (1, 1) if flag == 0 else (-1, 1)
#
#         while 0 <= chip_enemy[0] <= cell_qty and 0 <= chip_enemy[1] <= cell_qty:
#             cop_for_j1, cop_for_j2 = chip_enemy[0], chip_enemy[1]
#
#             if check_in_2D_array(chip_enemy, now_coord_all_move_and_color):
#                 count_chip_enemy += 1
#                 for j1, j2 in for_j:
#                     chip_enemy[0], chip_enemy[1] = cop_for_j1 + j1, cop_for_j2 + j2
#                     if check_motion_for_brain(chip_enemy, now_coord_all_move_and_color):
#                         new_chip = (chip_enemy[0], chip_enemy[1])
#                         list_with_sgen_chip_for_enemy.append(new_chip)
#
#             chip_enemy[0] = cop_for_j1 + next_x
#             chip_enemy[1] = cop_for_j2 + next_y
#
#         for chip in list_with_sgen_chip_for_enemy:
#
#             if count_chip_enemy == 1:
#                 dict_with_variants_for_enemy[chip] = coefficent[0]
#                 dict_with_variants_for_player[chip] = coefficent[0]
#             elif count_chip_enemy == 2:
#                 dict_with_variants_for_enemy[chip] = coefficent[1]
#             elif count_chip_enemy >= 3:
#                 dict_with_variants_for_enemy[chip] = coefficent[3]
#                 dict_with_variants_for_player[chip] = coefficent[3]
#
#     return dict_with_variants_for_player, dict_with_variants_for_enemy
#
#
# @njit
# def find_start_line(x, y, flag):
#     cell_qty = 14
#     if flag == 0:
#         x1, y1 = x, y
#         while x1 != 0 and y1 != 0:
#             x1 -= 1
#             y1 -= 1
#         return x1, y1
#     else:
#         x2, y2 = x, y
#         while x2 != cell_qty and y2 != 0:
#             x2 += 1
#             y2 -= 1
#         return x2, y2




def P_generator_motion(new_coord_motion, now_coord_all_move_and_color, last_variants_motion=[]):
    sgen_motion = []

    for x_coord in range(new_coord_motion[0] - 1, new_coord_motion[0] + 2):
        for y_coord in range(new_coord_motion[1] - 1, new_coord_motion[1] + 2):
            check_new_motion = check_motion_for_brain(x_coord, y_coord, now_coord_all_move_and_color)
            if check_new_motion and (x_coord, y_coord) not in last_variants_motion:
                new_chip = (x_coord, y_coord)
                sgen_motion.append(new_chip)

    if not last_variants_motion:
        return sgen_motion

    if new_coord_motion in last_variants_motion:
        last_variants_motion.pop(last_variants_motion.index(new_coord_motion))

    return sgen_motion + last_variants_motion

def silly_P_generator_motion(now_coord_all_move_and_color):
    sgen_motion = []

    for coord in now_coord_all_move_and_color:
        for x_coord in [coord[0] - 1, coord[0] + 2]:
            for y_coord in [coord[1] - 1, coord[1] + 2]:
                check_new_motion = check_motion_for_brain(x_coord, y_coord, now_coord_all_move_and_color)
                if check_new_motion and (x_coord, y_coord) not in sgen_motion:
                    new_chip = (x_coord, y_coord)
                    sgen_motion.append(new_chip)

    return sgen_motion


@njit
def check_line_isolated(our_check_line, now_coord_all_move_and_color):
    empty = np.array([-1, -1], dtype=np.int8)
    if np.array_equal(our_check_line[1], empty):
        return 0

    x_progressive = our_check_line[1][0] - our_check_line[0][0]
    y_progressive = our_check_line[1][1] - our_check_line[0][1]

    last_element = give_len_line(our_check_line) - 1
    coord_new_max = (x_progressive + our_check_line[last_element][0], y_progressive + our_check_line[last_element][1])
    coord_new_min = (our_check_line[0][0] - x_progressive, our_check_line[0][1] - y_progressive)

    check_coord_new_max = int(check_motion_for_brain(coord_new_max[0], coord_new_max[1], now_coord_all_move_and_color))
    check_coord_new_min = int(check_motion_for_brain(coord_new_min[0], coord_new_min[1], now_coord_all_move_and_color))

    return check_coord_new_min + check_coord_new_max

@njit
def find_position_score(now_all_line_blackplayer, now_all_line_whiteplayer, now_coord_all_move_and_color):

    score_rules = {
        2: {4:100000, 3:10000, 2:1000, 1:10},
        1: {4:5000, 3:500, 2:50}
    }

    pos_score_white = 0
    pos_score_black = 0

    for i in prange(len(now_all_line_whiteplayer)):
        line = now_all_line_whiteplayer[i]
        check_isolated = check_line_isolated(line, now_coord_all_move_and_color)
        if check_isolated in score_rules:
            pos_score_white += score_rules[check_isolated][give_len_line(line)]

    for i in prange(len(now_all_line_blackplayer)):
        line = now_all_line_blackplayer[i]
        check_isolated = check_line_isolated(line, now_coord_all_move_and_color)
        if check_isolated in score_rules:
            pos_score_black += score_rules[check_isolated][give_len_line(line)]

    return pos_score_white - pos_score_black


@njit
def dynamic_score_positions(all_line):
    dynamic_score = 0
    for line in all_line:
        dynamic_score += give_len_line(line)**2

    return dynamic_score



