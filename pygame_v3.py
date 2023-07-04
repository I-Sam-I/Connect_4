import pygame as pg
import pygame_gui as pg_gui
from ptext import drawbox, draw
from sys import exit
from numpy import zeros

pg.init()

def main():
    global BOARD, ROWS, COLUMNS, WIN_COUNT, WIDTH, HEIGHT, SCREEN, SQUARE_SIZE, RADIUS, CLOCK, MANAGER, FPS

    FPS = 60
        
    # Global Constants
    ROWS, COLUMNS = 6, 7
    WIN_COUNT = 4
    SQUARE_SIZE = 100
    RADIUS = SQUARE_SIZE / 2 - 5

    # SCREEN
    WIDTH = SQUARE_SIZE * COLUMNS
    HEIGHT = SQUARE_SIZE * (ROWS + 1)

    SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Connect 4')
    pg.display.set_icon(pg.image.load('graphics/CS50_cat.png').convert_alpha())

    # Clock
    CLOCK = pg.time.Clock()

    # Manager for pugame gui
    MANAGER = pg_gui.UIManager((WIDTH, HEIGHT))


    values = get_input()

    ROWS, COLUMNS, WIN_COUNT = values["rows"], values["columns"], values["win_count"]

    TOTAL_MOVES = ROWS * COLUMNS

    BOARD = zeros((ROWS, COLUMNS))


    # SCREEN
    WIDTH = SQUARE_SIZE * COLUMNS
    HEIGHT = SQUARE_SIZE * (ROWS + 1)
    SCREEN = pg.display.set_mode((WIDTH, HEIGHT))

    player = -1
    move = 0
    TOTAL_MOVES = ROWS * COLUMNS
    game_over = False

    draw_board()
    while True:
        if not game_over and move < TOTAL_MOVES:
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

            if move >= TOTAL_MOVES: text = "TIE!!!"; font_color = "white"
            else: text = f'Player {player} WON!!!'; font_color = "red" if player == 1 else "yellow"

            drawbox(text, (0, 2.5, WIDTH, SQUARE_SIZE), color=font_color, align="center")


        pg.display.flip()
        CLOCK.tick(FPS)

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
            return

    # Last row
    BOARD[ROWS - 1][column] = player
    return

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

    texts = {
        "title_text": 'Connect 4 Customization',
        "instructions_text": 'Default Values Are Already Selected',
        "row_text": 'Number of Rows:',
        "column_text": 'Number of Column:',
        "win_count_text": 'Number of Pieces in a Row to Win:'
    }
    
    dropdown_x = WIDTH // 2 + SQUARE_SIZE
    dropdown_y = SQUARE_SIZE * 2 - 25
    dropdown_width, dropdown_height = 75, 50

    max_window_size = max(pg.display.get_desktop_sizes())
    max_rows = max_window_size[1] // SQUARE_SIZE
    max_columns = max_window_size[0] // SQUARE_SIZE

    row_dropdown = pg_gui.elements.UIDropDownMenu (
        options_list = [str(i) for i in range(1, max_rows)],
        starting_option = str(ROWS),
        manager = MANAGER,
        relative_rect = pg.Rect(dropdown_x, dropdown_y, dropdown_width, dropdown_height),
        object_id = "#row_dropdown"
        )

    column_dropdown = pg_gui.elements.UIDropDownMenu (
        options_list = [str(i) for i in range(1, max_columns + 1)],
        starting_option = str(COLUMNS),
        manager = MANAGER,
        relative_rect = pg.Rect(dropdown_x + 20, dropdown_y + SQUARE_SIZE, dropdown_width, dropdown_height),
        object_id=  "#column_dropdown"
        )

    win_count_dropdown = pg_gui.elements.UIDropDownMenu (
        options_list = [str(i) for i in range(1, max(int(row_dropdown.selected_option), int(column_dropdown.selected_option)) + 1)],
        starting_option = str(WIN_COUNT),
        manager = MANAGER,
        relative_rect = pg.Rect(dropdown_x + (SQUARE_SIZE * 1.4), dropdown_y + SQUARE_SIZE * 2, dropdown_width, dropdown_height),
        object_id = "#win_count_dropdown"
        )

    submit_button = pg_gui.elements.UIButton (
        relative_rect=pg.Rect((WIDTH // 2 - 50, HEIGHT - SQUARE_SIZE * 2), (100, 50)),
        manager=MANAGER,
        object_id="#submit",
        text="PLAY"
        )

    while True:

        return_values = {
            "rows": ROWS,
            "columns": COLUMNS,
            "win_count": WIN_COUNT
            }

        UI_REFRESH_RATE = CLOCK.tick(FPS) / 1000

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg_gui.UI_DROP_DOWN_MENU_CHANGED:
                event_id = event.ui_object_id
                if event_id == "#row_dropdown" or event_id == "#column_dropdown":
                    win_count_dropdown.kill()
                    win_count_dropdown = pg_gui.elements.UIDropDownMenu (
                        options_list = [str(i) for i in range(1, max(int(row_dropdown.selected_option), int(column_dropdown.selected_option)) + 1)],
                        starting_option = str(WIN_COUNT),
                        manager = MANAGER,
                        relative_rect = pg.Rect(dropdown_x + (SQUARE_SIZE * 1.4), dropdown_y + SQUARE_SIZE * 2, dropdown_width, dropdown_height),
                        object_id = "#win_count_dropdown"
                )

            if submit_button.check_pressed():
                return_values["rows"] = int(row_dropdown.selected_option)
                return_values["columns"] = int(column_dropdown.selected_option)
                return_values["win_count"] = int(win_count_dropdown.selected_option)

                return return_values

            MANAGER.process_events(event)
        
        MANAGER.update(UI_REFRESH_RATE)

        SCREEN.fill("grey70")

        draw (
            text = texts["title_text"],
            center = (WIDTH // 2, SQUARE_SIZE // 2 - 10),
            fontsize = 75,
            color = "black",
            align = "center",
            underline = True,
            owidth = 0.5, ocolor = "white"
        )

        draw (
            text = texts["instructions_text"],
            center = (WIDTH // 2, SQUARE_SIZE + 10),
            fontsize = 50,
            color = "black",
            align = "center"
        )

        i = 2
        for text in list(texts.values())[2:]:

            draw (
                text = text,
                center = (WIDTH // 2 - SQUARE_SIZE // 2, SQUARE_SIZE * i),
                fontsize = 50,
                color = "black",
                align = "center"
            )

            i += 1

        draw (
            text = "Hello World!",
            center = (WIDTH // 2, HEIGHT - 70),
            fontsize = 25,
            color = "white",
            align = "center"
        )

        MANAGER.draw_ui(SCREEN)

        pg.display.flip()
        CLOCK.tick(FPS)


if __name__ == "__main__":
    main()