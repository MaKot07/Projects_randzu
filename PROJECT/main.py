import sys
from Graphics.Graphics_main import *
from analitycs.analitycs_main import *
from Brain.Brain_main import *
from Const import *
import numpy as np



def now_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return event

        if event.type == pygame.MOUSEBUTTONDOWN:
            return event

def main():
    win_color = -1
    color_user = black
    color_computer = white
    number_of_movies = 0
    index_x_rect, index_y_rect = 7, 7
    last_sgen_motion = [np.empty((0), dtype=np.int8)]

    game_graphics = Game_Graphics(number_of_movies)
    game_graphics.draw_all_game(win_color)

    board_player = Board(color_user)

    run = True
    while run:

        event = now_event()

        if game_graphics.give_number_move() % 2 != 0 and win_color == -1:
            Board_MinMax = Board(color_computer, board_player.give_all_line_blackplayer(), board_player.give_all_line_whiteplayer(), board_player.give_chips())
            last_sgen_motion = generator_motion( np.array( [index_x_rect, index_y_rect], dtype=np.int8), last_sgen_motion, board_player.give_chips())
            next_variants_move_and_motion = ( np.array((index_x_rect, index_y_rect)), last_sgen_motion )

            best_value, coord_best_move, count_all_variants = minimax(Board_MinMax, 4, next_variants_move_and_motion, True, float('-inf'), float('inf'), 0)
            print("$@!$@!", best_value)

            game_graphics.set_coord(coord_best_move[0], coord_best_move[1], color_computer)
            board_player.set_coord(coord_best_move[0], coord_best_move[1], color_computer)

            last_sgen_motion = generator_motion(coord_best_move, last_sgen_motion, board_player.give_chips())

            game_graphics.set_number_move()

            board_player.adding_lines(coord_best_move[0], coord_best_move[1], color_computer)

            win_color = board_player.check_colors_win()



        else:
            if event != None:
                if event.type == pygame.QUIT:
                    run = False
                    sys.exit()

                if event.button == 1:
                    check_x, check_y = give_coord(event)

                    check_correct_motion = board_player.check_motion(check_x, check_y)
                    if check_correct_motion == True and win_color == -1:
                        index_x_rect, index_y_rect = give_coord_rect(event)
                        game_graphics.set_coord(index_x_rect, index_y_rect, color_user)
                        board_player.set_coord(index_x_rect, index_y_rect, color_user)

                        game_graphics.set_number_move()
                        board_player.adding_lines(index_x_rect, index_y_rect, color_user)

                        print("Black", board_player.give_all_line_blackplayer())
                        win_color = board_player.check_colors_win()

                    check_newgame = check_want_newgame(check_x, check_y)
                    if check_newgame == True:
                        del game_graphics
                        del board_player

                        win_color = -1
                        number_of_movies = 0

                        game_graphics = Game_Graphics( number_of_movies)

                        board_player = Board(color_user)

        game_graphics.draw_all_game(win_color)


if __name__ == "__main__":
    main()