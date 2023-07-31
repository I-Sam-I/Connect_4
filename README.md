# Connect_4
#### Video Demo: <https://youtu.be/oqO9bwvrjpA>

#### Description:
GitHub Repo: <https://github.com/I-Sam-I/Connect_4/tree/main>
<br><br>

#### Connect 4 Rules
The rules of this game are the same as those of the official Connect 4. However, you can modify the board to be bigger or smaller. You can read the rules of the official Connect 4 [here](https://www.gamesver.com/the-rules-of-connect-4-according-to-m-bradley-hasbro/).

#### How to Play
To play, download `main.exe` (from releases), and run it. It displays a "Connect 4 Customization" menu when you run it. Note that the default values are already selected.
<br><br>
Default Values
- Number of Rows: 6
- Number of Columns: 7
- Number of Pieces in a Row to Win: 4

You can change these values; however, there are limitations:
- The max number of rows depends on the height of your screen.
- The max number of columns depends on the width of your screen.
- The number of pieces in a row to win cannot exceed the number of rows or columns.

Mode Selection:
- Player vs Player: 2 player game (on the same device)
- Player vs Computer: The player is red and the computer is yellow

After clicking on `PLAY`, Player 1 (red) plays first, followed by Player 2 (yellow). To drop a piece, click on a valid column. Once a player gets a 4 (or the value you selected) in a row, the game is over, and that player wins. To play again, restart the process.

#### Files and Folders
- **project.py**
  <br>
  `project.py` is the improved and cleaner version of `pygame_v3`. `project.py` also implements a simple AI algorithm. The algorithm drops a piece in all valid columns, decide which move is the best, and plays that.

- **test_project.py**
  <br>
  Tests `player_move()`, `best_move()`, and `check_win()`

- **ptext.py**
  <br>
  This is a module from [pygame text](https://github.com/cosmologicon/pygame-text) that I use in `main.py`
- **versions/**
  <br>
  This folder stores all my previous versions. `version_1` and `version_2` are command line based and use [tabulate](https://pypi.org/project/tabulate/). `pygame_v1`, `pygame_v2`, and `pygame_v3` use [pygame](https://www.pygame.org/), [sys](https://docs.python.org/3/library/sys.html), [numpy](https://numpy.org/), [pygame gui](https://github.com/MyreMylar/pygame_gui), and [ptext](https://github.com/cosmologicon/pygame-text).

  - `version_1`
    <br>
    The first version of my Connect 4 game is a command line-based game, meaning it is text-based in the Terminal. This version is not customizable. It uses the `tabulate` function from the `tabulate` module to display the board. The player types a letter from A-G, representing the columns, to drop a piece. There are many bugs with this code. For instance, the `check_win()` function does not declare a winner if a player drops a piece in the middle of a 4 in a row. The `check_win()` function is also bulky and inefficient.

  - `version_2`
    <br>
    `version_2` is also command-line based and uses the `tabulate` function from `tabulate`. The `check_win()` function bug is resolved. However, the user can change the number of rows, columns, and pieces in a row required to win. There is no maximum number of rows, but the maximum number of columns is only 26 as the user has to use alphabets (A-Z) to drop a piece. The number of pieces in a row to win is always less than or equal to the rows or columns.
    
  - `pygame_v1`
    <br>
    `pygame_v1` is the first version that uses `pygame` for an interactable board and `numpy` to initialize the board. The user cannot customize the game. If the players tie, then the game crashes. This version does not have a game loop, and the code is all over the place.

  - `pygame_v2`
    <br>
    `pygame_v2` is the second version, where the user can customize the board. However, there were no restrictions on how big the board could be other than that it had to be a two-digit number. I accomplished this by using `pygame_gui`'s `TextEntryLine`. The code is neater and better designed and has a main game loop. Some bugs in the code include that the game is infinitely long if there is a tie and that when a player wins, the text is too big to fit the screen if the board is smaller than the default values.

  - `pygame_v3`
    <br>
    `pygame_v3` is the third version. The user can still customize the board; however, there are restrictions now. The maximum number of rows and columns depends on the user's screen size. I used dropdowns to limit the user's input. I used `drawbox` and `draw` from `ptext` to display the winner correctly without overflowing. The rest is the same.
