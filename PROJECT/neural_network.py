import copy

import numba
from numba import typed, types

from tensorflow import keras
from tensorflow.keras import layers
import tensorflow as tf
from tensorflow.keras.layers import Layer
from tensorflow.keras.layers import Input, Dense

import matplotlib.pyplot as plt

from Graphics.Graphics_main import *
import sys
from Brain_main import *
import pickle

def generation_position_and_save(n, number_move):

    black = -1
    white = 1
    cell_qty = 14
    color_move = black
    percent_random = 0.1
    percent_depth1 = 0.4

    ni = 0
    while ni < n:
        sgen_board = Board(black)

        coord_move = (np.random.randint(5, 9), np.random.randint(5, 9))
        sgen_board.set_coord(coord_move[0], coord_move[1], black)
        sgen_board.adding_lines(coord_move[0], coord_move[1], black)

        variants_move = P_generator_motion(coord_move, sgen_board.give_chips())
        coord_move = variants_move[np.random.randint(0, len(variants_move)-1)]
        sgen_board.set_coord(coord_move[0], coord_move[1], white)
        sgen_board.adding_lines(coord_move[0], coord_move[1], white)

        for i in range(number_move-2):
            level_choice = np.random.random()

            if level_choice <= percent_random:
                variants_move = P_generator_motion(coord_move, sgen_board.give_chips(), copy.copy(variants_move))
                coord_move = variants_move[np.random.randint(0, len(variants_move)-1)]


                sgen_board.set_coord(coord_move[0], coord_move[1], color_move)
                sgen_board.adding_lines(coord_move[0], coord_move[1], color_move)
                make_position(sgen_board.give_chips(), [sgen_board.give_all_line_blackplayer(), sgen_board.give_all_line_whiteplayer()])

            elif level_choice <= percent_depth1:
                maximizing = True if color_move == white else False
                variants_move = P_generator_motion(coord_move, sgen_board.give_chips(), copy.copy(variants_move))

                Board_SillyMinMax = Board(color_move, sgen_board.give_all_line_blackplayer(),
                                     sgen_board.give_all_line_whiteplayer(), sgen_board.give_chips())

                _, coord_move, c = sily_minimax(Board_SillyMinMax, 1, variants_move, maximizing)

                sgen_board.set_coord(coord_move[0], coord_move[1], color_move)
                sgen_board.adding_lines(coord_move[0], coord_move[1], color_move)

                make_position(sgen_board.give_chips(), [sgen_board.give_all_line_blackplayer(), sgen_board.give_all_line_whiteplayer()])

            else:
                maximizing = True if color_move == white else False
                variants_move = P_generator_motion(coord_move, sgen_board.give_chips(), copy.copy(variants_move))

                Board_SillyMinMax = Board(color_move, sgen_board.give_all_line_blackplayer(),
                                          sgen_board.give_all_line_whiteplayer(), sgen_board.give_chips())

                _, coord_move, _ = sily_minimax(Board_SillyMinMax, 2, variants_move, maximizing)

                sgen_board.set_coord(coord_move[0], coord_move[1], color_move)
                sgen_board.adding_lines(coord_move[0], coord_move[1], color_move)

                make_position(sgen_board.give_chips(), [sgen_board.give_all_line_blackplayer(), sgen_board.give_all_line_whiteplayer()])

            win_color = sgen_board.check_colors_win()
            if win_color != 0:
                break

            if color_move == black:
                color_move = white
            else:
                color_move = black

            ni += 1



def make_position(all_coords, all_lines):
    len_board = 15
    position = np.zeros((225), dtype=np.int8)

    for i in range(len(all_coords)):
        position[ all_coords[i][1]*len_board + all_coords[i][0] ] = all_coords[i][2]


    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data.csv', 'a', newline='') as file:
        np.savetxt(file, [position], delimiter=',', newline='\n', fmt='%d')

    # with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(black).csv', 'a', newline='') as file:
    #     np.savetxt(file, np.vstack(all_lines[0]), delimiter=',', newline='\n', fmt='%d')
    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(black).csv', 'ab') as file:
        pickle.dump(all_lines[0], file)


    # with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(white).csv', 'a', newline='') as file:
    #     np.savetxt(file, np.vstack(all_lines[1]), delimiter=',', newline='\n', fmt='%d')
    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(white).csv', 'ab') as file:
        pickle.dump(all_lines[1], file)

def sily_minimax(board_condition, depth, last_variants, maximizingPlayer, alpha=float('-inf'), beta=float('inf'), count_variants=0):

    if board_condition.check_colors_win() != 0:
        return (board_condition.find_win_position_score(), (-1,-1), count_variants)
    if depth <= 0:
        bl_line = board_condition.now_all_line_blackplayer
        wh_line = board_condition.now_all_line_whiteplayer
        all_coord = board_condition.now_coord_all_move_and_color
        return (find_position_score(bl_line, wh_line, all_coord), (-1,-1), count_variants)

    if maximizingPlayer:
        value = float('-inf')

        for move in last_variants:
            child = board_condition.get_new_state(move, black)
            new_variants_move = P_generator_motion(move, board_condition.give_chips(), copy.copy(last_variants))

            count_variants += 1
            ##print("#@%", count_variants)
            tmp, _, count_variants = sily_minimax(child, depth - 1, copy.copy(new_variants_move), not maximizingPlayer, alpha, beta, count_variants)

            if tmp > value:
                value = tmp
                best_movement = move

            if value > beta:
                break
            alpha = max(alpha, value)

    else:
        value = float('inf')

        for move in last_variants:
            child = board_condition.get_new_state(move, white)
            new_variants_move = P_generator_motion(move, board_condition.give_chips(), copy.copy(last_variants))

            count_variants += 1
            ##print("#@%", count_variants)
            tmp, _, count_variants = sily_minimax(child, depth - 1, copy.copy(new_variants_move), not maximizingPlayer, alpha, beta, count_variants)

            if tmp < value:
                value = tmp
                best_movement = move

            if value < alpha:
                break
            beta = min(beta, value)

    return value, best_movement, count_variants


#Visualisation
def show_positions():
    positions = np.loadtxt(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data.csv', delimiter=',',
                     dtype=int)

    labels = np.loadtxt(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_labels.csv',
                           delimiter=',',
                           dtype=int)

    # all_black_lines = np.loadtxt(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(black).csv', delimiter=',',
    #                  dtype=int)
    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(black).csv', 'rb') as file:
        all_black_lines = []
        while True:
            try:
                all_black_lines.append(pickle.load(file))
            except EOFError:
                break


    # all_white_lines = np.loadtxt(
    #     r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(white).csv', delimiter=',',
    #     dtype=int)
    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(white).csv', 'rb') as file:
        all_white_lines = []
        while True:
            try:
                all_white_lines.append(pickle.load(file))
            except EOFError:
                break

    i = 0

    Visual_board = Game_Graphics(0)
    Visual_board.draw_all_game(0, [])

    while True:
        event = now_event()

        if event != None:
            if event.type == pygame.QUIT:
                sys.exit()

            if event.button == 1:
                i += 1
                if i >= len(positions):
                    sys.exit()
            if event.button == 3:
                i = int(input())
                if i >= len(positions):
                    sys.exit()

            Visual_board = Game_Graphics(0, convert_positions(positions[i]))

            label = np.where(labels[i] == max(labels[i]))[0][0]
            coord_best_move = (label - (label // 15) * 15, label // 15)
            #print(coord_best_move)
            index_x_rect, index_y_rect = coord_best_move[0], coord_best_move[1]
            Visual_board.draw_all_game(0, [], (index_x_rect, index_y_rect))
            # #print("BLACK", all_black_lines[i])
            # #print("WHITE", all_white_lines[i])

def now_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return event

        if event.type == pygame.MOUSEBUTTONDOWN:
            return event

def convert_positions(position):
    len_board = 15

    conv_pos = []

    for i in range(len_board):
        for j in range(len_board):
            if position[ i*len_board + j ] != 0:
                conv_pos.append(np.array(( j, i, position[ i*len_board + j ] )))

    return np.array(conv_pos, dtype=np.int8)


def generation_labels():
    labels = np.loadtxt(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_labels.csv',
                        delimiter=',',
                        dtype=int)

    positions = np.loadtxt(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data.csv',
                           delimiter=',',
                           dtype=int)

    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(black).csv', 'rb') as file:
        all_black_lines = []
        while True:
            try:
                all_black_lines.append(pickle.load(file))
            except EOFError:
                break

    with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data_for_labels(white).csv', 'rb') as file:
        all_white_lines = []
        while True:
            try:
                all_white_lines.append(pickle.load(file))
            except EOFError:
                break

    possible_moves = typed.Dict.empty(
        key_type=types.UniTuple(types.int64, 2),
        value_type=numba.types.float64
    )


    for sample in range(len(labels), len(positions)):
        #print("Succesfull is:", ((sample+1)/len(positions))*100, "%")
        position = convert_positions(positions[sample])

        if len(position) % 2 == 0:
            color_minmax = black
        else:
            color_minmax = white

        Board_MinMax_for_labels = Board(color_minmax,all_black_lines[sample],
                             all_white_lines[sample], position)

        possible_moves = new_generator_motion_for_create_start_moves(
             Board_MinMax_for_labels.give_chips(), possible_moves,
            Board_MinMax_for_labels.give_all_line_whiteplayer(), white)

        possible_moves = new_generator_motion_for_create_start_moves(
             Board_MinMax_for_labels.give_chips(),
            create_independent_dict(possible_moves), Board_MinMax_for_labels.give_all_line_blackplayer(), black)

        next_variants_move_and_motion = ((-2,-2),create_independent_dict(possible_moves))

        maxim = True if color_minmax == white else False
        best_value, coord_best_move, count_all_variants = minimax(Board_MinMax_for_labels, 25, next_variants_move_and_motion,
                                                                  maxim, float('-inf'), float('inf'), 0)

        if coord_best_move[0] >= 0:
            new_labels = np.zeros((255), dtype=np.int8)
            new_labels[coord_best_move[1]*15 + coord_best_move[0]] = 1
            ##print(coord_best_move, " ", new_labels)
        else:
            new_labels = np.zeros((255))
            new_labels[0] = -100

        with open(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_labels.csv', 'a',
                  newline='') as file:
            np.savetxt(file, [new_labels], delimiter=',', newline='\n', fmt='%d')

        possible_moves_white_pl = typed.Dict.empty(
            key_type=types.UniTuple(types.int64, 2),
            value_type=numba.types.int64
        )
        possible_moves_black_pl = typed.Dict.empty(
            key_type=types.UniTuple(types.int64, 2),
            value_type=numba.types.int64
        )


@njit
def new_generator_motion_for_create_start_moves(now_coord_all_move_and_color, dict_with_variants, line_enemy, color_enemy):
    if not now_coord_all_move_and_color.any():
        dict_with_variants[(7, 7)] = 0.001
        return dict_with_variants

    coefficent = [0.1, 0.3, 0.5]
    empty = np.array([-1, -1], dtype=np.int8)

    all_coords = []
    for coord in now_coord_all_move_and_color:
        if coord[2] == color_enemy:
            all_coords.append((coord[0], coord[1]))

    for new_coord_motion in all_coords:
        new_coord_motion = np.array(new_coord_motion)
        for line in line_enemy:
            if check_in_2D_array(new_coord_motion, line):
                if np.array_equal(line[1], empty):
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            if i == 0 and j == 0:
                                continue
                            chip = (new_coord_motion[0] + i, new_coord_motion[1] + j)
                            if chip not in dict_with_variants and check_motion_for_brain(chip[0], chip[1], now_coord_all_move_and_color):
                                dict_with_variants[chip] = coefficent[0]
                    continue

                line_length = give_len_line(line)
                x_progressive = line[1][0] - line[0][0]
                y_progressive = line[1][1] - line[0][1]

                coord_new_max = (
                x_progressive + line[line_length-1][0], y_progressive + line[line_length-1][1])
                coord_new_min = (line[0][0] - x_progressive, line[0][1] - y_progressive)

                for coord in [coord_new_max, coord_new_min]:
                    if check_motion_for_brain(coord[0], coord[1], now_coord_all_move_and_color):
                        if line_length == 2:
                            dict_with_variants[coord] = coefficent[1]
                        elif line_length >= 3:
                            dict_with_variants[coord] = coefficent[2]

    return dict_with_variants


def train_neural_network():
    labels = np.loadtxt(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_labels.csv',
                        delimiter=',',
                        dtype=int)

    positions = np.loadtxt(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\train_data.csv',
                           delimiter=',',
                           dtype=int)

    empty_pos = []
    for i in range(len(labels)):
        if labels[i][0] < -10:
            empty_pos.append(i)

    labels = np.delete(labels, empty_pos, axis=0)
    positions = np.delete(positions, empty_pos, axis=0)
    positions = np.copy(positions[0:len(labels)])



    for i in range(len(positions)):
        if np.sum(positions[i]) == 0:
            for j in range(len(positions[i])):
                positions[i][j] = 1 if positions[i][j] == -1 else 0.5
        else:
            for j in range(len(positions[i])):
                positions[i][j] = 1 if positions[i][j] == 1 else 0.5

    new_labels = np.zeros((len(labels), 2))
    for i in range(len(labels)):
        l = np.where(labels[i] == max(labels[i]))[0][0]
        coord_best_move = (l - (l // 15) * 15, l // 15)
        new_labels[i][0], new_labels[i][1] = coord_best_move

    indices_0 = np.random.permutation(positions.shape[0])
    training_data = positions[indices_0]
    training_output = new_labels[indices_0]

    x_val = training_data[:1000]
    partial_x_train = training_data[1000:]
    y_val = training_output[:1000]
    partial_y_train = training_output[1000:]

    training_model, prediction_model = build_model()

    lr_scheduler = tf.keras.callbacks.LearningRateScheduler(create_schedule_lr(training_model)) #простой вариант
    # patience = 5  # количество эпох, которые нужно ждать перед изменением lr
    # lr_scheduler = tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss ',
    #                                 patience=patience,
    #                                 factor=0.5,
    #                                 min_lr=0.001)

    #Сохранение автоматически
    # checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    #     filepath=r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\best_mode_auto.keras',
    #     monitor='val_loss',
    #     verbose=1,
    #     save_best_only=True,
    #     mode='min'
    # )

    #сохранение весов
    checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
        filepath=r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\best_weights.weights.h5',
        monitor='val_loss',
        verbose=1,
        save_best_only=True,
        save_weights_only=True,
        mode='min'
    )

    history = training_model.fit([partial_x_train, partial_y_train],
                        partial_y_train,
                        epochs=100,
                        batch_size=256,
                        validation_data=([x_val, y_val], y_val),
                        callbacks=[checkpoint_callback, lr_scheduler])

    prediction_model.load_weights(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\best_weights.weights.h5')
    prediction_model.save(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\best_prediction_model.keras')

    #Сохранение вручную
    # best_model = tf.keras.models.load_model(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\neural_network\best_model_manually.keras', custom_objects={'CustomLossLayer': CustomLossLayer})
    # best_vall_loss = best_model.validation([x_val, y_val], y_val)
    #
    # num_epochs = 3
    # for epoch in range(num_epochs):
    #     history = model.fit([partial_x_train, partial_y_train],
    #                         partial_y_train,
    #                         epochs=1,
    #                         batch_size=256,
    #                         validation_data=([x_val, y_val], y_val))
    #
    #     if True:#history.history["vall_loss"] < best_vall_loss:
    #         best_vall_loss = history.history['val_loss']
    #         model.save('neural_network/best_model_manually.keras')


    loss = history.history["loss"]
    val_loss = history.history["val_loss"]
    epochs = range(1, len(loss) + 1)
    plt.plot(epochs, loss, "bo", label="Потери на этапе обучения")
    plt.plot(epochs, val_loss, "b", label="Потери на этапе проверки")
    plt.title("Потери на этапах обучения и проверки")
    plt.xlabel("Эпохи")
    plt.ylabel("Потери")
    plt.legend()
    plt.show()

    # plt.clf()
    # acc = history.history["accuracy"]
    # val_acc = history.history["val_accuracy"]
    # plt.plot(epochs, acc, "bo", label="Точность на этапе обучения")
    # plt.plot(epochs, val_acc, "b", label="Точность на этапе проверки")
    # plt.title("Точность на этапах обучения и проверки")
    # plt.xlabel("Эпохи")
    # plt.ylabel("Точность")
    # plt.legend()
    # plt.show()




def build_model():
    # model = keras.Sequential([
    #                       layers.Dense(2048, activation="relu"),
    #     layers.Dense(2048, activation="relu"),
    #     layers.Dense(1024, activation="relu"),
    #     layers.Dense(1024, activation="relu"),
    #                       layers.Dense(2, activation='linear')
    #       ])
    #model.compile(optimizer="adam", loss="mean_absolute_error", metrics=["mean_absolute_error"])

    input_layer = Input(shape=(225,), name="position")
    true_output = Input(shape=(2,), name="coords")

    layer = layers.Dense(2048, activation="relu")(input_layer)
    #layer = layers.Dense(1024, activation="relu")(layer)
    #layer = layers.Dense(1024, activation="relu")(layer)

    predict_output = layers.Dense(2, activation= custom_activation)(layer)

    loss_layer = CustomLossLayer()([true_output, predict_output, input_layer])

    training_model  = keras.models.Model(inputs=[input_layer, true_output], outputs=loss_layer)
    training_model .compile(optimizer='adam')

    prediction_model = keras.models.Model(inputs=input_layer, outputs=predict_output)

    return training_model, prediction_model

def custom_activation(x):
    return tf.sigmoid(x) * 15

class CustomLossLayer(Layer):
    def __init__(self, **kwargs):
        super(CustomLossLayer, self).__init__(**kwargs)

    def call(self, inputs):
        y_true, y_pred, positions = inputs

        batch_size = tf.shape(positions)[0]
        board_width = 15

        base_loss = tf.reduce_mean(tf.square(y_pred - y_true), axis=-1)

        pred_x = tf.cast(y_pred[:, 0], tf.int32)
        pred_y = tf.cast(y_pred[:, 1], tf.int32)

        pred_index = pred_y * board_width + pred_x

        batch_indices = tf.range(batch_size, dtype=tf.int32)
        gather_indices = tf.stack([batch_indices, pred_index], axis=1)

        pred_occupancy = tf.gather_nd(positions, gather_indices)

        overlap_penalty = tf.cast(pred_occupancy != 0, tf.float32)

        total_loss = base_loss * overlap_penalty * 4 + base_loss

        self.add_loss(total_loss)

        return y_pred

    def get_config(self):
        config = super(CustomLossLayer, self).get_config()
        return config

    @classmethod
    def from_config(cls, config):
        return cls(**config)


# def schedule_lr(epoch):
#     if epoch < 5:
#         return 0.001
#     elif epoch < 10:
#         return 0.0005
#     else:
#         return 0.0001

def create_schedule_lr(model):
    def schedule_lr(epoch, lr):
        logs = model.history.history
        if len(logs) == 0:
            return 0.001

        val_accuracy = logs['val_loss'][-1]
        if val_accuracy > 0.3 and val_accuracy < 0.35 and False:
            return 0.1
        else:
            return 0.001
    return schedule_lr




#generation_position_and_save(10000, 50)


generation_labels()


#show_positions()


#train_neural_network()

