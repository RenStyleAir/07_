# Tetromino (a Tetris clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Creative Commons BY-NC-SA 3.0 US

import random, time, pygame, sys
from pygame.locals import *

FPS = 25
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
BOXSIZE = 20
BOARDWIDTH = 10 
BOARDHEIGH = 20 
BLANK = '.'

MOVESIDEWAYSFREQ = 0.15
MOVEDOWNFREQ = 0.1

XMARGINX = int((WINDOWWIDTH - BOARDWIDTH * BOXSIZE)/2)
TOPMARGIN = WINDOWHEIGHT - (BOARDHEIGH - BOXSIZE) -5


WHITE =         (255,255,255)
GRAY  =         (185,185,185)
BLACK =         (  0,  0,  0)
RED =           (155,  0,  0)
LIGHTRED =      (175, 20, 20)
GREEN =         (  0,155,  0)
LIGHTGREEN =    ( 20,175, 20)
BLUE =          (  0,  0,155)
LIGHTBLUE =     ( 20, 20,175)
YELLOW =        (155,155,  0)
LIGHTYELLOW =   (175,175, 20)

BORDERCOLOR = BLUE
BGCOLOR     = BLACK
TEXTCOLOR   = WHITE
TEXTSHADOWCOLOR = GRAY
COLORS = (BLUE, GREEN , YELLOW, RED)
LIGHTCOLORS = (LIGHTBLUE, LIGHTGREEN, LIGHTYELLOW, LIGHTRED)
assert len(COLORS) == len(LIGHTCOLORS)

TEMPLATEWIDTH = 5 
TEMPLATEHEIGHT = 5

S_SHAPE_TEMPLATE = [['.....',
                    '.....',
                    '..OO.',
                    '.OO..',
                    '.....'],
                    ['.....',
                    '..O..',
                    '..OO.',
                    '...O.',
                    '.....']]

Z_SHAPE_TEMPLATE = [['.....',
                    '.....',
                    '.OO..',
                    '..OO.',
                    '.....'],
                    ['.....',
                    '..O..',
                    '.OO..',
                    '.O...',
                    '.....']]

I_SHAPE_TEMPLATE = [['..O..',
                    '..O..',
                    '..O..',
                    '..O..',
                    '.....'],
                    ['.....',
                    '.....',
                    'OOOO.',
                    '.....',
                    '.....']]

O_SHAPE_TEMPLATE = [['.....',
                    '.....',
                    '.OO..',
                    '.OO..',
                    '.....']]

J_SHAPE_TEMPLATE = [['.....',
                    '.O...',
                    '.OOO.',
                    '.....',
                    '.....'],
                    ['.....',
                    '..OO.',
                    '..O..',
                    '..O..',
                    '.....'],
                    ['.....',
                    '.....',
                    '.OOO.',
                    '...O.',
                    '.....'],
                    ['.....',
                    '..O..',
                    '..O..',
                    '..OO.',
                    '.....']]

L_SHAPE_TEMPLATE = [['.....',
                    '...O.',
                    '.OOO.',
                    '.....',
                    '.....'],
                    ['.....',
                    '..O..',
                    '..O..',
                    '..OO.',
                    '.....'],
                    ['.....',
                    '.....',
                    '.OOO.',
                    '.O...',
                    '.....'],
                    ['.....',
                    '.OO..',
                    '..O..',
                    '..O..',
                    '.....']]

T_SHAPE_TEMPLATE = [['.....',
                    '..O..',
                    '.OOO.',
                    '.....',
                    '.....'],
                    ['.....',
                    '..O..',
                    '..OO.',
                    '..O..',
                    '.....'],
                    ['.....',
                    '.....',
                    '.OOO.',
                    '..O..'],
                    ['.....',
                    '..O..',
                    '.OO..',
                    '..O..',
                    '.....']]


SHAPES = {'S':S_SHAPE_TEMPLATE,
            'Z':Z_SHAPE_TEMPLATE,
            'J':J_SHAPE_TEMPLATE,
            'L':L_SHAPE_TEMPLATE,
            'I':I_SHAPE_TEMPLATE,
            'O':O_SHAPE_TEMPLATE,
            'T':T_SHAPE_TEMPLATE}


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetromino')

    showTextScreen('Tetromino')

    while True:
        if random.randint(0,1) == 0 :
            pygame.mixer.music.load('tetrisb.mid')
        else:
            pygame.mixer.music.load('tetrisa.mid')
        pygame.mixer.music.play(-1, 0.0)
        runGame()
        pygame.mixer.music.stop()
        showTextScreen('Game Over')

def runGame():
    #
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False
    movingRight = False
    movingLeft = False
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True:
        if fallingPiece == None:

            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time()

            if not isValidPosition(board, fallingPiece):
                return

        checkForQuit()
        for event in pygame.event.get():
            if event.type == KEYUP:
                if (event.key == K_p):
                    #pausing
                    DISPLAYSURF.fill(BGCOLOR)
                    pygame.mixer.music.stop()
                    showTextScreen('Paused')
                    pygame.mixer.music.play(-1, 0.0)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif (event.key == K_left or event.key == K_a):
                    movingLeft = False
                elif (event.key == K_right or event.key == K_d):
                    movingLeft = False
                elif (event.key == K_down or event.key == K_s):
                    movingLeft = False
            
            if event.key == KEYDOWN:
                
                if (event.key == K_left or event.key == K_a) and isValidPosition(board, fallingPiece, adjX = -1):
                    fallingPiece['x'] -= 1 
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()

                if (event.key == K_right or event.key == K_d) and isValidPosition(board, fallingPiece, adjX = 1):
                    fallingPiece['x'] += 1 
                    movingLeft = False
                    movingRight = True
                    lastMoveSidewaysTime = time.time()
                    
                #rotation
                elif (event.key == K_up or event.key == K_w):
                    fallingPiece['rotation'] = (fallingPiece['rotation'] +1) %len(SHAPES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation']-1) % len(SHAPES[fallingPiece['shape']])
                    elif (event.key == K_q): 
                        fallingPiece['rotation'] = (fallingPiece['rotation']+ 1) % len(SHAPES[fallingPiece['shape']])
                        if not isValidPosition(boar, fallingPiece):
                            fallingPiece['rotation'] = (fallingPiece['rotation'] + 1)% len(SHAPES[fallingPiece['shape']])

                # fall faster
                elif(event.key == K_DOWN or event.key == K_s) :
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()

                # 
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i -1

        # 
        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime() >  MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX = -1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX = 1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPositon(board, fallingPiece, adjy = 1): 
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        #
        if time.time() - lastFallTime > fallFreq:
            # 
            if not isValidPosition(board, fallingPiece, adjY = 1):
                # 
                addToBoard(board, fallingPiece)
                score += removeCompletelines(board)
                level , fallFreq = calculateLevenAndFallFreq(score)
            else:
                # 
                fallingPiece['y'] += 1
                lastFallTime = time.time()

            
        # 
        DISPALYSURF.fill(BGCOLOR)
        drawBoard(board)
        drawStatus(score, level)
        drawNextPiece(nextPiece)
        if fallingPiece != None:
            drawPiece(fallingPiece)
        
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def makeTextObjs(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def terminate():
    pygame.quit()
    sys.exit()


def checkForKeyPress():
    # 
    # 
    checkForQuit()

    for event in pygame.event.get([KEYDOWN, KEYUP]):
            if event.type == KEYDOWN:
                continue
            return event.key
        return None

    
def showTextScreen(text):
    # 
    # 
    # 
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
    titleRect.center = (int(WINDOWWIDTH /2 ), int(WINDOWHEIGHT /2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    # 
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH /2 )-3, int(WINDOWHEIGHT /2)-3)
    DISPLAYSURF.blit(titleSurf, titleRect)


    pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH/2), int(WINDOWHEIGHT) /2 + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    
def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event == K_ESCAPE:
            terminate()
        pygame.event.post(event)


def calculateLevelAndFallFreq(score):
    # 
    # 
    level = int(score/ 10) +1
    fallFreq = 0.27 - (level * 0.02)
    return level, fallFreq

def getNewPiece():
    # 
    shape = random.choice(list(SHAPES.keys()))
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(SHAPES[shape]) -1 ),
                'x': int(BOARDWIDTH/2) - int(TEMPLATEWIDTH/2),
                'y': -2,
                'color': random.randint(0, len(colors)-1)}
    return newPiece


def addToBoard(board, piece):
    # 
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if SHAPES[piece['shape']][piece['rotation'][x][y]] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']


def getBlankBoard():
    # 
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK]* BOARDHEIGH)
    return board


def isOnBoard(x,y):
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGH


def isFalisPosition(board, piece, adjX = 0, adjY = 0):
    # 
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0 
            if isAboveBoard or SHAPES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            # if not isOnBoard(x + piece['x'] + adjX , y + piece['y']+ adjY):
            #     return False
            















        
