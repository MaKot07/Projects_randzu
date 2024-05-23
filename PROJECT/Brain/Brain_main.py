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
    pos_score = 0
    for line in lines:
        pos_score += len(line)

    return pos_score
