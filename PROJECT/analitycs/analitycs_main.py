from Const import *
import pygame
#from Graphics.Graphics_main import *
import copy


#variables
all_line_whiteplayer = []
all_line_blackplayer = []
check_win_black = False
check_win_white = False


class Analitycs:

    __check_win_black = False
    __check_win_white = False
    __cell_qty = 14

    def __init__(self, now_coord_all_move_and_color, color):
        self.color = copy.copy(color)
        self.now_coord_all_move_and_color = copy.copy(now_coord_all_move_and_color)
        self.now_all_line_blackplayer = []
        self.now_all_line_whiteplayer = []

    def set_coord(self, x, y, color):
        self.now_coord_all_move_and_color.append(((x,y), color))

    def give_all_line_blackplayer(self):
        return self.now_all_line_blackplayer
    def give_all_line_whiteplayer(self):
        return self.now_all_line_whiteplayer

    def give_color(self):
        return self.color

    def give_chips(self):
        return self.now_coord_all_move_and_color

    def find_near_chips(self, x, y, need_color):
        near_chips = []

        if ((x + 1, y + 1), need_color) in self.now_coord_all_move_and_color:
            near_chips.append((x + 1, y + 1))
        if ((x + 1, y), need_color) in self.now_coord_all_move_and_color:
            near_chips.append((x + 1, y))
        if ((x + 1, y - 1), need_color) in self.now_coord_all_move_and_color:
            near_chips.append((x + 1, y - 1))
        if ((x, y + 1), need_color) in self.now_coord_all_move_and_color:
            near_chips.append((x, y + 1))
        if ((x - 1, y - 1), need_color) in self.now_coord_all_move_and_color:
            near_chips.append((x - 1, y - 1))
        if ((x - 1, y), need_color) in self.now_coord_all_move_and_color:
            near_chips.append((x - 1, y))
        if ((x - 1, y + 1), need_color) in self.now_coord_all_move_and_color:
            near_chips.append((x - 1, y + 1))
        if ((x, y - 1), need_color) in self.now_coord_all_move_and_color:
            near_chips.append((x, y - 1))

        return near_chips

    def check_line(self, coord_chip, our_line):
        x, y = coord_chip
        max_chip = our_line[-1]
        if len(our_line) == 1:
            fl = True
        else:
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

    def check_condition_win(self, need_color):
        if need_color == BLACK:
            all_line = self.now_all_line_blackplayer
        else:
            all_line = self.now_all_line_whiteplayer
        fl = False
        check_draw = True
        for x in range(14 + 1):
            for y in range(14 + 1):
                if (x, y, WHITE) not in self.now_coord_all_move_and_color or (x, y, BLACK) not in self.now_coord_all_move_and_color:
                    check_draw = False
        if check_draw == True:
            return None
        for line in all_line:
            if len(line) >= 5:
                fl = True
                break

        if fl == True:
            return True
        else:
            return False

    def check_colors_win(self):
        check_win_white = self.check_condition_win(WHITE)
        check_win_black = self.check_condition_win(BLACK)

        if check_win_white:
            return WHITE
        if check_win_black:
            return BLACK

        return None

    def check_connect_lines(self, coord_chip, line, color_chip, all_line):
        add = (False, 0)
        if coord_chip > line[-1]:
            new_coord_x_chip = coord_chip[0] + (coord_chip[0] - line[-1][0])
            new_coord_y_chip = coord_chip[1] + (coord_chip[1] - line[-1][1])
            next_coord_chip = (new_coord_x_chip, new_coord_y_chip)

        else:
            new_coord_x_chip = coord_chip[0] - (line[0][0] - coord_chip[0])
            new_coord_y_chip = coord_chip[1] - (line[0][1] - coord_chip[1])
            next_coord_chip = (new_coord_x_chip, new_coord_y_chip)

        if color_chip == BLACK:
            for lines in all_line:
                if next_coord_chip in lines and lines != line:
                    if len(lines) != 1:
                        check_next_line = self.check_line(coord_chip, lines)
                        if check_next_line == True:
                            return (True, all_line.index(lines))
                    else:
                        add = (True, all_line.index(lines))
        else:
            for lines in all_line:
                if next_coord_chip in lines and lines != line:
                    if len(lines) != 1:
                        check_next_line = self.check_line(coord_chip, lines)
                        if check_next_line == True:
                            return (True, all_line.index(lines))
                    else:
                        add = (True, all_line.index(lines))

        return add

    def dellit_near_chips(self, coords_chip, check_in_line, list_whith_lines, delit_color):
        all_near_chips = self.find_near_chips(coords_chip[0], coords_chip[1], delit_color)

        for near_chips in all_near_chips:
            if near_chips in check_in_line and [near_chips] in list_whith_lines:
                del list_whith_lines[list_whith_lines.index([near_chips])]
        return list_whith_lines

    def find_need_line(self, coords_chip, color,  need_line):
        list_without_len_1 = []
        list_with_len_1 = []

        if color == BLACK:
            bl_near_chips = self.find_near_chips(coords_chip[0], coords_chip[1], color)

            for near_coords_chip in bl_near_chips:
                for lines in need_line:
                    if near_coords_chip in lines:
                        in_condition = self.check_line(coords_chip, lines)
                        if in_condition == True:
                            if len(lines) != 1:
                                list_without_len_1.append(lines)
                            else:
                                list_with_len_1.append(lines)
        else:
            wh_near_chips = self.find_near_chips(coords_chip[0], coords_chip[1], color)
            for near_coords_chip in wh_near_chips:
                for lines in need_line:
                    if near_coords_chip in lines:
                        in_condition = self.check_line(coords_chip, lines)
                        if in_condition == True:
                            if len(lines) != 1:
                                list_without_len_1.append(lines)
                            else:
                                list_with_len_1.append(lines)

        return list_without_len_1 + list_with_len_1

    def adding_lines(self, index_x_rect, index_y_rect, color_player):
        if color_player == BLACK:
            all_line = self.now_all_line_blackplayer
            list_whith_lines = self.find_need_line((index_x_rect, index_y_rect), color_player, all_line)
            for line in list_whith_lines:
                if (index_x_rect, index_y_rect) > line[-1]:
                    check_connect_another_line, index_connect_line = self.check_connect_lines((index_x_rect, index_y_rect), line, color_player, all_line)
                    if check_connect_another_line == True:
                        self.now_all_line_blackplayer.append(line + [(index_x_rect, index_y_rect)] + all_line[index_connect_line])
                        new_line = line + [(index_x_rect, index_y_rect)] + all_line[index_connect_line]

                        list_whith_lines = self.dellit_near_chips((index_x_rect, index_y_rect), new_line, list_whith_lines, color_player)
                        if len(all_line[index_connect_line]) != 1:
                            if all_line[index_connect_line] in list_whith_lines:
                                del list_whith_lines[list_whith_lines.index(all_line[index_connect_line])]
                            del self.now_all_line_blackplayer[index_connect_line]
                        if len(line) != 1:
                            del self.now_all_line_blackplayer[all_line.index(line)]
                    else:
                        self.now_all_line_blackplayer.append(line + [(index_x_rect, index_y_rect)])
                        new_line = line + [(index_x_rect, index_y_rect)]

                        if len(line) != 1:
                            del self.now_all_line_blackplayer[all_line.index(line)]
                            list_whith_lines = self.dellit_near_chips((index_x_rect, index_y_rect), new_line,list_whith_lines, color_player)
                else:
                    check_connect_another_line, index_connect_line = self.check_connect_lines((index_x_rect, index_y_rect),line, color_player, all_line)
                    if check_connect_another_line == True:
                        self.now_all_line_blackplayer.append(all_line[index_connect_line] + [(index_x_rect, index_y_rect)] + line)
                        new_line = all_line[index_connect_line] + [(index_x_rect, index_y_rect)] + line

                        list_whith_lines = self.dellit_near_chips((index_x_rect, index_y_rect), new_line, list_whith_lines, color_player)
                        if len(all_line[index_connect_line]) != 1:
                            if all_line[index_connect_line] in list_whith_lines:
                                del list_whith_lines[list_whith_lines.index(all_line[index_connect_line])]
                            del self.now_all_line_blackplayer[index_connect_line]
                        if len(line) != 1:
                            del self.now_all_line_blackplayer[all_line.index(line)]
                    else:
                        self.now_all_line_blackplayer.append([(index_x_rect, index_y_rect)] + line)
                        new_line = [(index_x_rect, index_y_rect)] + line

                        if len(line) != 1:
                            del self.now_all_line_blackplayer[all_line.index(line)]
                            list_whith_lines = self.dellit_near_chips((index_x_rect, index_y_rect), new_line,list_whith_lines, color_player)
        else:
            all_line = self.now_all_line_whiteplayer
            list_whith_lines = self.find_need_line((index_x_rect, index_y_rect), color_player,  all_line)
            for line in list_whith_lines:
                if (index_x_rect, index_y_rect) > line[-1]:
                    check_connect_another_line, index_connect_line = self.check_connect_lines((index_x_rect, index_y_rect),line, color_player, all_line)
                    if check_connect_another_line == True:
                        self.now_all_line_whiteplayer.append(line + [(index_x_rect, index_y_rect)] + all_line[index_connect_line])
                        new_line = line + [(index_x_rect, index_y_rect)] + all_line[index_connect_line]

                        list_whith_lines = self.dellit_near_chips((index_x_rect, index_y_rect), new_line, list_whith_lines, color_player)
                        if len(all_line[index_connect_line]) != 1:
                            if all_line[index_connect_line] in list_whith_lines:
                                del list_whith_lines[list_whith_lines.index(all_line[index_connect_line])]
                            del self.now_all_line_whiteplayer[index_connect_line]
                        if len(line) != 1:
                            del self.now_all_line_whiteplayer[all_line.index(line)]
                    else:
                        self.now_all_line_whiteplayer.append(line + [(index_x_rect, index_y_rect)])
                        new_line = line + [(index_x_rect, index_y_rect)]

                        if len(line) != 1:
                            del self.now_all_line_whiteplayer[all_line.index(line)]
                            list_whith_lines = self.dellit_near_chips((index_x_rect, index_y_rect), new_line,list_whith_lines, color_player)
                else:
                    check_connect_another_line, index_connect_line = self.check_connect_lines((index_x_rect, index_y_rect),line, color_player, all_line)
                    if check_connect_another_line == True:
                        self.now_all_line_whiteplayer.append(all_line[index_connect_line] + [(index_x_rect, index_y_rect)] + line)
                        new_line = all_line[index_connect_line] + [(index_x_rect, index_y_rect)] + line

                        list_whith_lines = self.dellit_near_chips((index_x_rect, index_y_rect), new_line, list_whith_lines, color_player)
                        if len(all_line[index_connect_line]) != 1:
                            if all_line[index_connect_line] in list_whith_lines:
                                del list_whith_lines[list_whith_lines.index(all_line[index_connect_line])]
                            del self.now_all_line_whiteplayer[index_connect_line]
                        if len(line) != 1:
                            del self.now_all_line_whiteplayer[all_line.index(line)]
                    else:
                        self.now_all_line_whiteplayer.append([(index_x_rect, index_y_rect)] + line)
                        new_line = [(index_x_rect, index_y_rect)] + line

                        if len(line) != 1:
                            del self.now_all_line_whiteplayer[all_line.index(line)]
                            list_whith_lines = self.dellit_near_chips((index_x_rect, index_y_rect), new_line,list_whith_lines, color_player)

        if color_player == WHITE:
            self.now_all_line_whiteplayer.append([(index_x_rect, index_y_rect)])
        else:
            self.now_all_line_blackplayer.append([(index_x_rect, index_y_rect)])

    def now_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return event

            if event.type == pygame.MOUSEBUTTONDOWN:
                return event

    def check_motion(self, x, y):
        fl = False
        x_rect = round(x / cell_size_ramka)
        y_rect = round(y / cell_size_ramka)

        if x <= (cell_qty * cell_size_ramka) and x >= 0 and y <= (cell_qty * cell_size_ramka) and y >= 0:
            if ((x_rect, y_rect), WHITE) not in self.now_coord_all_move_and_color and (
            (x_rect, y_rect), BLACK) not in self.now_coord_all_move_and_color:
                fl = True

        if fl == True:
            return True
        else:
            return False

    def check_motion_for_generator(self, x, y):
        fl = False

        if x <= cell_qty and x >= 0 and y <= cell_qty and y >= 0:
            if ((x, y), WHITE) not in self.now_coord_all_move_and_color and (
            (x, y), BLACK) not in self.now_coord_all_move_and_color:
                fl = True

        if fl == True:
            return True
        else:
            return False

    def check_motion_for_pose_score(self, x_rect, y_rect):
        fl = False

        if x_rect <= cell_qty and x_rect >= 0 and y_rect <= cell_qty and y_rect >= 0:
            if ((x_rect, y_rect), WHITE) not in self.now_coord_all_move_and_color and (
            (x_rect, y_rect), BLACK) not in self.now_coord_all_move_and_color:
                fl = True

        if fl == True:
            return True
        else:
            return False

    def check_want_newgame(self, x_pixel, y_pixel):
        if x_pixel >= 700 and x_pixel <= 840 and y_pixel >= 180 and y_pixel < 250:
            return True
        return False





def check_motion_for_generator(x, y, now_coord_all_move_and_color):
    fl = False

    if x <= cell_qty and x >= 0 and y <= cell_qty and y >= 0:
        if ((x, y), WHITE) not in now_coord_all_move_and_color and ((x, y), BLACK) not in now_coord_all_move_and_color:
            fl = True

    if fl == True:
        return True
    else:
        return False



def check_motion_for_pose_score(x_rect, y_rect, now_coord_all_move_and_color):
    fl = False

    if x_rect <= cell_qty and x_rect >= 0 and y_rect <= cell_qty and y_rect >= 0:
        if ((x_rect, y_rect), WHITE) not in now_coord_all_move_and_color and ((x_rect, y_rect), BLACK) not in now_coord_all_move_and_color:
            fl = True

    if fl == True:
        return True
    else:
        return False


def check_want_newgame(x_pixel, y_pixel):
    if x_pixel >= 700 and x_pixel <= 840 and y_pixel >= 180 and y_pixel < 250:
        return True
    return False


