import numpy as np
from Brain_main import *

def generation_position_and_save(n, number_move):
    if n%number_move != 0:
        raise SystemExit("n не делится на number_move")

    black = 0
    white = 1
    cell_qty = 14
    color_move = black
    percent_random = 0.1
    percent_depth1 = 0.5

    all_generation_positions = np.zeros((255, n), dtype=np.int8)

    for sample in range(int(n/number_move)):
        sgen_board = Board()

        coord_move = (np.random.randint(0, 11), np.random.randint(0, 11))
        sgen_board.set_coord(coord_move[0], coord_move[1], black)

        variants_move = P_generator_motion(coord_move, sgen_board.give_chips())
        coord_move = variants_move[np.random.randint(0, len(variants_move))]
        sgen_board.set_coord(coord_move[0], coord_move[1], white)

        for i in range(number_move-2):
            level_choice = np.random.random()

            if level_choice <= percent_random:
                variants_move = P_generator_motion(coord_move, sgen_board.give_chips())
                coord_move = variants_move[np.random.randint(0, len(variants_move))]






generation_position_and_save(100, 50)