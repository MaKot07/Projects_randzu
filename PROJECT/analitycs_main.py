from numba import njit
from numba import typed, prange
import numpy as np



black = -1
white = 1
cell_qty = 14
cell_size = 40
cell_size_ramka = 42



@njit
def adding_lines(index_x_rect, index_y_rect, color_player, player_lines_array, now_coord_all_move_and_color):
    array_with_coord = np.array([index_x_rect, index_y_rect], dtype=np.int8)
    player_lines = in_list_all_lines(player_lines_array)

    delit_index_line = []
    passed_index_line = []


    new_line_template = np.full((9, 2), -1, dtype=np.int8)


    near_chips, have_near_chips = find_near_chips(array_with_coord[0], array_with_coord[1], color_player, now_coord_all_move_and_color)

    list_whith_lines = find_need_line(array_with_coord, player_lines_array, near_chips)

    if player_lines:
        new_line_template[0] = array_with_coord
        copy_new_line_template = new_line_template.copy()
        player_lines.append(copy_new_line_template)
        new_line_template[0] = np.array([-1, -1], dtype=np.int8)

    else:
        new_line_template[0] = array_with_coord
        copy_new_line_template = new_line_template.copy()
        player_lines.append(copy_new_line_template)

    for index_line, line in enumerate(list_whith_lines):
        if index_line not in passed_index_line:
            all_index_empty = give_index_empty(line)
            line_without_empty = delete_by_index(line, all_index_empty)
            check_connect_another_line, index_connect_line = check_connect_lines(array_with_coord,line_without_empty, player_lines)

            if check_connect_another_line:
                new_connect_line = create_line_with_connect(array_with_coord, line_without_empty,player_lines[index_connect_line])
                new_line = create_new_line(new_connect_line)
                player_lines.append(new_line)
                passed_index_line.extend(dellit_near_chips(array_with_coord, new_line, player_lines[index_connect_line], list_whith_lines))
                if give_len_line(player_lines[index_connect_line]) != 1:
                    delit_index_line.append(index_connect_line)
            else:
                new_connect_line = create_line_without_connect(array_with_coord, line_without_empty)
                new_line = create_new_line(new_connect_line)
                player_lines.append(new_line)
                passed_index_line.extend(
                    dellit_near_chips_without_connect(array_with_coord, new_line, list_whith_lines))

            if len(line_without_empty) != 1:
                delit_index_line.append(find_index_in_2D_array(list_whith_lines[index_line], player_lines))

    array_player_lines = list_in_array(player_lines)
    if delit_index_line:
        return delete_by_index(array_player_lines, delit_index_line)
    else:
        return array_player_lines




@njit
def find_near_chips(x, y, need_color, coord_all_move_and_color):
    near_chips = []
    chip = np.array([0, 0, need_color])

    for i in prange(-1, 2):
        for j in prange(-1, 2):
            if i == 0 and j == 0:
                continue
            chip[0] = x + i
            chip[1] = y + j
            if check_in_2D_array(chip, coord_all_move_and_color):
                near_chips.append([chip[0], chip[1]])

    if len(near_chips) == 0:
        return np.empty((0, 2), dtype=np.int8), False

    return np.array(near_chips, dtype=np.int8), True

@njit
def find_need_line(coords_chip, now_all_line_player, near_chips):
    list_without_len_1 = []
    list_with_len_1 = []
    result_list = typed.List()

    for i in prange(len(near_chips)):
        near_coords_chip = near_chips[i]
        for j in range(len(now_all_line_player)):
            lines = now_all_line_player[j]
            if check_in_2D_array(near_coords_chip, lines):
                in_condition = check_line(coords_chip, lines)
                if in_condition:
                    line_length = give_len_line(lines)
                    if line_length != 1:
                        list_without_len_1.append(lines)
                    else:
                        list_with_len_1.append(lines)


    if len(list_with_len_1) > 0 and len(list_without_len_1) == 0:
        for arr in list_with_len_1:
            result_list.append(arr)
        return result_list
    elif len(list_without_len_1) > 0 and len(list_with_len_1) == 0:
        for arr in list_without_len_1:
            result_list.append(arr)
        return result_list

    for arr in list_without_len_1:
        result_list.append(arr)
    for arr in list_with_len_1:
        result_list.append(arr)
    return result_list

@njit
def check_connect_lines(coord_chip, line_without_empty, all_line):
    add = (False, 0)

    if not (coord_chip[0] < line_without_empty[0][0] or (coord_chip[0] == line_without_empty[0][0] and coord_chip[1] < line_without_empty[0][1])):
        new_coord_x_chip = coord_chip[0] + (coord_chip[0] - line_without_empty[-1][0])
        new_coord_y_chip = coord_chip[1] + (coord_chip[1] - line_without_empty[-1][1])
        next_coord_chip = np.array([new_coord_x_chip, new_coord_y_chip], dtype=np.int8)
    else:
        new_coord_x_chip = coord_chip[0] - (line_without_empty[0][0] - coord_chip[0])
        new_coord_y_chip = coord_chip[1] - (line_without_empty[0][1] - coord_chip[1])
        next_coord_chip = np.array([new_coord_x_chip, new_coord_y_chip], dtype=np.int8)

    result_index = -1
    found = False

    for index in prange(len(all_line)):
        lines = all_line[index]
        if check_in_2D_array(next_coord_chip, lines):
            if give_len_line(lines) != 1:
                check_next_line = check_line(coord_chip, lines)
                if check_next_line:
                    found = True
                    result_index = index
                    break
            else:
                if np.array_equal(all_line[index], lines):
                    add = (True, index)

    if found:
        return (True, result_index)

    return add

@njit
def dellit_near_chips(coords_chip, new_line, connect_line, list_whith_lines):
    index_to_del = []

    for i in prange(len(new_line)):
        if (coords_chip == new_line[i]).all():
            for j in prange(len(list_whith_lines)):
                arr_with_lines = list_whith_lines[j]
                if (new_line[i - 1] == arr_with_lines[0]).all() or (new_line[i + 1] == arr_with_lines[0]).all() or (connect_line == arr_with_lines).all():
                    index_to_del.append(j)
            break

    return index_to_del

@njit
def dellit_near_chips_without_connect(coords_chip, new_line, list_whith_lines):
    index_to_del = []

    arr_empty = np.array([-1, -1], dtype=np.int8)
    if (coords_chip == new_line[0]).all():
        for j, arr_with_lines in enumerate(list_whith_lines):
            if (new_line[1] == arr_with_lines[0]).all() and (arr_empty == arr_with_lines[1]).all():
                index_to_del = [j]
                return index_to_del

    for i, arr in enumerate(new_line):
        if (coords_chip == arr).all():
            for j, arr_with_lines in enumerate(list_whith_lines):
                if (new_line[i - 1] == arr_with_lines[0]).all() and (arr_empty == arr_with_lines[1]).all():
                    index_to_del.append(j)
                    break
            break

    return index_to_del

@njit
def create_line_with_connect(chip_coord, line, connect_line):
    mask = give_index_empty_in_mask(connect_line)
    new_connect_line = connect_line[~mask]
    chip_coord_2d = np.array([[-1,-1]], dtype=np.int8)
    chip_coord_2d[0] = chip_coord
    if chip_coord[0] < line[0][0] or (chip_coord[0] == line[0][0] and chip_coord[1] < line[0][1]):
        new_line_without_empty = np.concatenate((new_connect_line, chip_coord_2d, line))
        return new_line_without_empty
    else:
        new_line_without_empty = np.concatenate((line, chip_coord_2d, new_connect_line))
        return new_line_without_empty

@njit
def create_line_without_connect(chip_coord, line):
    chip_coord = np.asarray(chip_coord, dtype=np.int8)
    chip_coord_2d = np.expand_dims(chip_coord, axis=0)

    if chip_coord[0] < line[0][0] or (chip_coord[0] == line[0][0] and chip_coord[1] < line[0][1]):
        new_line_without_empty = np.concatenate((chip_coord_2d, line), axis=0)
        return new_line_without_empty
    else:
        new_line_without_empty = np.concatenate((line, chip_coord_2d), axis=0)
        return new_line_without_empty

@njit
def create_new_line(new_line_without_empty):
    new_line_with_empty = np.full((9, 2), -1, dtype=np.int8)
    for i, arr in enumerate(new_line_without_empty):
        new_line_with_empty[i] = arr
    return new_line_with_empty


@njit
def check_want_newgame(x_pixel, y_pixel):
    if x_pixel >= 700 and x_pixel <= 840 and y_pixel >= 180 and y_pixel < 250:
        return True
    return False


#Not good
@njit
def check_in_2D_array(check_array, check_in_array):
    if check_in_array.size == 0:
        return False

    n_rows = check_in_array.shape[0]

    for i in prange(n_rows):
        if (check_in_array[i] == check_array).all():
            return True
    return False

@njit
def check_in_2D_list(check_array, check_in_list):
    if check_in_list[0].size == 0:
        return False
    for sub in check_in_list:
        if (sub == check_array).all():
            return True
    return False

@njit
def check_not_in_2D_list(check_array, check_in_list):
    if check_in_list[0].size == 0:
        return True
    for sub in check_in_list:
        if (sub == check_array).all():
            return False
    return True



@njit
def find_index_in_2D_array(check_array, check_in_array):
    for i, sub in enumerate(check_in_array):
        if np.array_equal(sub, check_array):
            return i
    return -1

@njit
def give_index_empty(array_with_empty):
    index_empty = []
    for index, sub in enumerate(array_with_empty):
        if np.array_equal(sub, np.array([-1,-1], dtype=np.int8)):
            index_empty.append(index)
    return index_empty

@njit
def give_index_empty_in_mask(array_with_empty):
    empty = np.array([-1, -1], dtype=np.int8)
    mask = np.zeros(array_with_empty.shape[0], dtype=np.bool_)

    for i in range(array_with_empty.shape[0]):
        mask[i] = np.all(array_with_empty[i] == empty)

    return mask

@njit
def check_line(coord_chip, our_line):
    x, y = coord_chip
    min_chip = our_line[0]
    if our_line[1][0] == -1:
        return True
    else:
        if not (coord_chip[0] < min_chip[0] or (coord_chip[0] == min_chip[0] and coord_chip[1] < min_chip[1])):
            rate_x_progressive = our_line[1][0] - our_line[0][0]
            rate_y_progressive = our_line[1][1] - our_line[0][1]

            for i in range(len(our_line)):
                if np.array_equal(our_line[i+1], np.array([-1,-1], dtype=np.int8)):
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
@njit
def check_draw_njit(cell_qty, now_coord_all_move_and_color):
    for x in range(cell_qty + 1):
        for y in range(cell_qty + 1):
            new_arr_wh = np.array([[x, y, white]], dtype=np.int8)
            new_arr_bl = np.array([[x, y, black]], dtype=np.int8)
            if not check_in_2D_array(new_arr_wh, now_coord_all_move_and_color) or not check_in_2D_array(new_arr_bl, now_coord_all_move_and_color):
                return False
    return True

@njit
def give_len_line(line):
    lenn = 0
    empty = np.array([-1,-1], dtype=np.int8)
    for i, sub in enumerate(line):
        if np.array_equal(sub, empty):
            break
        lenn += 1
    return lenn


@njit
def check_win_njit(all_line):
    for line in all_line:
        if give_len_line(line) >= 5:
            return True
    return False

@njit
def check_motion_for_brain(x, y, now_coord_all_move_and_color):

    if x <= cell_qty and x >= 0 and y <= cell_qty and y >= 0:
        if not check_in_2D_array(np.array([x, y, white], dtype=np.int8), now_coord_all_move_and_color) and not check_in_2D_array(np.array([x, y, black], dtype=np.int8), now_coord_all_move_and_color):
            return True

    return False

@njit
def check_motion_for_generator(coord_chip_and_color, now_coord_all_move_and_color):
    if coord_chip_and_color[0] <= cell_qty and coord_chip_and_color[0] >= 0 and coord_chip_and_color[1] <= cell_qty and coord_chip_and_color[1] >= 0:
        if not check_in_2D_array(np.array([coord_chip_and_color[0], coord_chip_and_color[1], white], dtype=np.int8), now_coord_all_move_and_color) and not check_in_2D_array(np.array([coord_chip_and_color[0], coord_chip_and_color[1], black], dtype=np.int8), now_coord_all_move_and_color):
            return True
    return False

@njit
def in_list_all_lines(all_lines):
    result_list = []
    for arr in all_lines:
        result_list.append(arr)
    return result_list

@njit
def delete_by_index(arr, indices_to_delete):

    mask = np.ones(arr.shape[0], dtype=np.bool_)
    for i in indices_to_delete:
        mask[i] = False
    return arr[mask]

@njit
def list_in_array(list_arrays):
    result_array = np.full((len(list_arrays), 9, 2), -1, dtype=np.int8)

    for i, arr in enumerate(list_arrays):
        result_array[i] = arr

    return  result_array

@njit
def copy_array(array):
    copy_arr = np.empty_like(array)
    for i,arr in enumerate(array):
        copy_arr[i] = np.copy(arr)
    return copy_arr


@njit
def remove_element_by_index(lst, idx):
    return [lst[i] for i in range(len(lst)) if i != idx]

@njit
def remove_element_from_list(lst, val):
    return [x for x in lst if not np.array_equal(x, val)]

@njit
def create_independent_dict(original):
    new_dict = typed.Dict()
    for key, value in original.items():
        new_dict[key] = value
    return new_dict
