from Const import *
from analitycs.analitycs_main import *
import random

coord_all_move_and_color = []

def generator_motion(for_color_player):
    sgen_motion = []
    random_chose = (-1,-1)
    for x_coord_enemy, y_cooord_enemy, color_enemy in coord_all_move_and_color:
        if for_color_player != color_enemy:
            start_x_coord = x_coord_enemy - 5
            end_x_coord = x_coord_enemy + 5

            start_y_coord = y_cooord_enemy - 5
            end_y_coord = y_cooord_enemy + 5

            for x_coord in range(start_x_coord, end_x_coord + 1):
                for y_coord in range(start_y_coord, end_y_coord + 1):
                    check_new_motion = check_motion_for_generator(x_coord, y_coord, coord_all_move_and_color)
                    if check_new_motion:
                        if (x_coord, y_coord) not in sgen_motion:
                            sgen_motion.append((x_coord, y_coord))

    if len(sgen_motion) != 0:
        random_chose = random.choice(sgen_motion)

    return random_chose

