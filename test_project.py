from numpy import zeros
from project import player_move, best_move, check_win 


ROWS, COLUMNS, WIN_COUNT = 6, 7, 4
BOARD = zeros((ROWS, COLUMNS), dtype=int)
LIMIT = WIN_COUNT - 1
PLAYER, OPP_PLAYER = 1, 2


def test_player_move():
    temp_board = BOARD.copy()
    player_move(temp_board, PLAYER, 0)
    assert temp_board[5][0] == PLAYER
    
    player_move(temp_board, OPP_PLAYER, 0)
    assert temp_board[4][0] == OPP_PLAYER
    
    player_move(temp_board, PLAYER, 3)
    assert temp_board[5][3] == PLAYER
    
    
def test_best_move():
    # Simulate Horizontal Win
    temp_board = BOARD.copy()
    player_move(temp_board, PLAYER, 0)
    player_move(temp_board, PLAYER, 1)
    player_move(temp_board, PLAYER, 2)
    assert best_move(temp_board, PLAYER) == 3
    
    # Simulate Vertical Win
    temp_board = BOARD.copy()
    player_move(temp_board, PLAYER, 0)
    player_move(temp_board, PLAYER, 0)
    player_move(temp_board, PLAYER, 0)
    assert best_move(temp_board, PLAYER) == 0
    
    # Simulate Diagonal-Right Win
    temp_board = BOARD.copy()
    player_move(temp_board, PLAYER, 0)
    player_move(temp_board, OPP_PLAYER, 1)
    player_move(temp_board, PLAYER, 1)
    player_move(temp_board, OPP_PLAYER, 2)
    player_move(temp_board, OPP_PLAYER, 2)
    player_move(temp_board, PLAYER, 2)
    player_move(temp_board, OPP_PLAYER, 3)
    player_move(temp_board, OPP_PLAYER, 3)
    player_move(temp_board, OPP_PLAYER, 3)
    assert best_move(temp_board, PLAYER) == 3
    
    # Simulate Diagonal-Left Win
    temp_board = BOARD.copy()
    player_move(temp_board, PLAYER, 6)
    player_move(temp_board, OPP_PLAYER, 5)
    player_move(temp_board, PLAYER, 5)
    player_move(temp_board, OPP_PLAYER, 4)
    player_move(temp_board, OPP_PLAYER, 4)
    player_move(temp_board, PLAYER, 4)
    player_move(temp_board, OPP_PLAYER, 3)
    player_move(temp_board, OPP_PLAYER, 3)
    player_move(temp_board, OPP_PLAYER, 3)
    assert best_move(temp_board, PLAYER) == 3


def test_check_win():
    # Simulate Horizontal Win
    for row in range(ROWS):
        for col in range(COLUMNS - LIMIT):
            temp_board = BOARD.copy()
                        
            for k in range(WIN_COUNT):
                temp_board[row, col + k] = PLAYER
            
            assert check_win(temp_board, PLAYER)
            
    # Simulate Vertical Win
    for col in range(COLUMNS):
        for row in range(ROWS - LIMIT):
            temp_board = BOARD.copy()
                        
            for k in range(WIN_COUNT):
                temp_board[row + k, col] = PLAYER
            
            assert check_win(temp_board, PLAYER)
    
    # Simulate Diagonal-Right Win
    for row in range(LIMIT, ROWS):
        for col in range(COLUMNS - LIMIT):
            temp_board = BOARD.copy()
                        
            for k in range(WIN_COUNT):
                temp_board[row - k, col + k] = PLAYER
            
            assert check_win(temp_board, PLAYER)
            
    # Simulate Diagonal-Left Win
    for row in range(LIMIT, ROWS):
        for col in range(LIMIT, COLUMNS):
            temp_board = BOARD.copy()
                        
            for k in range(WIN_COUNT):
                temp_board[row - k, col - k] = PLAYER
            
            assert check_win(temp_board, PLAYER)
