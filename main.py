import pygame as pg
import pygame_gui as pg_gui
from ptext import drawbox, draw
from sys import exit
from numpy import zeros

pg.init()


def main():
    global BOARD, ROWS, COLUMNS, WIN_COUNT, WIDTH, HEIGHT, SCREEN, SQUARE_SIZE, RADIUS, CLOCK, MANAGER, FPS, TOTAL_MOVES

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

    # Clock
    CLOCK = pg.time.Clock()

    # Manager for pugame gui
    MANAGER = pg_gui.UIManager((WIDTH, HEIGHT))

    # Board
    values = get_input()
    ROWS, COLUMNS, WIN_COUNT = values["rows"], values["columns"], values["win_count"]
    BOARD = zeros((ROWS, COLUMNS))


    # SCREEN
    WIDTH = SQUARE_SIZE * COLUMNS
    HEIGHT = SQUARE_SIZE * (ROWS + 1)
    SCREEN = pg.display.set_mode((WIDTH, HEIGHT))

    # Game Logic Variables
    player = -1
    move = 0
    TOTAL_MOVES = ROWS * COLUMNS
    game_over = False


    # Game Loop
    draw_board()
    while True:

        # Game
        if not game_over and move < TOTAL_MOVES:
            player = move % 2 + 1

            for event in pg.event.get():
                
                # Stop Game
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                # Player move
                if event.type == pg.MOUSEBUTTONDOWN:
                    column = event.pos[0] // 100
                    
                    if BOARD[0][column] == 0:
                        player_move(player, column)
                        move += 1
                    
                    draw_board()
                    
                    if check_win(player): game_over = True

                piece_animation(player)

        # End Screen
        else:
            for event in pg.event.get():

                # Stop Game
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            # Winner
            display_winner(player, move)


        pg.display.flip()
        CLOCK.tick(FPS)


def check_win(player):

    # Temp variables
    highlight_width = 13
    flag = False
    limit = WIN_COUNT - 1

    # Check Vertical |
    for i in range(COLUMNS):
        for j in range(ROWS - limit):

            count = sum([1 for k in range(WIN_COUNT) if BOARD[j + k][i] == player])

            # If win, highlight it
            if count == WIN_COUNT:
                for l in range(1, WIN_COUNT + 1):
                    pg.draw.circle(SCREEN, "green", (SQUARE_SIZE * i + SQUARE_SIZE/2, SQUARE_SIZE * (l + j) + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True
    
    # Check Horizontal -
    for i in range(ROWS):
        for j in range(COLUMNS - limit):
            
            count = sum([1 for k in range(WIN_COUNT) if BOARD[i][j + k] == player])

            # If win, highlight it
            if count == WIN_COUNT:
                for l in range(WIN_COUNT):
                    pg.draw.circle(SCREEN, "green", (SQUARE_SIZE * (l + j) + SQUARE_SIZE/2, (i + 1) * SQUARE_SIZE + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True
            
    # Check Diagonal-Right /
    for i in range(limit, ROWS):
        for j in range(COLUMNS - limit):
            
            count = sum([1 for k in range(WIN_COUNT) if BOARD[i - k][j + k] == player])

            # If win, highlight it
            if count == WIN_COUNT:
                for l in range(WIN_COUNT):
                    pg.draw.circle(SCREEN, "green", (SQUARE_SIZE * (l + j) + SQUARE_SIZE/2, SQUARE_SIZE * (-l + i + 1) + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True
            
    # Check Diagonal-Left \
    for i in range(limit, ROWS):
        for j in range(limit, COLUMNS):
            
            count = sum([1 for k in range(WIN_COUNT) if BOARD[i - k][j - k] == player])

            # If win, highlight it
            if count == WIN_COUNT:
                for l in range(WIN_COUNT):
                    pg.draw.circle(SCREEN, "green", (SQUARE_SIZE * (-l + j) + SQUARE_SIZE/2, SQUARE_SIZE * (-l + i + 1) + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True

    return flag

def display_winner(player, move):
    
    # Clear Top Row
    pg.draw.rect(SCREEN, "black", (0, 0, WIDTH, SQUARE_SIZE))

    # Check for Tie
    if move >= TOTAL_MOVES:
        text = "TIE!!!"
        font_color = "white"

    # Winner
    else:
        text = f'Player {player} WON!!!'
        font_color = "red" if player == 1 else "yellow"

    # Display winner
    drawbox (
        text = text,
        rect = (0, 2.5, WIDTH, SQUARE_SIZE),
        color = font_color,
        align = "center"
    )

def draw_board():
    for r in range(ROWS):
        for c in range(COLUMNS):

            # Draw Square
            pg.draw.rect(SCREEN, "blue", (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Draw Circle Based on Player
            if BOARD[r][c] == 1:
                pg.draw.circle(SCREEN, "red",
                (c * SQUARE_SIZE + SQUARE_SIZE / 2, r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2), RADIUS)
            
            elif BOARD[r][c] == 2:
                pg.draw.circle(SCREEN, "yellow",
                (c * SQUARE_SIZE + SQUARE_SIZE / 2, r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2), RADIUS)

            else:
                pg.draw.circle(SCREEN, "black",
                (c * SQUARE_SIZE + SQUARE_SIZE / 2, r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2), RADIUS)

def get_input():

    # Texts on the Customization
    texts = {
        "title_text": 'Connect 4 Customization',
        "instructions_text": 'Default Values Are Already Selected',
        "row_text": 'Number of Rows:',
        "column_text": 'Number of Columns:',
        "win_count_text": 'Number of Pieces in a Row to Win:'
    }

    # Max Size of BOARD
    max_window_size = max(pg.display.get_desktop_sizes())
    max_rows = max_window_size[1] // SQUARE_SIZE
    max_columns = max_window_size[0] // SQUARE_SIZE
    
    # Dropdown variables
    dropdown_x = WIDTH // 2 + SQUARE_SIZE
    dropdown_y = SQUARE_SIZE * 2 - 25
    dropdown_width, dropdown_height = 75, 50

    # Dropdowns
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
    max_win = max(int(row_dropdown.selected_option), int(column_dropdown.selected_option))
    win_count_dropdown = pg_gui.elements.UIDropDownMenu (
        options_list = [str(i) for i in range(1, max_win + 1)],
        starting_option = str(WIN_COUNT),
        manager = MANAGER,
        relative_rect = pg.Rect(dropdown_x + (SQUARE_SIZE * 1.4), dropdown_y + SQUARE_SIZE * 2, dropdown_width, dropdown_height),
        object_id = "#win_count_dropdown"
    )

    # Play
    submit_button = pg_gui.elements.UIButton (
        relative_rect = pg.Rect((WIDTH // 2 - 50, HEIGHT - SQUARE_SIZE * 2), (100, 50)),
        manager = MANAGER,
        object_id = "#submit",
        text = "PLAY"
    )

    # Game Loop
    while True:

        # Defualt Values
        return_values = {
            "rows": ROWS,
            "columns": COLUMNS,
            "win_count": WIN_COUNT
            }

        # Refresh Rate 
        UI_REFRESH_RATE = CLOCK.tick(FPS) / 1000

        for event in pg.event.get():

            # Quit Game
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            # If Dropdown Changed, Update the Win Count
            if event.type == pg_gui.UI_DROP_DOWN_MENU_CHANGED:
                event_id = event.ui_object_id
                
                if event_id in ["#row_dropdown", "#column_dropdown"]:
                    win_count_dropdown.kill()
                    max_win = max(int(row_dropdown.selected_option), int(column_dropdown.selected_option))
                    win_count_dropdown = pg_gui.elements.UIDropDownMenu (
                        options_list = [str(i) for i in range(1, max_win + 1)],
                        starting_option = str(WIN_COUNT) if WIN_COUNT <= int(row_dropdown.selected_option) or WIN_COUNT <= int(column_dropdown.selected_option) else str(max_win),
                        manager = MANAGER,
                        relative_rect = pg.Rect(dropdown_x + (SQUARE_SIZE * 1.4), dropdown_y + SQUARE_SIZE * 2, dropdown_width, dropdown_height),
                        object_id = "#win_count_dropdown"
                )

            # If Submitted
            if submit_button.check_pressed():
                return_values["rows"] = int(row_dropdown.selected_option)
                return_values["columns"] = int(column_dropdown.selected_option)
                return_values["win_count"] = int(win_count_dropdown.selected_option)

                return return_values

            MANAGER.process_events(event)
        
        # Pygame GUI manager
        MANAGER.update(UI_REFRESH_RATE)

        # Background
        SCREEN.fill("grey70")

        # Draw The texts to SCREEN, draw() from ptext.py
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

        # Draw GUI
        MANAGER.draw_ui(SCREEN)

        pg.display.flip()
        CLOCK.tick(FPS)

def piece_animation(player):

    # Get Current Mouse Position
    posx = pg.mouse.get_pos()[0]

    # Clear Top Row
    pg.draw.rect(SCREEN, "black", (0, 0, WIDTH, SQUARE_SIZE))
    
    # Player Color
    color = "red" if player == 1 else "yellow"

    # Draw Piece
    pg.draw.circle(SCREEN, color, (posx, SQUARE_SIZE / 2), RADIUS)

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


if __name__ == "__main__":
    main()
