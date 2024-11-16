import sys
from Graphics.Graphics_main import *
from PROJECT.Brain_main import *
from neural_network import *
import numpy as np
from numba import typed
import numba
from numba import typed, types
import pickle

def now_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return event

        if event.type == pygame.MOUSEBUTTONDOWN:
            return event

def main():
    win_color = 0
    color_user = black
    color_computer = white
    number_of_movies = 0
    index_x_rect, index_y_rect = 7, 7
    len_board = 15
    play_neural_network = False
    if play_neural_network:
        model = tf.keras.models.load_model(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\best_prediction_model.keras', custom_objects={'CustomLossLayer': CustomLossLayer, 'custom_activation': custom_activation})

    possible_moves_white_pl = typed.Dict.empty(
        key_type=types.UniTuple(types.int8, 2),
        value_type=numba.types.float32
    )
    possible_moves_black_pl = typed.Dict.empty(
        key_type=types.UniTuple(types.int8, 2),
        value_type=numba.types.float32
    )

    game_graphics = Game_Graphics(number_of_movies)
    game_graphics.draw_all_game(win_color)

    main_board = Board(color_user)

    if color_computer == white:
        comp_move = False
    else:
        comp_move = True

    while True:
        event = now_event()

        if comp_move and win_color == 0:
            if play_neural_network:
                if game_graphics.give_number_move() > 3:

                    position = np.zeros((1,225), dtype=np.int8)
                    for i in range(len(main_board.give_chips())):
                        position[0][main_board.give_chips()[i][1] * len_board + main_board.give_chips()[i][0]] = main_board.give_chips()[i][2]
                    if np.sum(position[0]) == 0:
                        for j in range(len(position[0])):
                            position[0][j] = 1 if position[0][j] == -1 else 0.5
                    else:
                        for j in range(len(position[0])):
                            position[0][j] = 1 if position[0][j] == 1 else 0.5

                    #для старой модели
                    # not_convert_coord = model.predict(position)[0]
                    # label = np.where(not_convert_coord == max(not_convert_coord))[0][0]
                    # coord_best_move = (label-(label//15)*15, label//15)

                    not_round_coord_best_move = model.predict(position)[0]
                    coord_best_move = (round(not_round_coord_best_move[0]), round(not_round_coord_best_move[1]))
                    print(coord_best_move, not_round_coord_best_move)

                    game_graphics.set_coord(coord_best_move[0], coord_best_move[1], color_computer)
                    main_board.set_coord(coord_best_move[0], coord_best_move[1], color_computer)

                    game_graphics.set_number_move()

                    main_board.adding_lines(coord_best_move[0], coord_best_move[1], color_computer)

                    win_color = main_board.check_colors_win()
                    comp_move = not comp_move
                else:
                    maximizing = True if color_computer == white else False
                    variants_move = silly_P_generator_motion(main_board.give_chips())

                    Board_SillyMinMax = Board(color_computer, main_board.give_all_line_blackplayer(),
                                              main_board.give_all_line_whiteplayer(), main_board.give_chips())

                    _, coord_best_move, c = sily_minimax(Board_SillyMinMax, 1, variants_move, maximizing)

                    game_graphics.set_coord(coord_best_move[0], coord_best_move[1], color_computer)
                    main_board.set_coord(coord_best_move[0], coord_best_move[1], color_computer)

                    game_graphics.set_number_move()

                    main_board.adding_lines(coord_best_move[0], coord_best_move[1], color_computer)

                    win_color = main_board.check_colors_win()
                    comp_move = not comp_move

            else:
                Board_MinMax = Board(color_computer, main_board.give_all_line_blackplayer(), main_board.give_all_line_whiteplayer(), main_board.give_chips())
                if possible_moves_black_pl.get((index_x_rect, index_y_rect)) is not None:
                    possible_moves_black_pl.pop((index_x_rect, index_y_rect))
                if possible_moves_white_pl.get((index_x_rect, index_y_rect)) is not None:
                    possible_moves_white_pl.pop((index_x_rect, index_y_rect))
                next_variants_move_and_motion = ( (index_x_rect, index_y_rect),create_independent_dict(possible_moves_black_pl), create_independent_dict(possible_moves_white_pl))

                maxim = True if color_computer == white else False
                best_value, coord_best_move, count_all_variants = minimax(Board_MinMax, 25, next_variants_move_and_motion, maxim, float('-inf'), float('inf'), 0)

                print("3#@#", count_all_variants, find_position_score(main_board.give_all_line_blackplayer(), main_board.give_all_line_whiteplayer(), main_board.give_chips()))

                game_graphics.set_coord(coord_best_move[0], coord_best_move[1], color_computer)
                main_board.set_coord(coord_best_move[0], coord_best_move[1], color_computer)

                possible_moves_black_pl, possible_moves_white_pl = new_generator_motion(coord_best_move, main_board.give_chips(), create_independent_dict(possible_moves_black_pl), create_independent_dict(possible_moves_white_pl), white)

                game_graphics.set_number_move()

                main_board.adding_lines(coord_best_move[0], coord_best_move[1], color_computer)

                # for_otladka[0].append(main_board.give_all_line_blackplayer())
                # for_otladka[1].append(main_board.give_all_line_whiteplayer())
                # for_otladka[2].append(main_board.give_chips())

                win_color = main_board.check_colors_win()
                comp_move = not comp_move

        else:
            if event != None:
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.button == 1:
                    check_x, check_y = give_coord(event)

                    check_correct_motion = main_board.check_motion(check_x, check_y)
                    if check_correct_motion == True and win_color == 0:
                        index_x_rect, index_y_rect = give_coord_rect(event)
                        game_graphics.set_coord(index_x_rect, index_y_rect, color_user)
                        main_board.set_coord(index_x_rect, index_y_rect, color_user)

                        game_graphics.set_number_move()
                        main_board.adding_lines(index_x_rect, index_y_rect, color_user)

                        #print("Black", main_board.give_all_line_blackplayer())
                        win_color = main_board.check_colors_win()
                        comp_move = not comp_move

                        # for_otladka[0].append(main_board.give_all_line_blackplayer())
                        # for_otladka[1].append(main_board.give_all_line_whiteplayer())
                        # for_otladka[2].append(main_board.give_chips())

                    check_newgame = check_want_newgame(check_x, check_y)
                    if check_newgame == True:
                        del game_graphics
                        del main_board

                        win_color = 0
                        number_of_movies = 0

                        game_graphics = Game_Graphics( number_of_movies)

                        main_board = Board(color_user)

        game_graphics.draw_all_game(win_color)


# if __name__ == "__main__":
#     main()


def otladka():
    # with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\OTLADKA\otladka.csv', 'ab') as file:
    #     pickle.dump(main(), file)
    # sys.exit()


    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\OTLADKA\otladka.csv', 'rb') as file:
        a = []
        while True:
            try:
                a.append(pickle.load(file))
            except EOFError:
                break

    print(a[0])


otladka()