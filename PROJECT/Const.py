# import sys
# from Graphics.Graphics_main import *
# from PROJECT.Brain_main import *
# import numpy as np
# from numba import typed
# import numba
# from numba import typed, types
#
# possible_moves_white_pl = typed.Dict.empty(
#         key_type=types.UniTuple(types.int64, 2),
#         value_type=numba.types.int64
#     )
# possible_moves_black_pl = typed.Dict.empty(
#     key_type=types.UniTuple(types.int64, 2),
#     value_type=numba.types.int64
# )
#
# color_user = black
# color_computer = white
# board = Board(color_user)
#
# board.set_coord(5, 5, color_user)
# possible_moves_white_pl, possible_moves_black_pl = new_generator_motion( (5, 5), board.give_chips(), create_independent_dict(possible_moves_white_pl), create_independent_dict(possible_moves_black_pl), black)
#
# board.set_coord(4, 4, color_computer)
# possible_moves_black_pl, possible_moves_white_pl = new_generator_motion((4,4), board.give_chips(),create_independent_dict(possible_moves_black_pl),create_independent_dict(possible_moves_white_pl), white)
#
# board.set_coord(6, 5, color_user)
# possible_moves_white_pl, possible_moves_black_pl = new_generator_motion( (6, 5), board.give_chips(), create_independent_dict(possible_moves_white_pl), create_independent_dict(possible_moves_black_pl), black)
#
# board.set_coord(3,3, color_computer)
# possible_moves_black_pl, possible_moves_white_pl = new_generator_motion((3,3), board.give_chips(),create_independent_dict(possible_moves_black_pl),create_independent_dict(possible_moves_white_pl), white)
#
# board.set_coord(7, 5, color_user)
# possible_moves_white_pl, possible_moves_black_pl = new_generator_motion( (7, 5), board.give_chips(), create_independent_dict(possible_moves_white_pl), create_independent_dict(possible_moves_black_pl), black)
#
# board.set_coord(4, 5, color_computer)
# possible_moves_black_pl, possible_moves_white_pl = new_generator_motion((4,5), board.give_chips(),create_independent_dict(possible_moves_black_pl),create_independent_dict(possible_moves_white_pl), white)
#
# board.set_coord(8, 5, color_user)
# possible_moves_white_pl, possible_moves_black_pl = new_generator_motion( (8, 5), board.give_chips(), create_independent_dict(possible_moves_white_pl), create_independent_dict(possible_moves_black_pl), black)
#
# board.set_coord(9, 5, color_computer)
# possible_moves_black_pl, possible_moves_white_pl = new_generator_motion((9,5), board.give_chips(),create_independent_dict(possible_moves_black_pl),create_independent_dict(possible_moves_white_pl), white)
#
# board.set_coord(7, 6, color_user)
# possible_moves_white_pl, possible_moves_black_pl = new_generator_motion( (7, 6), board.give_chips(), create_independent_dict(possible_moves_white_pl), create_independent_dict(possible_moves_black_pl), black)
#
# board.set_coord(4, 3, color_computer)
# possible_moves_black_pl, possible_moves_white_pl = new_generator_motion((4,3), board.give_chips(),create_independent_dict(possible_moves_black_pl),create_independent_dict(possible_moves_white_pl), white)
#
# board.set_coord(4, 6, color_user)
# possible_moves_white_pl, possible_moves_black_pl = new_generator_motion( (4, 6), board.give_chips(), create_independent_dict(possible_moves_white_pl), create_independent_dict(possible_moves_black_pl), black)
#
# board.set_coord(2, 2, color_computer)
# possible_moves_black_pl, possible_moves_white_pl = new_generator_motion((2,2), board.give_chips(),create_independent_dict(possible_moves_black_pl),create_independent_dict(possible_moves_white_pl), white)
#
# board.set_coord(4, 2, color_user)
# possible_moves_white_pl, possible_moves_black_pl = new_generator_motion( (4, 2), board.give_chips(), create_independent_dict(possible_moves_white_pl), create_independent_dict(possible_moves_black_pl), black)
#
# print("#@$@", possible_moves_white_pl.get((4,6)))
