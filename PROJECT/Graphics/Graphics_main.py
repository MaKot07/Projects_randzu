import sys
import pygame
import numpy as np


black = -1
white = 1
cell_qty = 14
cell_size = 40
cell_size_ramka = 42
colors = (234, 237, 204)
chip_radius = 13

button_color = (255, 165, 0)
button_hover_color = (255, 140, 0)
text_color = (255, 255, 255)


board_shift = 120
WHITE = (255, 255, 255)
RED = (225, 0, 50)
GREEN = (0, 225, 0)
BLUE = (0, 0, 225)
BLACK = (10, 10, 10)
GRAY = (92, 87, 87)
GLOW = (255, 215, 0, 128)

class Game_Graphics:

    __cell_qty = 14
    __cell_size = 40
    __cell_size_ramka = 42
    __colors = (234, 237, 204)
    __board_shift = 120


    def __init__(self, number_of_movies, now_coord_all_move_and_color = np.empty(0, dtype=np.int8)):
        self.__now_coord_all_move_and_color = now_coord_all_move_and_color
        self.__number_of_movies = number_of_movies

    def set_number_move(self):
        self.__number_of_movies += 1

    def give_number_move(self):
        return self.__number_of_movies


    def draw_all_game(self, win_color, buttons,  label_chip=(-1,-1)):
        self.draw_screen()
        self.draw_main_board()
        if len(self.__now_coord_all_move_and_color) > 0:
            self.draw_all_shashky(label_chip)

        self.text_output_number_of_movies()
        if win_color != 0:
            self.text_win(win_color)

        for button in buttons:
            button.draw(screen)

        pygame.display.update()
        # pygame.time.delay(120)


    #@staticmethod
    def draw_main_board(self):
        for y in range(Game_Graphics.__cell_qty):
            for x in range(Game_Graphics.__cell_qty):
                pygame.draw.rect(screen, colors, (x * (Game_Graphics.__cell_size + 2) + Game_Graphics.__board_shift, y * (Game_Graphics.__cell_size + 2) + Game_Graphics.__board_shift, Game_Graphics.__cell_size, Game_Graphics.__cell_size))
                pygame.draw.rect(screen, BLACK, (x * Game_Graphics.__cell_size_ramka + Game_Graphics.__board_shift, y * Game_Graphics.__cell_size_ramka + Game_Graphics.__board_shift, Game_Graphics.__cell_size_ramka, Game_Graphics.__cell_size_ramka),2)


    def draw_all_shashky(self, label_chip):
        last_move = self.__now_coord_all_move_and_color[-1]
        pygame.draw.circle(screen, GLOW,
                           (last_move[0] * cell_size_ramka + board_shift, last_move[1] * cell_size_ramka + board_shift),
                           chip_radius+3)

        for index_x_rect, index_y_rect, color_player in self.__now_coord_all_move_and_color:
            if color_player == black:
                pygame.draw.circle(screen, BLACK, (index_x_rect * cell_size_ramka + board_shift, index_y_rect * cell_size_ramka + board_shift), chip_radius)
            else:
                pygame.draw.circle(screen, WHITE, (index_x_rect * cell_size_ramka + board_shift, index_y_rect * cell_size_ramka + board_shift), chip_radius)


        if label_chip != (-1,-1):
            pygame.draw.circle(screen, (0, 225, 0), (label_chip[0] * cell_size_ramka + board_shift, label_chip[1] * cell_size_ramka + board_shift), chip_radius)

    #@staticmethod
    # def draw_screen(self):
    #     screen.fill((155, 155, 155))


    def draw_screen(self):
        background_image = pygame.image.load(r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\Graphics\images\table1_middle.jpg')
        screen.blit(background_image, (0, 0))

    #@staticmethod
    def text_output_number_of_movies(self):
        text = f'Moves made: {self.__number_of_movies}'
        pygame.draw.rect(screen, button_color, pygame.Rect(120, 750, 290, 70), border_radius=10)
        font = pygame.font.Font(r"C:\Users\lehas\GitHub\Projects_randzu\PROJECT\Graphics\fonts\PoetsenOne-Regular.ttf",36)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=pygame.Rect(120, 750, 290, 70).center)
        screen.blit(text_surface, text_rect)

        # text_move = f1.render(f'Ходы: {coord_all_move_and_color}', 1, BLACK)
        # screen.blit(text_move, (100, 750))

    #@staticmethod
    # def draw_button_newgame(self):
    #     pygame.draw.rect(screen, (40, 224, 132), (700, 180, 140, 70))
    #     text = f1.render(f'NEW GAME', 1, BLACK)
    #     screen.blit(text, (700, 200))


    def text_win(self, color):
        if color == black:
            text = f'The game is over, black wins'
            pygame.draw.rect(screen, button_color, pygame.Rect(200, 300, 520, 70), border_radius=10)
            font = pygame.font.Font(
                r"C:\Users\lehas\GitHub\Projects_randzu\PROJECT\Graphics\fonts\PoetsenOne-Regular.ttf", 36)
            text_surface = font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=pygame.Rect(200, 300, 520, 70).center)
            screen.blit(text_surface, text_rect)
        else:
            text = f'The game is over, white wins!!'
            pygame.draw.rect(screen, button_color, pygame.Rect(200, 300, 520, 70), border_radius=10)
            font = pygame.font.Font(
                r"C:\Users\lehas\GitHub\Projects_randzu\PROJECT\Graphics\fonts\PoetsenOne-Regular.ttf", 36)
            text_surface = font.render(text, True, text_color)
            text_rect = text_surface.get_rect(center=pygame.Rect(200, 300, 520, 70).center)
            screen.blit(text_surface, text_rect)

    def change_color_player(self, color_player):
        if color_player == black:
            color_player = white
        else:
            color_player = black

        return color_player

    def set_coord(self, x, y, color):
        if self.__now_coord_all_move_and_color.size == 0:
            self.__now_coord_all_move_and_color = np.array([[x,y,color]])
        else:
            self.__now_coord_all_move_and_color = np.vstack((self.__now_coord_all_move_and_color, np.array([[x, y, color]])))

class Button:
    def __init__(self, name, x, y, width, height, text):
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.color = button_color
        self.hover_color = button_hover_color
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        font = pygame.font.Font(r"C:\Users\lehas\GitHub\Projects_randzu\PROJECT\Graphics\fonts\PoetsenOne-Regular.ttf", 36)
        text_surface = font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.color = self.hover_color
        else:
            self.color = button_color


def color_choice():
    passive_buttons = [
        Button("text_choice", 270, 200, 300, 70, "Choose a color")
    ]

    dynamic_buttons = [
        Button("choice_white", 220, 310, 200, 70, "white"),
        Button("choice_black", 420, 310, 200, 70, "black")
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in dynamic_buttons:
                    if button.rect.collidepoint(event.pos):
                        if button.name == "choice_white":
                            return white
                        if button.name == "choice_black":
                            return black


        mouse_pos = pygame.mouse.get_pos()

        for button in dynamic_buttons:
            button.check_hover(mouse_pos)

        background_image = pygame.image.load(
            r'C:\Users\lehas\GitHub\Projects_randzu\PROJECT\Graphics\images\table1_middle.jpg')
        screen.blit(background_image, (0, 0))

        for button in dynamic_buttons+passive_buttons:
            button.draw(screen)

        pygame.display.flip()

def give_coord(events):
    x, y = events.pos
    x, y = x - board_shift, y - board_shift
    return x,y

def give_coord_rect(events):
    x,y = give_coord(events)

    index_x_rect = round(x / cell_size_ramka)
    index_y_rect = round(y / cell_size_ramka)

    return index_x_rect,index_y_rect

def check_in_2D_array(check_array, check_in_array):
    for i, sub in enumerate(check_in_array):
        if np.array_equal(sub, check_array):
            return True
    return False




pygame.init()
screen = pygame.display.set_mode((900, 850))
pygame.display.set_caption("MY game")

# icon = pygame.image.load("images/icon.png")
# pygame.display.set_icon(icon)


f1 = pygame.font.Font(None, 36)







