import pygame ,sys
import time

# initialize the pygame
pygame.init()

# screen size
WIDTH = 630
HEIGHT = 770

# screen property
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("SUDOKU GAME")

# fonts
font = pygame.font.SysFont("comicsans", 40)
font2 = pygame.font.SysFont("comicsans", 30)

# Contants
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
flag = False
flag2= True
WIDTH_SQ = 70 # size of each square
row = column = 0 # set default value to 0

# sudoku board
BOARD =[
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

# store the value in new list to not to lose original board
CHECK = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

def drawGrid():
    x = 0
    y = 0
    for i in range(10):
        thick = 5 if i%3 ==0 else 2
        pygame.draw.line(screen, black,(x , 0),(x , WIDTH),thick)
        pygame.draw.line(screen, black,(0, y),(WIDTH , y), thick)
        x += WIDTH_SQ
        y += WIDTH_SQ

def drawBoard(Board):
    # board is 630 x 630 martrix
    for i in range(9):
        for j in range(9):
            if not Board[i][j] == 0:
                pygame.draw.rect(screen, green, (j * WIDTH_SQ, i * WIDTH_SQ, WIDTH_SQ, WIDTH_SQ))
                text = font.render(f"{Board[i][j]}",True,(0,0,0))
                screen.blit(text, ( j * WIDTH_SQ + 35 ,i * WIDTH_SQ + 35)) # 35 is middle of square
    drawGrid() # added grid to the board
    text = font2.render(" Press Enter: Automaticality Solve     Press A: Check Board ", True, black)
    screen.blit(text, (0,640))

# find the empty value in board
def findEmpty(Board):
    for row in range(9):
        for col in range(9):
            if Board[row][col] == 0:
                return row, col
    return None, None

# check the entered number is valid or not
def isValid(Board, guess ,row ,col):

    # for guess to be valid guess number should not be in same row
    row_values = Board[row]
    if guess in row_values:
        return False

    #guess should not in same column
    col_values =[Board[row][i]for i in range(9)]
    if guess in col_values:
        return False

    # guess number should not be 3x3 martrix
    row_start = (row // 3)* 3 #  5 // 3 = 1  1*3 = 3
    col_start = (col // 3)* 3
    for r in range(row_start, row_start+3):
        for c in range(col_start, col_start+3):
            if Board[r][c] == guess:
                return False

    # none of the condition meets then guess number is valid
    return True

def solveSudoku(Board, delay):
    row, col = findEmpty(Board)

    # if row or column is None then sudoku is solved
    if row is None:
        return True
    pygame.event.pump()
    for guess in range(1, 10):
        if isValid(Board, guess, row, col):
            Board[row][col] = guess
            screen.fill((255,255,255))
            drawBoard(Board)
            selectBox(row,col)
            pygame.time.delay(delay)
            # call the solveSudoku function recursively
            if solveSudoku(Board, delay):
                return True
        # backtrack the value is its is not valid
        Board[row][col] = 0
        screen.fill((255, 255, 255))
        drawBoard(Board)
        selectBox(row,col)
        pygame.display.update()
        pygame.time.delay(2*delay)

    return False

#function to  create a select box around the selected item
def selectBox(row,col):
    x = WIDTH_SQ*(col)
    y = WIDTH_SQ*(row)
    for i in range(2):
        pygame.draw.line(screen, blue, (x, WIDTH_SQ*row), (x, WIDTH_SQ + WIDTH_SQ*row), 5) #vertical line
        pygame.draw.line(screen, blue, (WIDTH_SQ*col, y),(WIDTH_SQ + WIDTH_SQ*col, y), 5) # horizontal line
        x += WIDTH_SQ
        y += WIDTH_SQ

# function to draw type value on the screen
def drawValue(value, row, col):
    text = font.render(str(val), True, black)
    screen.blit(text, (col * WIDTH_SQ + 35, row* WIDTH_SQ + 25))

def check(Board , delay):
    row, col = findEmpty(BOARD)
    if row == None :
        solveSudoku(CHECK,0)
        if CHECK == Board:
            screen.fill((255,255,255))
            text = font.render("YOU SOLVED ", True, black)
            screen.blit(text, (20,WIDTH/2))
            pygame.display.update()
            time.sleep(5)
        else:
            screen.fill((255,255,255))
            text = font.render("YOU SOLVED IT WRONG ", True, (255, 0, 0))
            screen.blit(text, (20,WIDTH/2))
            pygame.display.update()
            time.sleep(5)
    else:
        screen.fill((255,255,255))
        text = font.render("PLEASE ENTERY ALL VALUE", True, black)
        screen.blit(text, (20,WIDTH/2))
        pygame.display.update()
        time.sleep(5)


RUN = True
while RUN:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                solveSudoku(CHECK,25)
                BOARD = CHECK
            if event.key == pygame.K_a:
                check(BOARD,0)
            if event.key == pygame.K_1:
                val = 1
                flag = True
            if event.key == pygame.K_2:
                val = 2
                flag = True
            if event.key == pygame.K_3:
                val = 3
                flag = True
            if event.key == pygame.K_4:
                val = 4
                flag = True
            if event.key == pygame.K_5:
                val = 5
                flag = True
            if event.key == pygame.K_6:
                val = 6
                flag = True
            if event.key == pygame.K_7:
                val = 7
                flag = True
            if event.key == pygame.K_8:
                val = 8
                flag = True
            if event.key == pygame.K_9:
                val = 9
                flag = True
            if event.key == pygame.K_c:
                val = 0
                flag = True
            if event.key == pygame.K_UP:
                if not row == 0:
                    row = row - 1
                    flag2 = False
            if event.key == pygame.K_DOWN:
                if not row == 8:
                    row = row + 1
                    flag2 = False
            if event.key == pygame.K_LEFT:
                if not col == 0:
                    col = col - 1
                    flag2 = False
            if event.key == pygame.K_RIGHT:
                if not col == 8:
                    col = col + 1
                    flag2 = False


    drawBoard(BOARD)

    # create a select select box on first empty space
    if flag2:
        row, col = findEmpty(BOARD)
        flag2 = False
    selectBox(row,col)

    # Check if the  user type a number and check if user is not typing on per bulid board
    if flag :
        if CHECK[row][col] == 0:
            drawValue(val, row,col)
            BOARD[row][col] = val
            flag = False
        else:
            # To pervent print of False after typing on per build broad
            flag = False

    pygame.display.update()
