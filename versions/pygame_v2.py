import pygame as pg
import pygame_gui as pg_gui
from sys import exit
from numpy import zeros

def draw_board():
    for r in range(ROWS):
        for c in range(COLUMNS):

            # Draw square
            pg.draw.rect(SCREEN, "blue", (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Draw circle
            if BOARD[r][c] == 1:
                pg.draw.circle(SCREEN, "red",
                (c * SQUARE_SIZE + SQUARE_SIZE / 2, r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2), RADIUS)
            
            elif BOARD[r][c] == 2:
                pg.draw.circle(SCREEN, "yellow",
                (c * SQUARE_SIZE + SQUARE_SIZE / 2, r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2), RADIUS)

            else:
                pg.draw.circle(SCREEN, "black",
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
                    pg.draw.circle(SCREEN, "green", (SQUARE_SIZE * i + SQUARE_SIZE/2, SQUARE_SIZE * (l + j) + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True
    
    # Check Horizontal -
    for i in range(ROWS):
        for j in range(COLUMNS - limit):
            
            count = sum([1 for k in range(WIN_COUNT) if BOARD[i][j + k] == player])

            if count == WIN_COUNT:
                for l in range(WIN_COUNT):
                    pg.draw.circle(SCREEN, "green", (SQUARE_SIZE * (l + j) + SQUARE_SIZE/2, (i + 1) * SQUARE_SIZE + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True
            
    # Check Diagonal-Right /
    for i in range(limit, ROWS):
        for j in range(COLUMNS - limit):
            
            count = sum([1 for k in range(WIN_COUNT) if BOARD[i - k][j + k] == player])

            if count == WIN_COUNT:
                for l in range(WIN_COUNT):
                    pg.draw.circle(SCREEN, "green", (SQUARE_SIZE * (l + j) + SQUARE_SIZE/2, SQUARE_SIZE * (-l + i + 1) + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True
            
    # Check Diagonal-Left \
    for i in range(limit, ROWS):
        for j in range(limit, COLUMNS):
            
            count = sum([1 for k in range(WIN_COUNT) if BOARD[i - k][j - k] == player])

            if count == WIN_COUNT:
                for l in range(WIN_COUNT):
                    pg.draw.circle(SCREEN, "green", (SQUARE_SIZE * (-l + j) + SQUARE_SIZE/2, SQUARE_SIZE * (-l + i + 1) + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True

    return flag

def get_input():
    
    font = pg.font.Font(None, 50)

    title_surf = font.render('Connect 4 Customization', True, "black")
    title_rect = title_surf.get_rect(center = (WIDTH / 2, SQUARE_SIZE / 2))

    instructions_surf = font.render('Leave it Blank for Default Values', True, "black")
    instructions_rect =  instructions_surf.get_rect(center = (WIDTH / 2, SQUARE_SIZE + 25))

    row_surf = font.render('Number of Rows:', True, "black")
    row_rect = row_surf.get_rect(center = (WIDTH / 2 - 50, HEIGHT / 2 - SQUARE_SIZE))
    input_row = pg_gui.elements.UITextEntryLine(relative_rect=pg.Rect((row_rect.right + 10, row_rect.top - 7), (50, 50)), manager=MANAGER, object_id="#row")
    input_row.set_allowed_characters('numbers')
    input_row.set_forbidden_characters('letters')
    input_row.set_text_length_limit(2)

    col_surf = font.render('Number of Column:', True, "black")
    col_rect = col_surf.get_rect(center = (WIDTH / 2 - 50, HEIGHT / 2))
    input_col = pg_gui.elements.UITextEntryLine(relative_rect=pg.Rect((col_rect.right + 10, col_rect.top - 7), (50, 50)), manager=MANAGER, object_id="#col")
    input_col.set_allowed_characters('numbers')
    input_col.set_forbidden_characters('letters')
    input_col.set_text_length_limit(2)

    win_surf = font.render('Number of Pieces in a Row to Win:', True, "black")
    win_rect = win_surf.get_rect(center = (WIDTH / 2 - 25, HEIGHT / 2 + SQUARE_SIZE))
    input_win = pg_gui.elements.UITextEntryLine(relative_rect=pg.Rect((win_rect.right + 10, win_rect.top - 7), (50, 50)), manager=MANAGER, object_id="#win")
    input_win.set_allowed_characters('numbers')
    input_win.set_forbidden_characters('letters')
    input_win.set_text_length_limit(2)

    submit_button = pg_gui.elements.UIButton(
        relative_rect=pg.Rect((WIDTH / 2 - 50, HEIGHT - SQUARE_SIZE * 1.5), (100, 50)),
        manager=MANAGER, object_id="submit", text="SUBMIT")

    while True:

        return_values = {"rows": ROWS, "columns": COLUMNS, "win_count": WIN_COUNT}

        UI_REFRESH_RATE = CLOCK.tick(fps) / 1000

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            MANAGER.process_events(event)

        if submit_button.check_pressed():
            row = input_row.get_text()
            col = input_col.get_text()
            win = input_win.get_text()
            if row: return_values["rows"] = int(row)
            if col: return_values["columns"] = int(col)
            if win: return_values["win_count"] = int(win)

            return return_values
        
        MANAGER.update(UI_REFRESH_RATE)

        SCREEN.fill("darkgrey")
        SCREEN.blit(title_surf, title_rect)
        SCREEN.blit(instructions_surf, instructions_rect)
        SCREEN.blit(row_surf, row_rect)
        SCREEN.blit(col_surf, col_rect)
        SCREEN.blit(win_surf, win_rect)

        MANAGER.draw_ui(SCREEN)

        pg.display.flip()


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
WIDTH = SQUARE_SIZE * COLUMNS
HEIGHT = SQUARE_SIZE * (ROWS + 1)
window_size = max(pg.display.get_desktop_sizes())

SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Connect 4')
pg.display.set_icon(pg.image.load('graphics/CS50_cat.png').convert_alpha())

# Clock
fps = 60
CLOCK = pg.time.Clock()

# Manager for pugame gui
MANAGER = pg_gui.UIManager((WIDTH, HEIGHT))

values = get_input()
ROWS, COLUMNS, WIN_COUNT = values["rows"], values["columns"], values["win_count"]
WIDTH = SQUARE_SIZE * COLUMNS
HEIGHT = SQUARE_SIZE * (ROWS + 1)
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))

# Board
BOARD = zeros((ROWS, COLUMNS))
draw_board()

while True:
    if not game_over and move < total_moves:
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
            
            pg.draw.rect(SCREEN, "black", (0, 0, WIDTH, SQUARE_SIZE))
            if move % 2 == 0:
                pg.draw.circle(SCREEN, "red", (posx, SQUARE_SIZE / 2), RADIUS)
            
            else:
                pg.draw.circle(SCREEN, "yellow", (posx, SQUARE_SIZE / 2), RADIUS)

    else:
        for event in pg.event.get():
            # Stop Game
            if event.type == pg.QUIT:
                pg.quit()
                exit()

        pg.draw.rect(SCREEN, "black", (0, 0, WIDTH, SQUARE_SIZE))

        font = pg.font.Font(None, 125)

        font_color = "red" if player == 1 else "yellow"

        font_surf = font.render(f'Player {player} WON!!!', False, font_color)
        font_rect = font_surf.get_rect(center = (WIDTH / 2, SQUARE_SIZE / 2))

        SCREEN.blit(font_surf, font_rect)
    
    pg.display.flip()
    CLOCK.tick(fps)

