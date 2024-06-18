from Const import *
from analitycs.analitycs_main import *
import random
import copy

now_coord_all_move_and_color = []




class Intelect(Analitycs):

    def __init__(self, now_all_line_blackplayer=[], now_all_line_whiteplayer=[], now_coord_all_move_and_color=[], color=()):
        self.now_coord_all_move_and_color = copy.copy(now_coord_all_move_and_color)
        self.now_all_line_blackplayer = copy.copy(now_all_line_blackplayer)
        self.now_all_line_whiteplayer = copy.copy(now_all_line_whiteplayer)
        self.color = copy.copy(color)

    def __del__(self):
        return

    def generator_motion(self):
        sgen_motion = []

        coord_left_border = 100
        coord_down_border = -1
        coord_right_border = -1
        coord_up_border = 100
        for (x_coord_enemy, y_cooord_enemy), color_enemy in self.now_coord_all_move_and_color:
            if x_coord_enemy < coord_left_border:
                coord_left_border = x_coord_enemy
            if x_coord_enemy > coord_right_border:
                coord_right_border = x_coord_enemy
            if y_cooord_enemy > coord_down_border:
                coord_down_border = y_cooord_enemy
            if y_cooord_enemy < coord_up_border:
                coord_up_border = y_cooord_enemy

        for x_coord in range(coord_left_border - 1, coord_right_border + 2):
            for y_coord in range(coord_up_border - 1, coord_down_border + 2):
                check_new_motion = self.check_motion_for_generator(x_coord, y_coord)
                if check_new_motion:
                    sgen_motion.append((x_coord, y_coord))
        return sgen_motion

    def find_position_score(self):
        pos_score = 0
        for line in self.now_all_line_whiteplayer:
            check_isolated = self.check_line_isolated(line, WHITE)
            if check_isolated == 0:
                if len(line) == 4:
                    pos_score += 17500
                if len(line) == 3:
                    pos_score += 3000
                if len(line) == 2:
                    pos_score += 140
                if len(line) == 1:
                    pos_score += 5

            if check_isolated == 1:
                if len(line) == 4:
                    pos_score += 9500
                if len(line) == 3:
                    pos_score += 560
                if len(line) == 2:
                    pos_score += 60
                if len(line) == 1:
                    pos_score += 10

        for line in self.now_all_line_blackplayer:
            check_isolated = self.check_line_isolated(line, BLACK)
            if check_isolated == 0:
                if len(line) == 4:
                    pos_score -= 17500
                if len(line) == 3:
                    pos_score -= 3000
                if len(line) == 2:
                    pos_score -= 140
                if len(line) == 1:
                    pos_score -= 5

            if check_isolated == 1:
                if len(line) == 4:
                    pos_score -= 9500
                if len(line) == 3:
                    pos_score -= 560
                if len(line) == 2:
                    pos_score -= 60
                if len(line) == 1:
                    pos_score -= 10
        return pos_score

    def find_win_position_score(self):
        pos_score = 0
        if self.check_colors_win() == WHITE:
            pos_score += 1000000
        else:
            pos_score -= 1000000
        return pos_score


    def check_line_isolated(self, our_check_line, color_our_line):
        if len(our_check_line) == 1:
            if color_our_line == BLACK:
                near_chips = self.find_near_chips(our_check_line[0][0], our_check_line[0][1], WHITE)
                for new_coord_x, new_coord_y in near_chips:
                    check_coord_new = self.check_motion_for_pose_score(new_coord_x, new_coord_y)
                    if check_coord_new == True:
                        return 1
                return 0
            else:
                near_chips = self.find_near_chips(our_check_line[0][0], our_check_line[0][1], BLACK)
                for new_coord_x, new_coord_y in near_chips:
                    check_coord_new = self.check_motion_for_pose_score(new_coord_x, new_coord_y)
                    if check_coord_new == True:
                        return 1
                return 0

        x_progressive = our_check_line[1][0] - our_check_line[0][0]
        y_progressive = our_check_line[1][1] - our_check_line[0][1]

        coord_new_max = (x_progressive + our_check_line[-1][0], y_progressive + our_check_line[-1][1])
        coord_new_min = (our_check_line[0][0] - x_progressive, our_check_line[0][1] - y_progressive)

        check_coord_new_max = self.check_motion_for_pose_score(coord_new_max[0], coord_new_max[1])
        check_coord_new_min = self.check_motion_for_pose_score(coord_new_min[0], coord_new_min[1])

        if check_coord_new_max == False and check_coord_new_min == False:
            return 2
        else:
            if check_coord_new_max == False or check_coord_new_min == False:
                return 1
            else:
                return 0

    def get_new_state(self, new_move, color):
        new_coord_all_move_and_color = copy.copy(self.now_coord_all_move_and_color) + [(new_move, self.color)]
        new_all_line = copy.copy([self.now_all_line_blackplayer, self.now_all_line_whiteplayer])

        self.adding_lines(new_move[0], new_move[1], self.color)
        createn_new_state = Intelect(new_all_line[0], new_all_line[1], new_coord_all_move_and_color, color)

        return createn_new_state

    def minimax(self, depth, maximizingPlayer, alpha=float('-inf'), beta=float('inf')):
        best_movement = (0, 0)

        if self.check_colors_win() != None:
            #if self.check_colors_win() == BLACK:
            print(depth, self.check_colors_win(), self.find_win_position_score())
            return (self.find_win_position_score(), None)
        if depth == 0:
            #print(depth, self.check_colors_win(), self.find_position_score())
            return (self.find_position_score(), None)

        if maximizingPlayer:
            value = -float('inf')
            possible_moves = self.generator_motion()

            for move in possible_moves:
                child = self.get_new_state(move, BLACK)

                tmp, _ = child.minimax(depth - 1, not maximizingPlayer, alpha, beta)
                del child

                if tmp > value:
                    value = tmp
                    best_movement = move

                if value >= beta:
                    break
                alpha = max(alpha, value)

        else:
            value = float('inf')
            possible_moves = self.generator_motion()

            for move in possible_moves:
                child = self.get_new_state(move, WHITE)

                tmp, _ = child.minimax(depth - 1, not maximizingPlayer, alpha, beta)
                del child

                if tmp < value:
                    value = tmp
                    best_movement = move

                if value <= alpha:
                    break
                beta = min(beta, value)

        return (value, best_movement)










