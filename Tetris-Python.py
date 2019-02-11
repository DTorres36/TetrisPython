#################################################
# TETRIS-PYTHON
# Name: Darwin Torres
# 7 October 2018
#################################################

from tkinter import *

# returns the dimensions to be used in the Tetris game
def gameDimensions():
    rows = 18
    cols = 10
    cellSize = 20
    margin = 25
    return (rows, cols, cellSize, margin)

# sets the width and height of the window and starts Tetris
def playTetris():
    (rows, cols, cellSize, margin) = gameDimensions()
    width = (2*margin + cols*cellSize)*2
    height = 2*margin + rows*cellSize
    run(width, height)

# sets up the initial data in the model
def init(data):
    (data.rows, data.cols, data.cellSize, data.margin) = gameDimensions()
    data.isGameOver = False
    data.isPaused = False
    data.boardWidth = data.cols*data.cellSize
    data.score = 0
    data.emptyColor = "blue"
    data.board = []
    # creates a 2D list without aliasing
    for rows in range(data.rows):
        row = []
        for cols in range(data.cols):
            row.append(data.emptyColor)
        data.board.append(row)
    # unique 2D list is created for each game piece
    iPiece = [
        [  True,  True,  True,  True ]
    ]
    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]
    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]
    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]
    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]
    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]
    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]
    # unique lists and corresponsing colors are saved in a list
    data.tetrisPieces = [iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece]
    data.tetrisPieceColors = ["red", "yellow", "magenta", "pink", "cyan", 
                            "green", "orange"]
    newFallingPiece(data)

# determines the next action based on player keyboard input
def keyPressed(event, data):
    if data.isGameOver == False and data.isPaused == False:
    # arrow keys move and rotate piece
        if event.keysym == "Left":
            moveFallingPiece(data, 0, -1)
        elif event.keysym == "Right":
            moveFallingPiece(data, 0, 1)
        elif event.keysym == "Down":
            moveFallingPiece(data, 1, 0)
        elif event.keysym == "x" or event.keysym == "z":
            rotateFallingPiece(data, event.keysym)
        elif event.keysym == "space":
            hardDrop(data)
    if event.keysym == "r":
    # new game can be started at any time by pressing 'r'
        data.isGameOver = False
        init(data)
    if data.isGameOver == False and event.keysym == "p":
    # current game can be paused by pressing 'p'
        data.isPaused = not data.isPaused

# executes following code repeatedly on a certain time interval
def timerFired(data):
    if data.isGameOver == False and data.isPaused == False:
        if moveFallingPiece(data, 1, 0) == False:
            # falling piece is placed when it can no longer fall
            placeFallingPiece(data)
            newFallingPiece(data)
            if not fallingPieceIsLegal(data):
            # player loses when new piece is immediately illegal
                data.isGameOver = True

# immediately places the falling piece below its current position
def hardDrop(data):
    while fallingPieceIsLegal(data) == True:
        data.fallingPieceRow += 1
    data.fallingPieceRow -= 1

# removes rows in the board that do not contain empty cells
def removeFullRows(data):
    newBoard = []
    rowsRemoved = 0
    for row in data.board:
        # only removes rows without an 'empty' cell
        if data.emptyColor in row:
            newBoard.append(row)
        else:
            rowsRemoved += 1
    rewardedPoints = rowsRemoved**2
    data.score += rewardedPoints
    # rewarded points are the square of number of rows removed
    while len(newBoard) < data.rows:
        # new empty rows are added to top of board
        newBoard = [[data.emptyColor]*data.cols] + newBoard
    data.board = newBoard

# locks a falling piece in place if it can no longer continue falling
def placeFallingPiece(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            # data.board is altered so it now includes colors of piece
            if data.fallingPiece[row][col] == True:
                data.board[row + data.fallingPieceRow][col +
                        data.fallingPieceCol] = data.fallingPieceColor
    removeFullRows(data)

# generates a new falling piece
def newFallingPiece(data):
    import random
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    # new piece is randomly chosen from list of pieces
    data.fallingPiece = data.tetrisPieces[randomIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex]
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols//2 - len(data.fallingPiece[0])//2
    
# determines if the positioning of a falling piece is legal
def fallingPieceIsLegal(data):
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            if data.fallingPiece[row][col] == True:
                boardRow = data.fallingPieceRow + row
                boardCol = data.fallingPieceCol + col
                # checks if cell is within board and not within another piece
                if (boardRow in range(len(data.board)) and boardCol in
                range(len(data.board[0])) and data.board[boardRow][boardCol] ==
                data.emptyColor):
                    continue
                return False
    return True
    
# rotates the falling piece counter-clockwise
def rotateFallingPiece(data, key):
    oldPiece = data.fallingPiece
    # original values are saved just in case new ones are illegal
    oldRow = data.fallingPieceRow
    oldCol = data.fallingPieceCol
    oldNumRows = len(data.fallingPiece)
    oldNumCols = len(data.fallingPiece[0])
    # position of new row and column are calculated
    newNumRows = oldNumCols
    newNumCols = oldNumRows
    newRow = oldRow + oldNumRows//2 - newNumRows//2
    newCol = oldCol + oldNumCols//2- newNumCols//2
    newPiece = []
    # dimensions of new piece are determined
    for row in range(newNumRows):
        addRow = []
        for col in range(newNumCols):
            addRow.append(None)
        newPiece.append(addRow)
    # new element values are determined based on rotation direction
    if key == "x":
        for row in range(oldNumRows):
            for col in range(oldNumCols):
                newPiece[(oldNumCols-1) - col][row] = oldPiece[row][col]
    elif key == "z":
        for row in range(oldNumRows):
            for col in range(oldNumCols):
                newPiece[col][(oldNumRows-1) - row] = oldPiece[row][col]
    # falling piece values are set to the new rotated values
    data.fallingPiece = newPiece
    data.fallingPieceRow = newRow
    data.fallingPieceCol = newCol
    # falling piece is changed back if new piece is not legal
    if not fallingPieceIsLegal(data):
        data.fallingPiece = oldPiece
        data.fallingPieceRow = oldRow
        data.fallingPieceCol = oldCol
    oldFallingPiece = data.fallingPiece

# moves the falling piece in a certain direction
def moveFallingPiece(data, drow, dcol):
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    if not fallingPieceIsLegal(data):
        # moves piece back to original position so illegal move is not drawn
        data.fallingPieceRow -= drow
        data.fallingPieceCol -= dcol
        return False
    return True
    
# displays the falling piece on the board
def drawFallingPiece(canvas, data):
     # loops through each cell in the falling piece 2D list
    for row in range(len(data.fallingPiece)):
        for col in range(len(data.fallingPiece[0])):
            # only draws a cell for each "True" element 
            if data.fallingPiece[row][col] == True:
                drawCell(canvas, data, row + data.fallingPieceRow, col +
                        data.fallingPieceCol, data.fallingPieceColor)
    
# draws a cell on the board 
def drawCell(canvas, data, row, col, color):
    top = data.margin + data.cellSize*row
    left = data.margin + data.cellSize*col
    right = left + data.cellSize
    bottom = top + data.cellSize
    # finds the coordinates of each corner before drawing the cell
    canvas.create_rectangle(left, top, right, bottom, 
                            fill = color,
                            width = 3)

# draws each cell on the board
def drawBoard(canvas, data):
    for row in range(len(data.board)):
        for col in range(len(data.board[0])):
            drawCell(canvas, data, row, col, data.board[row][col])

# displays the current score
def drawScore(canvas, data):
    canvas.create_text(3*data.width/4, data.margin,
                    text = "Score : " + str(data.score),
                    font = ("Helvetica", str(data.boardWidth//12), "bold"),
                    fill = "black")
                    
# Redraws what is displayed based on what has been inputted by user.
def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "orange")
    drawBoard(canvas, data)
    drawScore(canvas, data)
    drawFallingPiece(canvas, data)
    # controls are displayed beside the board
    canvas.create_text(3*data.width/4, 5*data.margin, text = "CONTROLS",
                        font = "Helvetica 20 bold")
    canvas.create_text(3*data.width/4 - data.margin/2, 9*data.margin,
                        text = 
                        "Move Left:            Left Arrow Key\n" + 
                        "Move Right:          Right Arrow Key\n"
                        "Move Down:            Down Arrow Key\n" + 
                        "Hard Drop:               Spacebar\n" + 
                        "Rotate Clockwise:           Z\n" +
                        "Rotate Counter-Clockwise:   X\n" + 
                        "Pause/Un-Pause:             P\n" + 
                        "Reset Game:                 R",
                        font = "Consolas 9")
    if data.isGameOver == True:
        # Game over screen
        canvas.create_rectangle(data.width/10, 1*data.height/4, 
                            9*data.width/10, 3*data.height/4, 
                            fill = "black", outline = "green2", 
                            width = 8)
        canvas.create_text(data.width/2, data.height/2,
                        text = "GAME OVER :(",
                        font = "Helvetica " + str(data.width//15) + \
                        " bold", fill = "green2")
        canvas.create_text(data.width/2, 3*data.height/8,
                        text = "Score: " + str(data.score),
                        font = "Helvetica " + str(data.width//20) + \
                        " bold", fill = "white")
        canvas.create_text(data.width/2, 5*data.height/8,
                        text = "Press 'R' to start a new game!",
                        font = "Helvetica " + str(data.width//26) + \
                        " bold", fill = "white")
    elif data.isPaused == True:
        # Pause screen
        canvas.create_rectangle(data.width/10, data.height/3, 
                            9*data.width/10, 2*data.height/3, 
                            fill = "black", outline = "green2", 
                            width = 8)
        canvas.create_text(data.width/2, data.height/2,
                        text = "PAUSED",
                        font = "Helvetica " + str(data.width//15) + \
                        " bold", fill = "white")

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

playTetris()
