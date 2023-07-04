from tabulate import tabulate
from string import ascii_uppercase

# Globl Constants
PLAYERS = {
    "NONE": '',
    "Player 1": 'O',
    "Player 2": 'X'
}

# Board
WIN_COUNT = 4
ROWS, COLUMNS = 6, 7
BOARD = [[PLAYERS["NONE"] for i in range(COLUMNS)] for j in range(ROWS)]

HEADERS = list(ascii_uppercase)[:COLUMNS]


# Main
def main():
    global BOARD, ROWS, COLUMNS, WIN_COUNT, HEADERS

    # Get user input
    d = get_size()
    ROWS, COLUMNS, WIN_COUNT = d["row"], d["col"], d["win"]
    BOARD = [[PLAYERS["NONE"] for i in range(COLUMNS)] for j in range(ROWS)]
    HEADERS = list(ascii_uppercase)[:COLUMNS]

    # Welcome
    print(f"\n\nTHIS IS CONNECT {WIN_COUNT}")
    print(f"GET {WIN_COUNT} IN A ROW, IN ANY DIRECTION\n")

    # Print Board
    print_board()

    # Maximum number of moves
    total_moves = ROWS * COLUMNS

    # Each move
    for move in range(total_moves):

        # Get player
        player = PLAYERS["Player 1"] if move % 2 == 0 else PLAYERS["Player 2"]
        player_name = [name[0] for name in list(PLAYERS.items()) if name[1] == player][0]

        # Print board and which player's move
        print(f"\n{player_name}'s Turn ({player})")
        player_move(player)
        print_board()

        # Check for win
        if (check_win(player)):
            print(f"\n\n{player_name} ({player}) WON!!!")
            return
        
    # Tie
    print("\nTIE!!!")
    return


# Checks for 4 in a row
def check_win(player):

    # Temp variable
    limit = WIN_COUNT - 1

    # Check Vertical |
    for i in range(COLUMNS):
        for j in range(ROWS - limit):

            count = sum([1 for k in range(WIN_COUNT) if BOARD[j + k][i] == player])

            if count == WIN_COUNT:
                return True
    
    # Check Horizontal -
    for i in range(ROWS):
        for j in range(COLUMNS - limit):
            
            count = sum([1 for k in range(WIN_COUNT) if BOARD[i][j + k] == player])

            if count == WIN_COUNT:
                return True
            
    # Check Diagonal-Right /
    for i in range(limit, ROWS):
        for j in range(COLUMNS - limit):
            
            count = sum([1 for k in range(WIN_COUNT) if BOARD[i - k][j + k] == player])

            if count == WIN_COUNT:
                return True
            
    # Check Diagonal-Left \
    for i in range(limit, ROWS):
        for j in range(limit, COLUMNS):
            
            count = sum([1 for k in range(WIN_COUNT) if BOARD[i - k][j - k] == player])

            if count == WIN_COUNT:
                return True

    return False


# Get size of board
def get_size():
    d = {"row": ROWS, "col": COLUMNS, "win": WIN_COUNT}
    
    print("Press Enter for Default Values")

    while True:
        row = input("Number of Rows: ")

        if len(row) == 0:
            break

        try:
            row = int(row)
            if row > 0:
                d["row"] = row
                break

        except:
            continue

    while True:
        col = input("Number of Columns: ")
        
        if len(col) == 0:
            break

        try:
            col = int(col)
            if col > 0 and col <= 26:
                d["col"] = col
                break

        except:
            continue

    while True:
        win = input("Number of Pieces in a Row for Win: ") 

        if len(win) == 0:
            break

        try:
            win = int(win)
            if win <= d["row"] or win <= d["col"]:
                d["win"] = win
                break

        except:
            continue

    return d


# Each player's move
def player_move(player):

    # Get column as a number
    column = ""
    while True:
        column = input(f"Enter Column [{HEADERS[0]}-{HEADERS[-1]}]: ").strip().upper()

        # Check if column is correct
        if len(column) == 1 and column.isalpha() and column in HEADERS:
            column = ord(column) - ord(HEADERS[0])
            
            # Check if the column is full
            if BOARD[0][column] == PLAYERS["NONE"]:
                break

    # Check each row in column
    for i in range(ROWS - 1):

        # Next row is not empty, then place move here
        if BOARD[i + 1][column] != PLAYERS["NONE"]:
            BOARD[i][column] = player
            return

        # Last row
        elif i + 1 == ROWS - 1:
            BOARD[i + 1][column] = player
            return
        
    return


# Print the board using tabulate
def print_board():
    # tabulate attributes
    headers = HEADERS
    tablefmt = "mixed_grid"

    # Print
    print("\n")
    print(tabulate(BOARD, headers, tablefmt, stralign="center"))


# Call main
if __name__ == "__main__":
    main()