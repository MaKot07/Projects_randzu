from Const import *
import pygame
import numpy as np
import copy
from numba import jit


class Analitycs:

    cell_qty = 14

    def __init__(self, now_coord_all_move_and_color, color):
        self.color = copy.copy(color)
        self.now_coord_all_move_and_color = np.array(copy.copy(now_coord_all_move_and_color))
        self.now_all_line_blackplayer = np.array([])
        self.now_all_line_whiteplayer = np.array([])

    def set_coord(self, x, y, color):
        new_arr = np.array([[x,y, color]])
        if len(self.now_coord_all_move_and_color) == 0:
            self.now_coord_all_move_and_color = new_arr
        else:
            self.now_coord_all_move_and_color = np.vstack((self.now_coord_all_move_and_color, new_arr))

    def give_all_line_blackplayer(self):
        return self.now_all_line_blackplayer

    def give_all_line_whiteplayer(self):
        return self.now_all_line_whiteplayer

    def give_color(self):
        return self.color

    def give_chips(self):
        return self.now_coord_all_move_and_color

    @jit(nopython=True)
    def find_near_chips(self, x, y, need_color):
        near_chips = np.array([])

        for i in range(-1, 2):
            for j in range(-1,2):
                new_x = x + i
                new_y = y + j
                if check_in_2D_array(np.array([new_x, new_y, need_color]), self.now_coord_all_move_and_color) and (i != 0 or j != 0):
                    if len(near_chips) == 0:
                        near_chips = np.array([[new_x, new_y]])
                    else:
                        near_chips = np.vstack((near_chips, np.array([[new_x, new_y]])))

        return near_chips

    @jit(nopython=True)
    def check_line(self, coord_chip, our_line):
        x, y = coord_chip
        min_chip = our_line[0]
        if our_line[1][0] == -1:
            return True
        else:
            if not (coord_chip[0] < min_chip[0] or (coord_chip[0] == min_chip[0] and coord_chip[1] < min_chip[1])):
                rate_x_progressive = our_line[1][0] - our_line[0][0]
                rate_y_progressive = our_line[1][1] - our_line[0][1]

                for i in range(len(our_line)):
                    if np.array_equal(our_line[i+1], np.array([-1,-1])):
                        if our_line[i][0] + rate_x_progressive == x and our_line[i][1] + rate_y_progressive == y:
                            return True
                        else:
                            return False
            else:
                rate_x_progressive = our_line[1][0] - our_line[0][0]
                rate_y_progressive = our_line[1][1] - our_line[0][1]

                if our_line[0][0] - rate_x_progressive == x and our_line[0][1] - rate_y_progressive == y:
                    return True
                else:
                    return False

    @jit(nopython=True)
    def check_condition_win(self, need_color):
        if need_color == black:
            all_line = self.now_all_line_blackplayer
        else:
            all_line = self.now_all_line_whiteplayer
        check_draw = True
        for x in range(cell_qty + 1):
            for y in range(cell_qty + 1):
                new_arr_wh = np.array([[x, y, white]])
                new_arr_bl = np.array([[x, y, black]])
                if not check_in_2D_array(new_arr_wh, self.now_coord_all_move_and_color) or not check_in_2D_array(new_arr_bl, self.now_coord_all_move_and_color):
                    check_draw = False
        if check_draw == True:
            return None
        for line in all_line:
            if give_len_line(line) >= 5:
                return  True

        return False

    @jit(nopython=True)
    def check_colors_win(self):
        check_win_white = self.check_condition_win(white)
        check_win_black = self.check_condition_win(black)

        if check_win_white:
            return white
        if check_win_black:
            return black

        return None

    @jit(nopython=True)
    def check_connect_lines(self, coord_chip, line, all_line):
        add = (False, 0)
        if not (coord_chip[0] < line[0][0] or (coord_chip[0] == line[0][0] and coord_chip[1] < line[0][1])):
            new_coord_x_chip = coord_chip[0] + (coord_chip[0] - line[-1][0])
            new_coord_y_chip = coord_chip[1] + (coord_chip[1] - line[-1][1])
            next_coord_chip = np.array([new_coord_x_chip, new_coord_y_chip])
        else:
            new_coord_x_chip = coord_chip[0] - (line[0][0] - coord_chip[0])
            new_coord_y_chip = coord_chip[1] - (line[0][1] - coord_chip[1])
            next_coord_chip = np.array([new_coord_x_chip, new_coord_y_chip])

        for lines in all_line:
            if check_in_2D_array(next_coord_chip, lines):
                if give_len_line(lines) != 1:
                    check_next_line = self.check_line(coord_chip, lines)
                    if check_next_line == True:
                        for index in range(len(all_line)):
                            if np.array_equal(all_line[index], lines):
                                return (True, index)
                else:
                    for index in range(len(all_line)):
                        if np.array_equal(all_line[index], lines):
                            add = (True, index)

        return add

    @jit(nopython=True)
    def dellit_near_chips(self, coords_chip, check_in_line, list_whith_lines, delit_color, all_delit_index):
        all_near_chips = self.find_near_chips(coords_chip[0], coords_chip[1], delit_color)
        new_list_whith_lines = np.array([])
        index_to_del = np.array([])

        for near_chips in all_near_chips:
            near_chips_with_empty = np.concatenate([np.array([near_chips]), np.full((14, 2), -1)])
            if check_in_2D_array(near_chips, check_in_line) and check_in_2D_array( near_chips_with_empty, list_whith_lines):
                for i in range(len(list_whith_lines)):
                    if np.array_equal(list_whith_lines[i], near_chips_with_empty):
                        if len(index_to_del) == 0:
                            index_to_del = np.array([i])
                        else:
                            index_to_del = np.vstack((index_to_del, np.array([i])))
                        break

        if len(all_delit_index) != 0:
            return np.vstack((all_delit_index, index_to_del))
        else:
            return index_to_del

    @jit(nopython=True)
    def find_need_line(self, coords_chip, color):
        list_without_len_1 = np.array([])
        list_with_len_1 = np.array([])

        if color == black:
            bl_near_chips = self.find_near_chips(coords_chip[0], coords_chip[1], color)

            for near_coords_chip in bl_near_chips:
                for lines in self.now_all_line_blackplayer:
                    if check_in_2D_array(near_coords_chip, lines):
                        in_condition = self.check_line(coords_chip, lines)
                        if in_condition == True:
                            if give_len_line(lines) != 1:
                                if len(list_without_len_1) != 0:
                                    list_without_len_1 = np.vstack((list_without_len_1, [lines]))
                                else:
                                    list_without_len_1 = np.array([lines])
                            else:
                                if len(list_with_len_1) != 0:
                                    list_with_len_1 = np.vstack((list_with_len_1, [lines]))
                                else:
                                    list_with_len_1 = np.array([lines])
        else:
            wh_near_chips = self.find_near_chips(coords_chip[0], coords_chip[1], color)
            for near_coords_chip in wh_near_chips:
                for lines in self.now_all_line_whiteplayer:
                    if check_in_2D_array(near_coords_chip, lines):
                        in_condition = self.check_line(coords_chip, lines)
                        if in_condition == True:
                            if give_len_line(lines) != 1:
                                if len(list_without_len_1) != 0:
                                    list_without_len_1 = np.vstack((list_without_len_1, [lines]))
                                else:
                                    list_without_len_1 = np.array([lines])
                            else:
                                if len(list_with_len_1) != 0:
                                    list_with_len_1 = np.vstack((list_with_len_1, [lines]))
                                else:
                                    list_with_len_1 = np.array([lines])

        if len(list_without_len_1) != 0 and len(list_with_len_1) != 0:
            return np.concatenate(([list_without_len_1, list_with_len_1]))
        else:
            if len(list_with_len_1) == 0:
                return list_without_len_1
            elif len(list_without_len_1) == 0:
                return list_with_len_1

    @jit(nopython=True)
    def adding_lines(self, index_x_rect, index_y_rect, color_player):
        array_with_coord = np.array([index_x_rect, index_y_rect])
        if color_player == black:
            list_whith_lines = self.find_need_line( array_with_coord, color_player)
            delit_index_line = np.array([])
            for index_line in range(len(list_whith_lines)):
                line = list_whith_lines[index_line]
                if len(np.where(delit_index_line == [index_line])[0]) == 0:
                    all_index_empty = give_index_empty(line)
                    line = np.delete(line, all_index_empty, axis=0)
                    if not (index_x_rect < line[0][0] or (index_x_rect == line[0][0] and index_y_rect < line[0][1])):
                        check_connect_another_line, index_connect_line = self.check_connect_lines(array_with_coord, line, self.now_all_line_blackplayer)
                        if check_connect_another_line == True:
                            all_index_empty = give_index_empty(self.now_all_line_blackplayer[index_connect_line])
                            new_connect_line = np.delete(self.now_all_line_blackplayer[index_connect_line], all_index_empty, axis=0)

                            new_line_without_empty = np.concatenate((line, np.array([[index_x_rect, index_y_rect]]), new_connect_line))
                            empty_array = np.full((15 - len(new_line_without_empty), 2), -1)
                            new_line = np.vstack((new_line_without_empty, empty_array))
                            self.now_all_line_blackplayer = np.vstack((self.now_all_line_blackplayer, np.array([new_line])))

                            delit_index_line = self.dellit_near_chips(array_with_coord,new_line_without_empty, list_whith_lines, color_player, delit_index_line)
                            if len(new_connect_line) != 1:
                                if check_in_2D_array(self.now_all_line_blackplayer[index_connect_line], list_whith_lines):
                                    index_to_del = find_index_in_2D_array(self.now_all_line_blackplayer[index_connect_line], list_whith_lines)
                                    delit_index_line = np.vstack((delit_index_line, np.array([index_to_del])))
                                self.now_all_line_blackplayer = np.delete(self.now_all_line_blackplayer, index_connect_line, axis=0)
                            if len(line) != 1:
                                all_index_del = find_index_in_2D_array(list_whith_lines[index_line], self.now_all_line_blackplayer)
                                self.now_all_line_blackplayer = np.delete(self.now_all_line_blackplayer, all_index_del, axis=0)
                        else:
                            new_line_without_empty = np.concatenate((line, np.array([[index_x_rect, index_y_rect]])))
                            empty_array = np.full((15 - len(new_line_without_empty), 2), -1)
                            new_line = np.vstack((new_line_without_empty, empty_array))
                            self.now_all_line_blackplayer = np.vstack((self.now_all_line_blackplayer, np.array([new_line])))

                            if len(line) != 1:
                                delit_index_line = self.dellit_near_chips(array_with_coord,new_line_without_empty, list_whith_lines, color_player,delit_index_line)
                                all_index_del = find_index_in_2D_array(list_whith_lines[index_line], self.now_all_line_blackplayer)
                                self.now_all_line_blackplayer = np.delete(self.now_all_line_blackplayer, all_index_del, axis=0)
                    else:
                        check_connect_another_line, index_connect_line = self.check_connect_lines(array_with_coord, line, self.now_all_line_blackplayer)
                        if check_connect_another_line == True:
                            all_index_empty = give_index_empty(self.now_all_line_blackplayer[index_connect_line])
                            new_connect_line = np.delete(self.now_all_line_blackplayer[index_connect_line], all_index_empty, axis=0)

                            new_line_without_empty = np.concatenate((new_connect_line, np.array([[index_x_rect, index_y_rect]]), line))
                            empty_array = np.full((15 - len(new_line_without_empty), 2), -1)
                            new_line = np.vstack((new_line_without_empty, empty_array))
                            self.now_all_line_blackplayer = np.vstack((self.now_all_line_blackplayer, np.array([new_line])))

                            delit_index_line = self.dellit_near_chips(array_with_coord,new_line_without_empty, list_whith_lines, color_player, delit_index_line)
                            if len(new_connect_line) != 1:
                                if check_in_2D_array(self.now_all_line_blackplayer[index_connect_line], list_whith_lines):
                                    index_to_del = find_index_in_2D_array(self.now_all_line_blackplayer[index_connect_line],list_whith_lines)
                                    delit_index_line = np.vstack((delit_index_line, np.array([index_to_del])))
                                self.now_all_line_blackplayer = np.delete(self.now_all_line_blackplayer, index_connect_line, axis=0)
                            if len(line) != 1:
                                all_index_del = find_index_in_2D_array(list_whith_lines[index_line], self.now_all_line_blackplayer)
                                self.now_all_line_blackplayer = np.delete(self.now_all_line_blackplayer, all_index_del, axis=0)
                        else:
                            new_line_without_empty = np.concatenate((np.array([[index_x_rect, index_y_rect]]), line))
                            empty_array = np.full((15 - len(new_line_without_empty), 2), -1)
                            new_line = np.vstack((new_line_without_empty, empty_array))
                            self.now_all_line_blackplayer = np.vstack((self.now_all_line_blackplayer, np.array([new_line])))

                            if len(line) != 1:
                                delit_index_line = self.dellit_near_chips(array_with_coord,new_line_without_empty, list_whith_lines, color_player, delit_index_line)
                                all_index_del = find_index_in_2D_array(list_whith_lines[index_line], self.now_all_line_blackplayer)
                                self.now_all_line_blackplayer = np.delete(self.now_all_line_blackplayer, all_index_del, axis=0)
        else:
            list_whith_lines = self.find_need_line(array_with_coord, color_player)
            delit_index_line = np.array([])
            for index_line in range(len(list_whith_lines)):
                line = list_whith_lines[index_line]
                if len(np.where(delit_index_line == [index_line])[0]) == 0:
                    all_index_empty = give_index_empty(line)
                    line = np.delete(line, all_index_empty, axis=0)
                    if not (index_x_rect < line[0][0] or (index_x_rect == line[0][0] and index_y_rect < line[0][1])):
                        check_connect_another_line, index_connect_line = self.check_connect_lines(array_with_coord, line, self.now_all_line_whiteplayer)
                        if check_connect_another_line == True:
                            all_index_empty = give_index_empty(self.now_all_line_whiteplayer[index_connect_line])
                            new_connect_line = np.delete(self.now_all_line_whiteplayer[index_connect_line],all_index_empty, axis=0)

                            new_line_without_empty = np.concatenate((line, np.array([[index_x_rect, index_y_rect]]), new_connect_line))
                            empty_array = np.full((15 - len(new_line_without_empty), 2), -1)
                            new_line = np.vstack((new_line_without_empty, empty_array))
                            self.now_all_line_whiteplayer = np.vstack((self.now_all_line_whiteplayer, np.array([new_line])))

                            delit_index_line = self.dellit_near_chips(array_with_coord,new_line_without_empty, list_whith_lines,color_player, delit_index_line)
                            if len(new_connect_line) != 1:
                                if check_in_2D_array(self.now_all_line_whiteplayer[index_connect_line],list_whith_lines):
                                    index_to_del = find_index_in_2D_array(self.now_all_line_whiteplayer[index_connect_line], list_whith_lines)
                                    delit_index_line = np.vstack((delit_index_line, np.array([index_to_del])))
                                self.now_all_line_whiteplayer = np.delete(self.now_all_line_whiteplayer,index_connect_line, axis=0)
                            if len(line) != 1:
                                all_index_del = find_index_in_2D_array(list_whith_lines[index_line],self.now_all_line_whiteplayer)
                                self.now_all_line_whiteplayer = np.delete(self.now_all_line_whiteplayer, all_index_del,axis=0)
                        else:
                            new_line_without_empty = np.concatenate((line, np.array([[index_x_rect, index_y_rect]])))
                            empty_array = np.full((15 - len(new_line_without_empty), 2), -1)
                            new_line = np.vstack((new_line_without_empty, empty_array))
                            self.now_all_line_whiteplayer = np.vstack((self.now_all_line_whiteplayer, np.array([new_line])))

                            if len(line) != 1:
                                delit_index_line = self.dellit_near_chips(array_with_coord,new_line_without_empty, list_whith_lines,color_player, delit_index_line)
                                all_index_del = find_index_in_2D_array(list_whith_lines[index_line],self.now_all_line_whiteplayer)
                                self.now_all_line_whiteplayer = np.delete(self.now_all_line_whiteplayer, all_index_del,axis=0)
                    else:
                        check_connect_another_line, index_connect_line = self.check_connect_lines(array_with_coord, line, self.now_all_line_whiteplayer)
                        if check_connect_another_line == True:
                            all_index_empty = give_index_empty(self.now_all_line_whiteplayer[index_connect_line])
                            new_connect_line = np.delete(self.now_all_line_whiteplayer[index_connect_line],all_index_empty, axis=0)

                            new_line_without_empty = np.concatenate((new_connect_line, np.array([[index_x_rect, index_y_rect]]), line))
                            empty_array = np.full((15 - len(new_line_without_empty), 2), -1)
                            new_line = np.vstack((new_line_without_empty, empty_array))
                            self.now_all_line_whiteplayer = np.vstack((self.now_all_line_whiteplayer, np.array([new_line])))

                            delit_index_line = self.dellit_near_chips(array_with_coord,new_line_without_empty, list_whith_lines,color_player, delit_index_line)
                            if len(new_connect_line) != 1:
                                if check_in_2D_array(self.now_all_line_whiteplayer[index_connect_line],list_whith_lines):
                                    index_to_del = find_index_in_2D_array(self.now_all_line_whiteplayer[index_connect_line], list_whith_lines)
                                    delit_index_line = np.vstack((delit_index_line, np.array([index_to_del])))
                                self.now_all_line_whiteplayer = np.delete(self.now_all_line_whiteplayer,index_connect_line, axis=0)
                            if len(line) != 1:
                                all_index_del = find_index_in_2D_array(list_whith_lines[index_line],self.now_all_line_whiteplayer)
                                self.now_all_line_whiteplayer = np.delete(self.now_all_line_whiteplayer, all_index_del,axis=0)
                        else:
                            new_line_without_empty = np.concatenate((np.array([[index_x_rect, index_y_rect]]), line))
                            empty_array = np.full((15 - len(new_line_without_empty), 2), -1)
                            new_line = np.vstack((new_line_without_empty, empty_array))
                            self.now_all_line_whiteplayer = np.vstack((self.now_all_line_whiteplayer, np.array([new_line])))

                            if len(line) != 1:
                                delit_index_line = self.dellit_near_chips(array_with_coord,new_line_without_empty, list_whith_lines,color_player, delit_index_line)
                                all_index_del = find_index_in_2D_array(list_whith_lines[index_line],self.now_all_line_whiteplayer)
                                self.now_all_line_whiteplayer = np.delete(self.now_all_line_whiteplayer, all_index_del,axis=0)

        if color_player == white:
            if len(self.now_all_line_whiteplayer) == 0:
                empty_array = np.full((14, 2), -1)
                new_line = np.vstack((np.array([[index_x_rect, index_y_rect]]), empty_array))
                self.now_all_line_whiteplayer = np.array([new_line])
            else:
                empty_array = np.full((14, 2), -1)
                new_line = np.vstack((np.array([[index_x_rect, index_y_rect]]), empty_array))
                self.now_all_line_whiteplayer = np.vstack((self.now_all_line_whiteplayer, np.array([new_line])))
        else:
            if len(self.now_all_line_blackplayer) == 0:
                empty_array = np.full((14, 2), -1)
                new_line = np.vstack((np.array([[index_x_rect, index_y_rect]]), empty_array))
                self.now_all_line_blackplayer = np.array([new_line])
            else:
                empty_array = np.full((14, 2), -1)
                new_line = np.vstack((np.array([[index_x_rect, index_y_rect]]), empty_array))
                self.now_all_line_blackplayer = np.vstack((self.now_all_line_blackplayer,  np.array([new_line])))


    def check_motion(self, x, y):
        x_rect = np.round(x / cell_size_ramka)
        y_rect = np.round(y / cell_size_ramka)

        if x <= (cell_qty * cell_size_ramka) and x >= 0 and y <= (cell_qty * cell_size_ramka) and y >= 0:
            if not check_in_2D_array(np.array([x_rect, y_rect, white]), self.now_coord_all_move_and_color) and not check_in_2D_array(np.array([x_rect, y_rect, black]), self.now_coord_all_move_and_color):
                return True
        return False

    @jit(nopython=True)
    def check_motion_for_generator(self, x, y):

        if x <= cell_qty and x >= 0 and y <= cell_qty and y >= 0:
            if not check_in_2D_array(np.array([x, y, white]), self.now_coord_all_move_and_color) and not check_in_2D_array(np.array([x, y, black]), self.now_coord_all_move_and_color):
                return True

        return False

    @jit(nopython=True)
    def check_motion_for_pose_score(self, x_rect, y_rect):

        if x_rect <= cell_qty and x_rect >= 0 and y_rect <= cell_qty and y_rect >= 0:
            if not check_in_2D_array(np.array([x_rect, y_rect, white]), self.now_coord_all_move_and_color) and not check_in_2D_array(np.array([x_rect, y_rect, black]), self.now_coord_all_move_and_color):
                return True

        return False





@jit(nopython=True)
def check_want_newgame(self, x_pixel, y_pixel):
    if x_pixel >= 700 and x_pixel <= 840 and y_pixel >= 180 and y_pixel < 250:
        return True
    return False



@jit(nopython=True)
def check_in_2D_array(check_array, check_in_array):
    for i, sub in enumerate(check_in_array):
        if np.array_equal(sub, check_array):
            return True
    return False
@jit(nopython=True)
def find_index_in_2D_array(check_array, check_in_array):
    for i, sub in enumerate(check_in_array):
        if np.array_equal(sub, check_array):
            return i

@jit(nopython=True)
def give_index_empty(array_with_empty):
    index_empty = []
    for index, sub in enumerate(array_with_empty):
        if np.array_equal(sub, np.array([-1,-1])):
            index_empty.append(index)
    return index_empty

@jit(nopython=True)
def give_len_line(array):
    lenn = 0
    empty = np.array([-1,-1])
    for i, sub in enumerate(array):
        if np.array_equal(sub, empty):
            return lenn
        lenn += 1