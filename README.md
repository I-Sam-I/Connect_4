# Connect_4
#### Video Demo: <URL HERE>

#### Description:

This project is for [CS50x](https://cs50.harvard.edu/x/2023/)'s Final Project.

#### Connect 4 Rules
The rules of this game is the same as the rules of the official Connect 4. However, the board can be modified to be bigger or smaller. You can read the rules of the official Connect 4 [here](https://www.gamesver.com/the-rules-of-connect-4-according-to-m-bradley-hasbro/).

#### How to Play
To play, download `main.exe`, and run it. When you run it, it displays a "Connect 4 Customization" menu. Note that the default values are already selected.
<br><br>
Default Values
- Number of Rows: 6
- Number of Columns: 7
- Number of Pieces in a Row to Win: 4

You can change these values, however, there are limitations:
- The max number of rows depends on the height of your screen.
- The max number of columns depends on the width of your screen.
- The max number of pieces in a row to win cannot be greater than the number of rows or columns.

<br><br>

Player 1 (red) plays first, followed by Player 2 (yellow). To drop a piece click on a column thats valid to play in. Once any player gets a 4 (or the value you selected) in a row, the game is over and that player wins. To play again, restart the process.

#### Files and Folders
- **versions/**
  This folder contains all my previous versions, `version_1` and `version_2` are command line based, `pygame_v1`, `pygame_v2`, and `pygame_v3` use [pygame](https://www.pygame.org/)
