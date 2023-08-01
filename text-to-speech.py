import pyttsx3


engine = pyttsx3.init()
engine.setProperty('rate', 200)


engine.say("""
           Hello world, my name is Kumar Samyak, AKA Sam.
           I live in Frisco, Texas, USA.
           
           This is an AI voiceover.
           
           I made Connect 4!
           
           When you launch the game, a customization screen will appear. Here you can select how many rows, columns, and the number of pieces in a row are required to win. The default values are already selected.
           
           Some customization limits exist.
           
           The maximum number of rows depends on the height-wise size of your screen.
           The maximum number of columns depends on the width-wise size of your screen.
           The number of pieces in a row required to win is always less than or equal to the number of rows and columns.
           
           After that, select the mode you want to play.
           
           Once you are ready to play, click the play button.
           
           After that, a blue board with black circles in it appears. This represents the empty board. Player 1 is red, and Player 2 is Yellow. Player 1 plays first.
           
           To drop a piece, click on the column where you want to drop it.
           After a player moves, it is the other player's turn.
           
           A game ends when a player wins by making a four in a row, or the number you chose. If no one wins, it's a tie.
""")


engine.runAndWait()
engine.stop()
