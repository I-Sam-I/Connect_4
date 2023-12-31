import pygame as pg
import pygame_gui as pg_gui
from ptext import drawbox, draw
from sys import exit
from numpy import zeros, ndarray
from random import choice


pg.init()


# Global Constants
ROWS, COLUMNS = 6, 7
WIN_COUNT = 4
SQUARE_SIZE = 100
RADIUS = SQUARE_SIZE / 2 - 5

BOARD = zeros((ROWS, COLUMNS), dtype=int)

# SCREEN Dimensions
WIDTH = SQUARE_SIZE * COLUMNS
HEIGHT = SQUARE_SIZE * (ROWS + 1)
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))

# Clock
CLOCK = pg.time.Clock()
FPS = 60

# Manager for pygame gui
MANAGER = pg_gui.UIManager((WIDTH, HEIGHT))


def main():
    global BOARD, ROWS, COLUMNS, WIN_COUNT, WIDTH, HEIGHT

    # Board
    ROWS, COLUMNS, WIN_COUNT, MODE = get_input()
    BOARD = zeros((ROWS, COLUMNS), dtype=int)
    
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
                    
                if MODE == "Player vs Player":
                    if event.type == pg.MOUSEBUTTONDOWN:
                        column = event.pos[0] // 100
                        
                        if BOARD[0][column] == 0:
                            player_move(BOARD, player, column)
                            move += 1
                else:
                    if player == 1:
                        
                        # Player move
                        if event.type == pg.MOUSEBUTTONDOWN:
                            column = event.pos[0] // 100
                            
                            if BOARD[0][column] == 0:
                                player_move(BOARD, player, column)
                                move += 1
                    
                    # AI move
                    elif player == 2:
                        player_move(BOARD, player, best_move(BOARD, player))
                    
                        move += 1
                
                draw_board()  
                if check_win(BOARD, player): game_over = True
            
            piece_animation(player)

        # End Screen
        else:
            for event in pg.event.get():

                # Stop Game
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

            # Winner
            display_winner(player, TOTAL_MOVES, move)


        pg.display.flip()
        CLOCK.tick(FPS)


def analyze_board(board: ndarray, player: int) -> int:
    limit: int = WIN_COUNT - 1
    score: int = 0
    
    # Analyze Center
    center_count = list(board[:, COLUMNS // 2]).count(player)
    score += 15 * center_count
    
        
    # Analyze Horizontal -
    for i in range(ROWS):
        row: list = list(board[i,:])
        for j in range(COLUMNS - limit):
            window: list = row[j:j + WIN_COUNT]
            score += analyze_window(window, player)
    
    # Analyze Vertical |
    for i in range(COLUMNS):
        col: list = list(board[:,i])
        for j in range(ROWS - limit):
            window: list = col[j:j + WIN_COUNT]
            score += analyze_window(window, player)

    # Analyze Diagonal-Right /
    for i in range(ROWS - limit):
        for j in range(COLUMNS - limit):
            window: list = [board[i+k][j+k] for k in range(WIN_COUNT)]
            score += analyze_window(window, player)
            
    # Analyze Diagonal-Left \
    for i in range(ROWS):
        for j in range(COLUMNS - limit):
            window: list = [board[i-k][j+k] for k in range(WIN_COUNT)]
            score += analyze_window(window, player)
    
    return score


def analyze_window(window: list, player: int) -> int:      
    score: int = 0
    player_count: int = window.count(player)
    opp_player: int = 2 if player == 1 else 1
    opp_count: int = window.count(opp_player)
    empty_count: int = window.count(0)
    
    for count in range(WIN_COUNT, 1, -1):
        if player_count == count and empty_count == WIN_COUNT - count:
            if count == WIN_COUNT: score += 10000
            else: score += count * 20
    
    for count in range(WIN_COUNT - 1, 1, -1):
        if opp_count == count and empty_count == WIN_COUNT - count:
            if count == WIN_COUNT - 1: score -= 5000
            else: score -= count * 21
    
    return score


def best_move(board: ndarray, player: int) -> int:
    valid_columns = [c for c in range(COLUMNS) if board[0][c] == 0]
    best_score = -10000000
    best_column: int = choice(valid_columns)
    
    for col in valid_columns:
        temp_board = board.copy()
        player_move(temp_board, player, col)
        score = analyze_board(temp_board, player)
        
        if score > best_score: best_score, best_column = score, col
        
    
    return best_column
        

def check_win(board:ndarray, player: int) -> bool:

    # Temp variables
    highlight_width = 13
    flag = False
    limit = WIN_COUNT - 1

    # Check Vertical |
    for i in range(COLUMNS):
        for j in range(ROWS - limit):

            count: int = [board[j + k][i] for k in range(WIN_COUNT)].count(player)


            # If win, highlight it
            if count == WIN_COUNT:
                for l in range(1, WIN_COUNT + 1):
                    pg.draw.circle(SCREEN, "green", (SQUARE_SIZE * i + SQUARE_SIZE/2, SQUARE_SIZE * (l + j) + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True
    
    # Check Horizontal -
    for i in range(ROWS):
        for j in range(COLUMNS - limit):
            
            count: int = [board[i][j + k] for k in range(WIN_COUNT)].count(player)

            # If win, highlight it
            if count == WIN_COUNT:
                for l in range(WIN_COUNT):
                    pg.draw.circle(SCREEN, "green", (SQUARE_SIZE * (l + j) + SQUARE_SIZE/2, (i + 1) * SQUARE_SIZE + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True
            
    # Check Diagonal-Right /
    for i in range(limit, ROWS):
        for j in range(COLUMNS - limit):
            
            count: int = [board[i - k][j + k] for k in range(WIN_COUNT)].count(player)

            # If win, highlight it
            if count == WIN_COUNT:
                for l in range(WIN_COUNT):
                    pg.draw.circle(SCREEN, "green", (SQUARE_SIZE * (l + j) + SQUARE_SIZE/2, SQUARE_SIZE * (-l + i + 1) + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True
            
    # Check Diagonal-Left \
    for i in range(limit, ROWS):
        for j in range(limit, COLUMNS):
            
            count: int = [board[i - k][j - k] for k in range(WIN_COUNT)].count(player)

            # If win, highlight it
            if count == WIN_COUNT:
                for l in range(WIN_COUNT):
                    pg.draw.circle(SCREEN, "green", (SQUARE_SIZE * (-l + j) + SQUARE_SIZE/2, SQUARE_SIZE * (-l + i + 1) + SQUARE_SIZE/2), RADIUS, highlight_width)
                flag = True

    return flag


def display_winner(player: int, total_moves: int, move: int) -> None:

    # Clear Top Row
    pg.draw.rect(SCREEN, "black", (0, 0, WIDTH, SQUARE_SIZE))

    # Check for Tie
    if move >= total_moves:
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


def draw_board() -> None:
    for r in range(ROWS):
        for c in range(COLUMNS):

            # Draw Square
            pg.draw.rect(SCREEN, "blue", (c * SQUARE_SIZE, SQUARE_SIZE * (r + 1), SQUARE_SIZE, SQUARE_SIZE))

            # Draw Circle Based on Player
            match BOARD[r][c]:
                case 1: circle_color: str = "red"
                case 2: circle_color: str = "yellow"
                case 0: circle_color: str = "black"
            
            pg.draw.circle(SCREEN, circle_color, (SQUARE_SIZE * (c + .5), SQUARE_SIZE * (r + 1.5)), RADIUS)
                

def get_input() -> tuple:
    
    # SCREEN
    SCREEN = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption('Connect 4')

    # Texts on the Customization
    texts = {
        "title_text": 'Connect 4 Customization',
        "instructions_text": 'Default Values Are Already Selected',
        "row_text": 'Number of Rows:',
        "column_text": 'Number of Columns:',
        "win_count_text": 'Number of Pieces in a Row to Win:'
    }

    # Max Size of BOARD
    max_width, max_height = max(pg.display.get_desktop_sizes())
    max_rows = max_height // SQUARE_SIZE
    max_columns = max_width // SQUARE_SIZE
    
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
    
    max_win = min(int(row_dropdown.selected_option), int(column_dropdown.selected_option))
    win_count_dropdown = pg_gui.elements.UIDropDownMenu (
        options_list = [str(i) for i in range(1, max_win + 1)],
        starting_option = str(WIN_COUNT),
        manager = MANAGER,
        relative_rect = pg.Rect(dropdown_x + (SQUARE_SIZE * 1.4), dropdown_y + SQUARE_SIZE * 2, dropdown_width, dropdown_height),
        object_id = "#win_count_dropdown"
    )

    # Mode
    mode_list = pg_gui.elements.UISelectionList(
        relative_rect = pg.Rect((WIDTH // 2 - 100, HEIGHT - SQUARE_SIZE * 2.5), (200, 50)),
        item_list = ["Player vs Player", "Player vs Computer"],
        manager = MANAGER,
        object_id = "#mode"
    )
    
    # Play
    submit_button = pg_gui.elements.UIButton (
        relative_rect = pg.Rect((WIDTH // 2 - 50, HEIGHT - SQUARE_SIZE * 1.75), (100, 50)),
        manager = MANAGER,
        object_id = "#submit",
        text = "PLAY"
    )
    


    # Game Loop
    while True:
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
                    max_win = min(int(row_dropdown.selected_option), int(column_dropdown.selected_option))
                    win_count_dropdown = pg_gui.elements.UIDropDownMenu (
                        options_list = [str(i) for i in range(1, max_win + 1)],
                        starting_option = str(WIN_COUNT) if WIN_COUNT <= int(row_dropdown.selected_option) and WIN_COUNT <= int(column_dropdown.selected_option) else str(max_win),
                        manager = MANAGER,
                        relative_rect = pg.Rect(dropdown_x + (SQUARE_SIZE * 1.4), dropdown_y + SQUARE_SIZE * 2, dropdown_width, dropdown_height),
                        object_id = "#win_count_dropdown"
                )

            # If Submitted
            if submit_button.check_pressed():
                mode = mode_list.get_single_selection()
                if mode:
                    return int(row_dropdown.selected_option), int(column_dropdown.selected_option), int(win_count_dropdown.selected_option), mode

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


def piece_animation(player: int) -> None:

    # Get Current Mouse Position
    posx: float = pg.mouse.get_pos()[0]

    # Clear Top Row
    pg.draw.rect(SCREEN, "black", (0, 0, WIDTH, SQUARE_SIZE))
    
    # Player Color
    color: str = "red" if player == 1 else "yellow"

    # Draw Piece
    pg.draw.circle(SCREEN, color, (posx, SQUARE_SIZE / 2), RADIUS)


def player_move(board: ndarray, player: int, column: int) -> None:
    # Check each row in column
    for i in range(ROWS - 1):

        # Next row is not empty, then place move here
        if board[i + 1][column] != 0:
            board[i][column] = player
            return

    # Last row
    board[ROWS - 1][column] = player
    return


if __name__ == "__main__":
    main()
