import pygame as pg
from sys import exit
import numpy as np

def draw_board():
    for r in range(ROWS):
        for c in range(COLUMNS):

            # Draw square
            pg.draw.rect(SCREEN, pg.Color('blue'), (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Draw circle
            if BOARD[r][c] == 1:
                pg.draw.circle(SCREEN, pg.Color('red'),
                (c * SQUARE_SIZE + SQUARE_SIZE / 2, r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2), RADIUS)
            
            elif BOARD[r][c] == 2:
                pg.draw.circle(SCREEN, pg.Color('yellow'),
                (c * SQUARE_SIZE + SQUARE_SIZE / 2, r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2), RADIUS)

            else:
                pg.draw.circle(SCREEN, pg.Color('black'),
                (c * SQUARE_SIZE + SQUARE_SIZE / 2, r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2), RADIUS)

def player_move(player, column):
    # Check each row in column
    for i in range(ROWS - 1):

        # Next row is not empty, then place move here
        if BOARD[i + 1][column] != 0:
            BOARD[i][column] = player
            break

        # Last row
        elif i + 1 == ROWS - 1:
            BOARD[i + 1][column] = player
            break

def check_win(player):
    neon_green = pg.Color('green')
    highlight_width = 13

    # Temp variable
    flag = False
    limit = WIN_COUNT - 1

    # Check Vertical |
    for i in range(COLUMNS):
        for j in range(ROWS - limit):

            count = sum([1 for k in range(WIN_COUNT) if BOARD[j + k][i] == player])

            if count == WIN_COUNT:
                for l in range(1, WIN_COUNT + 1):
                    pg.draw.circle(SCREEN, pg.Color(neon_green), (SQUARE_SIZE * i + SQUARE_SIZE/2, SQUARE_SIZE * (l + j) + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True
    
    # Check Horizontal -
    for i in range(ROWS):
        for j in range(COLUMNS - limit):
            
            count = sum([1 for k in range(WIN_COUNT) if BOARD[i][j + k] == player])

            if count == WIN_COUNT:
                for l in range(WIN_COUNT):
                    pg.draw.circle(SCREEN, pg.Color(neon_green), (SQUARE_SIZE * (l + j) + SQUARE_SIZE/2, (i + 1) * SQUARE_SIZE + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True
            
    # Check Diagonal-Right /
    for i in range(limit, ROWS):
        for j in range(COLUMNS - limit):
            
            count = sum([1 for k in range(WIN_COUNT) if BOARD[i - k][j + k] == player])

            if count == WIN_COUNT:
                for l in range(WIN_COUNT):
                    pg.draw.circle(SCREEN, pg.Color(neon_green), (SQUARE_SIZE * (l + j) + SQUARE_SIZE/2, SQUARE_SIZE * (-l + i + 1) + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True
            
    # Check Diagonal-Left \
    for i in range(limit, ROWS):
        for j in range(limit, COLUMNS):
            
            count = sum([1 for k in range(WIN_COUNT) if BOARD[i - k][j - k] == player])

            if count == WIN_COUNT:
                for l in range(WIN_COUNT):
                    pg.draw.circle(SCREEN, pg.Color(neon_green), (SQUARE_SIZE * (-l + j) + SQUARE_SIZE/2, SQUARE_SIZE * (-l + i + 1) + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True

    return flag


pg.init()

# Global Constants
ROWS, COLUMNS = 6, 7
WIN_COUNT = 4
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE / 2 - 5

player = -1
move = 0
total_moves = ROWS * COLUMNS
game_over = False

# SCREEN
width = SQUARE_SIZE * COLUMNS
height = SQUARE_SIZE * (ROWS + 1)
window_size = max(pg.display.get_desktop_sizes())

SCREEN = pg.display.set_mode((width, height))
pg.display.set_caption('Connect 4')
#pg.display.set_icon(pg.image.load('graphics/CS50_cat.png').convert_alpha())

# Font
font = pg.font.SysFont('Fixedys Regular', 125)

# Board
BOARD = np.zeros((ROWS, COLUMNS))
draw_board()

while not game_over and move < total_moves:
    for event in pg.event.get():
        
        # Stop Game
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        # Player move
        if event.type == pg.MOUSEBUTTONDOWN:
            column = event.pos[0] // 100
            player = move % 2 + 1

            if BOARD[0][column] == 0:
                player_move(player, column)
                move += 1
            
            draw_board()
            if check_win(player): game_over = True


        posx = pg.mouse.get_pos()[0]
        
        pg.draw.rect(SCREEN, pg.Color('black'), (0, 0, width, SQUARE_SIZE))
        if move % 2 == 0:
            pg.draw.circle(SCREEN, pg.Color('red'), (posx, SQUARE_SIZE / 2), RADIUS)
        
        else:
            pg.draw.circle(SCREEN, pg.Color('yellow'), (posx, SQUARE_SIZE / 2), RADIUS)
        
        pg.display.update()

while game_over:
    for event in pg.event.get():
        
        # Stop Game
        if event.type == pg.QUIT:
            pg.quit()
            exit()

    pg.draw.rect(SCREEN, pg.Color('black'), (0, 0, width, SQUARE_SIZE))

    font_color = pg.Color('red') if player == 1 else pg.Color('yellow')

    font_surf = font.render(f'Player {player} WON!!!', False, font_color)
    font_rect = font_surf.get_rect(center = (width / 2, SQUARE_SIZE / 2))

    SCREEN.blit(font_surf, font_rect)

    pg.display.update()

