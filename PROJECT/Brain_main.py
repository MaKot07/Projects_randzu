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
        self.black = np.int8(0)
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

        if check_draw_njit(cell_qty, self.now_coord_all_move_and_color):
            return None

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

        return -1

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



@njit(cache=True)
def minimax(board_condition, depth, last_variants_move_and_motion, maximizingPlayer, alpha=float('-inf'), beta=float('inf'), count_variants=0):

    if board_condition.check_colors_win() != -1:
        return (board_condition.find_win_position_score(), (-1,-1), count_variants)
    if depth <= 0:
        bl_line = board_condition.now_all_line_blackplayer
        wh_line = board_condition.now_all_line_whiteplayer
        all_coord = board_condition.now_coord_all_move_and_color
        return (find_position_score(bl_line, wh_line, all_coord), (-1,-1), count_variants)

    if maximizingPlayer:
        value = float('-inf')
        possible_moves_white_pl, possible_moves_black_pl = new_generator_motion(last_variants_move_and_motion[0], board_condition.now_coord_all_move_and_color, create_independent_dict(last_variants_move_and_motion[2]), create_independent_dict(last_variants_move_and_motion[1]), black)

        for move, change_depth in possible_moves_white_pl.items():
            child = board_condition.get_new_state(move, black)

            count_variants += 1
            print("#@%", count_variants)
            next_variants_move_and_motion = (move, create_independent_dict(possible_moves_black_pl), create_independent_dict(possible_moves_white_pl))
            tmp, _, count_variants = minimax(child, depth - 1 + change_depth, next_variants_move_and_motion, not maximizingPlayer, alpha, beta, count_variants)

            if tmp > value:
                value = tmp
                best_movement = move

            if value >= beta:
                break
            alpha = max(alpha, value)

    else:
        value = float('inf')
        possible_moves_black_pl, possible_moves_white_pl = new_generator_motion(last_variants_move_and_motion[0], board_condition.now_coord_all_move_and_color, create_independent_dict(last_variants_move_and_motion[1]), create_independent_dict(last_variants_move_and_motion[2]), white)

        for move, change_depth in possible_moves_black_pl.items():
            child = board_condition.get_new_state(move, white)

            count_variants += 1
            print("#@%", count_variants)
            next_variants_move_and_motion = (move, create_independent_dict(possible_moves_black_pl), create_independent_dict(possible_moves_white_pl))
            tmp, _, count_variants = minimax(child, depth - 1 + change_depth, next_variants_move_and_motion, not maximizingPlayer, alpha, beta, count_variants)

            if tmp < value:
                value = tmp
                best_movement = move

            if value <= alpha:
                break
            beta = min(beta, value)

    return value, best_movement, count_variants



@njit(cache=True)
def new_generator_motion(new_coord_motion, now_coord_all_move_and_color, dict_with_variants_for_player, dict_with_variants_for_enemy, color_enemy):
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
                        dict_with_variants_for_enemy[chip] += 1
                        dict_with_variants_for_player[chip] = dict_with_variants_for_enemy[chip]
            else:
                if count_chip_enemy == 1:
                    dict_with_variants_for_enemy[chip] = -3
                    dict_with_variants_for_player[chip] = -3
                if count_chip_enemy == 2:
                    dict_with_variants_for_enemy[chip] = -2
                if count_chip_enemy == 3:
                    dict_with_variants_for_enemy[chip] = -1
                    dict_with_variants_for_player[chip] = -1
                if count_chip_enemy > 3:
                    dict_with_variants_for_enemy[chip] = 0
                    dict_with_variants_for_player[chip] = 0

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
                        dict_with_variants_for_enemy[chip] += 1
                        dict_with_variants_for_player[chip] = dict_with_variants_for_enemy[chip]
            else:
                if count_chip_enemy == 1:
                    dict_with_variants_for_enemy[chip] = -3
                    dict_with_variants_for_player[chip] = -3
                if count_chip_enemy == 2:
                    dict_with_variants_for_enemy[chip] = -2
                if count_chip_enemy == 3:
                    dict_with_variants_for_enemy[chip] = -1
                    dict_with_variants_for_player[chip] = -1
                if count_chip_enemy > 3:
                    dict_with_variants_for_enemy[chip] = 0
                    dict_with_variants_for_player[chip] = 0

    return dict_with_variants_for_player, dict_with_variants_for_enemy

@njit(cache=True)
def find_start_line(x, y, flag):
    cell_qty = 14
    if flag == 0:
        x1, y1 = x, y
        cell_qty = 14
        while x1 != 0 and y1 != 0:
            x1 -= 1
            y1 -= 1
        return x1, y1
    else:
        x2, y2 = x, y
        while x2 != cell_qty and y2 != 0:
            x2 += 1
            y2 -= 1
        return x2, y2




@njit(cache=True)
def generator_motion(new_coord_motion, last_variants_motion, now_coord_all_move_and_color):
    sgen_motion = []

    for x_coord in range(new_coord_motion[0] - 1, new_coord_motion[0] + 2):
        for y_coord in range(new_coord_motion[1] - 1, new_coord_motion[1] + 2):
            check_new_motion = check_motion_for_brain(x_coord, y_coord, now_coord_all_move_and_color)
            if check_new_motion and check_not_in_2D_list(np.array([x_coord, y_coord], dtype=np.int8), last_variants_motion):
                new_chip = np.array([x_coord, y_coord], dtype=np.int8)
                sgen_motion.append(new_chip)

    if last_variants_motion[0].size == 0:
        return sgen_motion

    if check_in_2D_list(new_coord_motion, last_variants_motion):
        last_variants_motion = remove_element_from_list(last_variants_motion, new_coord_motion)

    sgen_motion.extend(last_variants_motion)
    return sgen_motion


@njit(cache=True)
def check_line_isolated(our_check_line, now_coord_all_move_and_color):

    x_progressive = our_check_line[1][0] - our_check_line[0][0]
    y_progressive = our_check_line[1][1] - our_check_line[0][1]

    coord_new_max = (x_progressive + our_check_line[-1][0], y_progressive + our_check_line[-1][1])
    coord_new_min = (our_check_line[0][0] - x_progressive, our_check_line[0][1] - y_progressive)

    check_coord_new_max = check_motion_for_brain(coord_new_max[0], coord_new_max[1], now_coord_all_move_and_color)
    check_coord_new_min = check_motion_for_brain(coord_new_min[0], coord_new_min[1], now_coord_all_move_and_color)

    if check_coord_new_max == False and check_coord_new_min == False:
        return 2
    else:
        if check_coord_new_max == False or check_coord_new_min == False:
            return 1
        else:
            return 0

@njit(cache=True)
def find_position_score(now_all_line_blackplayer, now_all_line_whiteplayer, now_coord_all_move_and_color):
    pos_score = 0
    for line in now_all_line_whiteplayer:
        check_isolated = check_line_isolated(line, now_coord_all_move_and_color)
        if check_isolated == 0:
            if give_len_line(line) == 4:
                pos_score += 17500
            if give_len_line(line) == 3:
                pos_score += 3000
            if give_len_line(line) == 2:
                pos_score += 140
            if give_len_line(line) == 1:
                pos_score += 5

        if check_isolated == 1:
            if give_len_line(line) == 4:
                pos_score += 9500
            if give_len_line(line) == 3:
                pos_score += 560
            if give_len_line(line) == 2:
                pos_score += 60
            if give_len_line(line) == 1:
                pos_score += 10

    for line in now_all_line_blackplayer:
        check_isolated = check_line_isolated(line, now_coord_all_move_and_color)
        if check_isolated == 0:
            if give_len_line(line) == 4:
                pos_score -= 17500
            if give_len_line(line) == 3:
                pos_score -= 3000
            if give_len_line(line) == 2:
                pos_score -= 140
            if give_len_line(line) == 1:
                pos_score -= 5

        if check_isolated == 1:
            if give_len_line(line) == 4:
                pos_score -= 9500
            if give_len_line(line) == 3:
                pos_score -= 560
            if give_len_line(line) == 2:
                pos_score -= 60
            if give_len_line(line) == 1:
                pos_score -= 10
    return pos_score


@njit(cache=True)
def dynamic_score_positions(all_line):
    dynamic_score = 0
    for line in all_line:
        dynamic_score += give_len_line(line)**2

    return dynamic_score



