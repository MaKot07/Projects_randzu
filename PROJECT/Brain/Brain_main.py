from Const import *
from analitycs.analitycs_main import *
import random
import copy

coord_all_move_and_color = []

def generator_motion(color_for_gen):

    sgen_motion = []

    coord_left_border = 100
    coord_down_border = -1
    coord_right_border = -1
    coord_up_border = 100
    for (x_coord_enemy, y_cooord_enemy), color_enemy in coord_all_move_and_color:
        if color_for_gen != color_enemy:
            if x_coord_enemy < coord_left_border:
                coord_left_border = x_coord_enemy
            if x_coord_enemy > coord_right_border:
                coord_right_border = x_coord_enemy
            if y_cooord_enemy > coord_down_border:
                coord_down_border = y_cooord_enemy
            if y_cooord_enemy < coord_up_border:
                coord_up_border = y_cooord_enemy

    for x_coord in range(coord_left_border-2, coord_right_border + 3):
        for y_coord in range(coord_up_border-2, coord_down_border + 3):
            check_new_motion = check_motion_for_generator(x_coord, y_coord, coord_all_move_and_color)
            if check_new_motion:
                if (x_coord, y_coord) not in sgen_motion:
                    sgen_motion.append((x_coord, y_coord))

    return sgen_motion



def find_position_score(lines, now_coord_all_move_and_color):
    pos_score = 0
    for line in lines[1]:
        if len(line) >= 5:
            pos_score += 5000
        else:
            check_isolated = check_line_isolated(line, now_coord_all_move_and_color, WHITE)
            if check_isolated == 0:
                if len(line) == 4:
                    pos_score += 250
                if len(line) == 3:
                    pos_score += 70
                if len(line) == 2:
                    pos_score += 40
                if len(line) == 1:
                    pos_score += 10

            if check_isolated == 1:
                if len(line) == 4:
                    pos_score += 100
                if len(line) == 3:
                    pos_score += 40
                if len(line) == 2:
                    pos_score += 20
                if len(line) == 1:
                    pos_score += 5

    for line in lines[0]:
        if len(line) >= 5:
            pos_score -= 5000
        else:
            check_isolated = check_line_isolated(line, now_coord_all_move_and_color, BLACK)
            if check_isolated == 0:
                if len(line) == 4:
                    pos_score -= 250
                if len(line) == 3:
                    pos_score -= 70
                if len(line) == 2:
                    pos_score -= 40
                if len(line) == 1:
                    pos_score -= 10

            if check_isolated == 1:
                if len(line) == 4:
                    pos_score -= 100
                if len(line) == 3:
                    pos_score -= 40
                if len(line) == 2:
                    pos_score -= 20
                if len(line) == 1:
                    pos_score -= 5
    return pos_score


def check_line_isolated(our_check_line, now_coord_all_move_and_color, all_color_line):
    if len(our_check_line) == 1:
        if all_color_line == BLACK:
            near_chips = find_near_chips(our_check_line[0][0], our_check_line[0][1], WHITE, now_coord_all_move_and_color)
            for new_coord_x, new_coord_y in near_chips:
                check_coord_new = check_motion_for_pose_score(new_coord_x, new_coord_y, now_coord_all_move_and_color)
                if check_coord_new == True:
                    return 1
            return 0
        else:
            near_chips = find_near_chips(our_check_line[0][0], our_check_line[0][1], BLACK, now_coord_all_move_and_color)
            for new_coord_x, new_coord_y in near_chips:
                check_coord_new = check_motion_for_pose_score(new_coord_x, new_coord_y, now_coord_all_move_and_color)
                if check_coord_new == True:
                    return 1
            return 0

    x_progressive = our_check_line[1][0] - our_check_line[0][0]
    y_progressive = our_check_line[1][1] - our_check_line[0][1]

    coord_new_max = (x_progressive + our_check_line[-1][0], y_progressive + our_check_line[-1][1])
    coord_new_min = (our_check_line[0][0] - x_progressive, our_check_line[0][1] - y_progressive)

    check_coord_new_max = check_motion_for_pose_score(coord_new_max[0], coord_new_max[1], now_coord_all_move_and_color)
    check_coord_new_min = check_motion_for_pose_score(coord_new_min[0], coord_new_min[1], now_coord_all_move_and_color)

    if check_coord_new_max == False and check_coord_new_min == False:
        return 2
    else:
        if check_coord_new_max == False or check_coord_new_min == False:
            return 1
        else:
            return 0


def get_new_state(new_move, color_new_move, new_all_line, last_coord_all_move_and_color):
    new_coord_all_move_and_color = copy.copy(last_coord_all_move_and_color)
    new_coord_all_move_and_color.append((new_move, color_new_move))

    if color_new_move == WHITE:
        adding_lines(new_move[0], new_move[1], new_all_line[1], color_new_move, new_coord_all_move_and_color)
    else:
        adding_lines(new_move[0], new_move[1], new_all_line[0], color_new_move, new_coord_all_move_and_color)

    return ((new_all_line[0], new_all_line[1]), new_coord_all_move_and_color)


def minimax(game_state, depth, maximizingPlayer, alpha=float('-inf'), beta=float('inf')):
    best_movement = (0,0)
    if depth == 0 or check_condition_win(game_state[0][0], game_state[1]) == True or check_condition_win(game_state[0][0], game_state[1]) == None:
        return (find_position_score((game_state[0][0], game_state[0][1]), game_state[1]), None)

    if depth == 0 or check_condition_win(game_state[0][1], game_state[1]) == True or check_condition_win(game_state[0][1], game_state[1]) == None:
        return (find_position_score((game_state[0][0], game_state[0][1]), game_state[1]), None)

    if maximizingPlayer:
        value = float('-inf')
        possible_moves = generator_motion(WHITE)

        for move in possible_moves:
            child = get_new_state(move, WHITE, (game_state[0][0], game_state[0][1]), game_state[1])

            tmp, _ = minimax(child, depth - 1, False, alpha, beta)
            if tmp > value:
                value = tmp
                best_movement = move

            if value > beta:
                break
            alpha = max(alpha, value)

    else:
        value = float('inf')
        possible_moves = generator_motion(BLACK)

        for move in possible_moves:
            child = get_new_state(move, BLACK, (game_state[0][0], game_state[0][1]), game_state[1])

            tmp, _ = minimax(child, depth - 1, True, alpha, beta)
            if tmp < value:
                value = tmp
                best_movement = move

            if value < alpha:
                break
            beta = min(beta, value)

    return (value, best_movement)























