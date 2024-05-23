from Const import *
import pygame
from Graphics.Graphics_main import give_coord, give_coord_rect


def find_near_chips(x,y,color_player, coord_all_move_and_color):
    near_chips = []

    if (x+1, y+1, color_player) in coord_all_move_and_color:
        near_chips.append((x+1, y+1))
    if (x+1, y, color_player) in coord_all_move_and_color:
        near_chips.append((x+1, y))
    if (x+1, y-1, color_player) in coord_all_move_and_color:
        near_chips.append((x+1, y-1))
    if (x, y+1, color_player) in coord_all_move_and_color:
        near_chips.append((x, y+1))
    if (x-1, y-1, color_player) in coord_all_move_and_color:
        near_chips.append((x-1, y-1))
    if (x-1, y, color_player) in coord_all_move_and_color:
        near_chips.append((x-1, y))
    if (x-1, y+1, color_player) in coord_all_move_and_color:
        near_chips.append((x-1, y+1))
    if (x, y-1, color_player) in coord_all_move_and_color:
        near_chips.append((x, y-1))

    return near_chips


def check_line(coord_chip, our_line):
    x, y = coord_chip
    max_chip = our_line[-1]
    if coord_chip > max_chip:
        rate_x_progressive = our_line[1][0] - our_line[0][0]
        rate_y_progressive = our_line[1][1] - our_line[0][1]

        if our_line[-1][0] + rate_x_progressive == x and our_line[-1][1] + rate_y_progressive == y:
            fl = True
        else:
            fl = False
    else:
        rate_x_progressive = our_line[-1][0] - our_line[-2][0]
        rate_y_progressive = our_line[-1][1] - our_line[-2][1]

        if our_line[0][0] - rate_x_progressive == x and our_line[0][1] - rate_y_progressive == y:
            fl = True
        else:
            fl = False

    if fl == True:
        return True
    else:
        return False


def check_condition_win(all_line):
    fl = False
    for line in all_line:
        if len(line) == 5:
            fl = True
            break

    if fl == True:
        return True
    else:
        return False

def check_colors_win():
    check_win_white = check_condition_win(all_line_whiteplayer)
    check_win_black = check_condition_win(all_line_blackplayer)

    if check_win_black:
        return BLACK
    if check_win_white:
        return WHITE

    return None


def adding_lines(index_x_rect, index_y_rect, color_player, coord_all_move_and_color):
    if color_player == BLACK:
        bl_near_chips = find_near_chips(index_x_rect, index_y_rect, color_player, coord_all_move_and_color)
        for coord_chips in bl_near_chips:
            for line in all_line_blackplayer:
                if coord_chips in line:
                    if len(line) == 1:
                        if (index_x_rect, index_y_rect) > line[-1]:
                            all_line_blackplayer.append(line + [(index_x_rect, index_y_rect)])
                        else:
                            all_line_blackplayer.append([(index_x_rect, index_y_rect)] + line)
                    else:
                        in_condition = check_line((index_x_rect, index_y_rect), line)
                        if in_condition == True:
                            if (index_x_rect, index_y_rect) > line[-1]:
                                all_line_blackplayer.append(line + [(index_x_rect, index_y_rect)])
                            else:
                                all_line_blackplayer.append([(index_x_rect, index_y_rect)] + line)
    else:
        wh_near_chips = find_near_chips(index_x_rect, index_y_rect, color_player, coord_all_move_and_color)
        for coord_chips in wh_near_chips:
            for line in all_line_whiteplayer:
                if coord_chips in line:
                    if len(line) == 1:
                        if (index_x_rect, index_y_rect) > line[-1]:
                            all_line_whiteplayer.append(line + [(index_x_rect, index_y_rect)])
                        else:
                            all_line_whiteplayer.append([(index_x_rect, index_y_rect)] + line)

                    else:
                        in_condition = check_line((index_x_rect, index_y_rect), line)
                        if in_condition == True:
                            if (index_x_rect, index_y_rect) > line[-1]:
                                all_line_whiteplayer.append(line + [(index_x_rect, index_y_rect)])

                            else:
                                all_line_whiteplayer.append([(index_x_rect, index_y_rect)] + line)

    if color_player == WHITE:
        all_line_whiteplayer.append([(index_x_rect, index_y_rect)])

    else:
        all_line_blackplayer.append([(index_x_rect, index_y_rect)])


def now_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return event

        if event.type == pygame.MOUSEBUTTONDOWN:
            return event





def check_motion(x, y, coord_all_move_and_color ):
    fl = False
    x_rect = round(x / cell_size_ramka)
    y_rect = round(y / cell_size_ramka)

    if x <= (cell_qty * cell_size_ramka) and x >= 0 and y <= (cell_qty * cell_size_ramka) and y >= 0:
        if (x_rect, y_rect, WHITE) not in coord_all_move_and_color and (x_rect, y_rect, BLACK) not in coord_all_move_and_color:
            fl = True

    if fl == True:
        return True
    else:
        return False


def check_motion_for_generator(x, y, coord_all_move_and_color):
    fl = False

    if x <= 14 and x >= 0 and y <= 14 and y >= 0:
        if (x, y, WHITE) not in coord_all_move_and_color and (x, y, BLACK) not in coord_all_move_and_color:
            fl = True

    if fl == True:
        return True
    else:
        return False


#variables
all_line_whiteplayer = []
all_line_blackplayer = []
check_win_black = False
check_win_white = False

