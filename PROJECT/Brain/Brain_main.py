from Const import *
from analitycs.analitycs_main import *
import random

coord_all_move_and_color = []

def generator_motion(for_color_player):

    sgen_motion = []
    random_chose = (-1,-1)

    coord_left_border = 20
    coord_down_border = -1
    coord_right_border = -1
    coord_up_border = 20

    for x_coord_enemy, y_cooord_enemy, color_enemy in coord_all_move_and_color:
        if for_color_player != color_enemy:
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

    if len(sgen_motion) != 0:
        random_chose = random.choice(sgen_motion)

    return random_chose



def find_position_score(lines):
    pos_score = 0.0
    for line in lines:
        if len(line) == 1:
            pos_score += len(line)
        else:
            check_isolated = check_line_isolated(line)
            if check_isolated == 0:
                pos_score += len(line)
            else:
                if check_isolated == 1:
                    pos_score += len(line)/2

    return pos_score


def check_line_isolated(our_check_line):
    x_progressive = our_check_line[1][0] - our_check_line[0][0]
    y_progressive = our_check_line[1][1] - our_check_line[0][1]

    coord_new_max = (x_progressive + our_check_line[-1][0], y_progressive + our_check_line[-1][1])
    coord_new_min = (our_check_line[0][0] - x_progressive, our_check_line[0][1] - y_progressive)

    check_coord_new_max = check_motion_for_pose_score(coord_new_max[0], coord_new_max[1], coord_all_move_and_color)
    check_coord_new_min = check_motion_for_pose_score(coord_new_min[0], coord_new_min[1], coord_all_move_and_color)

    if check_coord_new_max == False and check_coord_new_min == False:
        return 2
    else:
        if check_coord_new_max == False or check_coord_new_min == False:
            return 1
        else:
            return 0
