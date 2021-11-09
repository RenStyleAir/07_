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

# new
# 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

                










        
