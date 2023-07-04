from tabulate import tabulate

# Globl Constants
PLAYERS = {
    "NONE": '',
    "Player 1": 'O',
    "Player 2": 'X'
}


# Board
ROWS = 6
COLUMNS = 7
BOARD = [[PLAYERS["NONE"] for i in range(COLUMNS)] for j in range(ROWS)]
location = {"ROW":-1, "COLUMN":-1}


# Main
def main():

    # Global variables
    global location

    # Print welcome
    print("THIS IS CONNECT 4")
    print("GET 4 IN A ROW, IN ANY DIRECTION\n\n")

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
        location = player_move(player)
        print_board()

        # Check for win
        if (check_win(player, location)):
            print(f"\n\n{player_name} ({player}) WON!!!")
            return


# Checks for 4 in a row
def check_win(player, location):
    # Get location
    row, column = location["ROW"], location["COLUMN"]

    # Check Up
    if row >= 3 and BOARD[row-1][column] == player and BOARD[row-2][column] == player and BOARD[row-3][column] == player:
        return True
    
    # Check Down
    elif row <= 2 and BOARD[row+1][column] == player and BOARD[row+2][column] == player and BOARD[row+3][column] == player:
        return True
    
    # Check Right
    elif column <= 3 and BOARD[row][column+1] == player and BOARD[row][column+2] == player and BOARD[row][column+3] == player:
        return True
    
    # Check Left
    elif row >= 3 and BOARD[row][column-1] == player and BOARD[row][column-2] == player and BOARD[row][column-3] == player:
        return True
    
    # Check Up-Right Diagonal
    elif row >= 3 and column <= 3 and BOARD[row-1][column+1] == player and BOARD[row-2][column+2] == player and BOARD[row-3][column+3] == player:
        return True
    
    # Check Up-Left Diagonal
    elif row >= 3 and column >= 3 and BOARD[row-1][column-1] == player and BOARD[row-2][column-2] == player and BOARD[row-3][column-3] == player:
        return True
    
    # Check Down-Right Diagonal
    elif row <= 2 and column <= 3 and BOARD[row+1][column+1] == player and BOARD[row+2][column+2] == player and BOARD[row+3][column+3] == player:
        return True
    
    # Check Down-Left Diagonal
    elif row <= 2 and column >= 3 and BOARD[row+1][column-1] == player and BOARD[row+2][column-2] == player and BOARD[row+3][column-3] == player:
        return True
    
    # No Win
    else:
        return False


# Each player's move
def player_move(player):

    # Get column [A-G] as a number [0-6]
    column = ""
    while True:
        column = input("Enter Column [A-G]: ").strip().upper()
        if (len(column) == 1 and column.isalpha() and column in ["A", "B", "C", "D", "E", "F", "G"]):
            column = ord(column) - ord("A")
            break

    # Setup location
    location["COLUMN"] = column

    # Check each row in column
    for i in range(ROWS - 1):

        # Next row is not empty, then place move here
        if BOARD[i + 1][column] != PLAYERS["NONE"]:
            BOARD[i][column] = player
            
            # return the location 
            location["ROW"] = i
            return location

        # Last row
        elif i + 1 == COLUMNS - 2:
            BOARD[i + 1][column] = player

            # return the location 
            location["ROW"] = i + 1
            return location


# Print the board using tabulate
def print_board():
    headers = ["A", "B", "C", "D", "E", "F", "G"]
    tablefmt = "pretty"
    print("\n")
    print(tabulate(BOARD, headers, tablefmt))


# Call main
if __name__ == "__main__":
    main()