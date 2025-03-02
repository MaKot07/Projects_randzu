from Graphics.Graphics_main import *
from Brain_main import *
import numba
from numba import typed, types


def now_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return event

        if event.type == pygame.MOUSEBUTTONDOWN:
            return event

def main():
    win_color = 0
    color_user = color_choice()
    number_of_movies = 0
    index_x_rect, index_y_rect = -1, -1

    possible_moves = typed.Dict.empty(
        key_type=types.UniTuple(types.int64, 2),
        value_type=numba.types.float64
    )

    passive_buttons = [
        Button("who_move", 110, 20, 220, 70, ""),
    ]
    dynamic_buttons = [
        Button("newgame", 375, 20, 220, 70, "New game"),
    ]

    #for_otladka = [[], [], [], [], []]

    if color_user == black:
        color_computer = white
        comp_move = False
    else:
        color_computer = black
        comp_move = True

    for button in passive_buttons:
        if button.name == "who_move":
            button.text = "Your move" if not comp_move else "Enemy move"

    game_graphics = Game_Graphics(number_of_movies)
    game_graphics.draw_all_game(win_color, dynamic_buttons + passive_buttons)

    main_board = Board(color_user)

    while True:
        event = now_event()

        if comp_move and win_color == 0:
            Board_MinMax = Board(color_computer, main_board.give_all_line_blackplayer(), main_board.give_all_line_whiteplayer(), main_board.give_chips())

            possible_moves.pop((index_x_rect, index_y_rect), None)

            next_variants_move_and_motion = ( (index_x_rect, index_y_rect),create_independent_dict(possible_moves))

            # for_otladka[3].append(convert_to_regular_dict(possible_moves_black_pl))
            # for_otladka[4].append(convert_to_regular_dict(possible_moves_white_pl))

            maxim = True if color_computer == white else False
            best_value, coord_best_move, count_all_variants = minimax(Board_MinMax, 15, next_variants_move_and_motion, maxim, float('-inf'), float('inf'), 0)

            if color_computer == white:
                possible_moves = new_generator_motion_for_minmax(
                    next_variants_move_and_motion[0], main_board.give_chips(),
                    create_independent_dict(next_variants_move_and_motion[1]), main_board.give_all_line_blackplayer())
            else:
                possible_moves = new_generator_motion_for_minmax(
                    next_variants_move_and_motion[0], main_board.give_chips(),
                    create_independent_dict(next_variants_move_and_motion[1]),
                    main_board.give_all_line_whiteplayer())

            #print("3#@#", count_all_variants,best_value, find_position_score(main_board.give_all_line_blackplayer(), main_board.give_all_line_whiteplayer(), main_board.give_chips()))

            game_graphics.set_coord(coord_best_move[0], coord_best_move[1], color_computer)
            main_board.set_coord(coord_best_move[0], coord_best_move[1], color_computer)

            game_graphics.set_number_move()

            main_board.adding_lines(coord_best_move[0], coord_best_move[1], color_computer)

            if color_computer == white:
                possible_moves = new_generator_motion_for_minmax(coord_best_move,
                                                                               main_board.give_chips(),
                                                                               create_independent_dict(
                                                                                   possible_moves),
                                                                               main_board.give_all_line_whiteplayer())
            else:
                possible_moves = new_generator_motion_for_minmax(coord_best_move,
                                                                               main_board.give_chips(),
                                                                               create_independent_dict(
                                                                                   possible_moves),
                                                                               main_board.give_all_line_blackplayer())

            # for_otladka[0].append(main_board.give_all_line_blackplayer())
            # for_otladka[1].append(main_board.give_all_line_whiteplayer())
            # for_otladka[2].append(main_board.give_chips())

            win_color = main_board.check_colors_win()
            comp_move = not comp_move

        else:
            if event != None:
                if event.type == pygame.QUIT:
                    #return for_otladka
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

                        ##print("Black", main_board.give_all_line_blackplayer())
                        win_color = main_board.check_colors_win()
                        comp_move = not comp_move

                        # for_otladka[0].append(main_board.give_all_line_blackplayer())
                        # for_otladka[1].append(main_board.give_all_line_whiteplayer())
                        # for_otladka[2].append(main_board.give_chips())


        #Обработка статичных кнопок
        for button in passive_buttons:
            if button.name == "who_move":
                button.text = "Your move" if not comp_move else "Enemy move"


        #Обработка динамических кнопок
        if event != None:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in dynamic_buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.name == "newgame":
                            win_color = 0
                            number_of_movies = 0
                            index_x_rect, index_y_rect = -1, -1
                            possible_moves = typed.Dict.empty(
                                key_type=types.UniTuple(types.int64, 2),
                                value_type=numba.types.float64
                            )
                            game_graphics = Game_Graphics(number_of_movies)
                            game_graphics.draw_all_game(win_color, dynamic_buttons+passive_buttons)

                            color_user = color_choice()
                            main_board = Board(color_user)

                            if color_user == black:
                                color_computer = white
                                comp_move = False
                            else:
                                color_computer = black
                                comp_move = True
                            for button in passive_buttons:
                                if button.name == "who_move":
                                    button.text = "Your move" if not comp_move else "Enemy move"

        mouse_pos = pygame.mouse.get_pos()

        for button in dynamic_buttons:
            button.check_hover(mouse_pos)

        game_graphics.draw_all_game(win_color, dynamic_buttons+passive_buttons)






if __name__ == "__main__":
    main()

