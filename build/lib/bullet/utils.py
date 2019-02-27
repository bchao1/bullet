import os
import sys
import tty, termios
import string
from .charDef import *
from . import colors

_, n = os.popen('stty size', 'r').read().split()
COLUMNS = int(n)

def mybeep():
    print(chr(BEEP_CHAR), end = '')

def mygetc():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def getchar():
    c = mygetc()
    if ord(c) == LINE_BEGIN_KEY or \
       ord(c) == LINE_END_KEY   or \
       ord(c) == TAB_KEY        or \
       ord(c) == NEWLINE_KEY:
       return c
    
    elif ord(c) == BACK_SPACE_KEY:
        return c
    
    elif ord(c) == ESC_KEY:
        combo = mygetc()
        if ord(combo) == MOD_KEY_INT:
            key = mygetc()
            if ord(key) >= MOD_KEY_BEGIN - MOD_KEY_FLAG and ord(key) <= MOD_KEY_END - MOD_KEY_FLAG:
                if ord(mygetc()) == MOD_KEY_DUMMY:
                    return chr(ord(key) + MOD_KEY_FLAG)
                else:
                    return UNDEFINED_KEY
            elif ord(key) >= ARROW_KEY_BEGIN - ARROW_KEY_FLAG and ord(key) <= ARROW_KEY_END - ARROW_KEY_FLAG:
                return chr(ord(key) + ARROW_KEY_FLAG)
            else:
                return UNDEFINED_KEY
        else:
            mybeep()
            return getchar()

    else:
        if c in string.printable:
            return c
        else:
            return UNDEFINED_KEY

    return UNDEFINED_KEY

# Basic command line functions

def puts(s, indent = 4):
    ''' Print string with indent. '''

    forceWrite(' ' * indent + s + '\n')

def moveCursorLeft(n):
    ''' Move cursor left n columns. '''

    forceWrite("\033[{}D".format(n))

def moveCursorRight(n):
    ''' Move cursor right n columns. '''
    
    forceWrite("\033[{}C".format(n))
    
def moveCursorUp(n):
    ''' Move cursor up n rows. '''

    forceWrite("\033[{}A".format(n))

def moveCursorDown(n):
    ''' Move cursor down n rows. '''

    forceWrite("\033[{}B".format(n))

def moveCursorHead():
    forceWrite("\r")

def clearLine():
    ''' Clear content of one line on the console. '''

    forceWrite(" " * COLUMNS)
    moveCursorHead()
    
def clearConsole(n):
    ''' Clear n console rows (bottom up). ''' 

    for _ in range(n):
        clearLine()
        moveCursorUp(1)

def forceWrite(s, end = ''):
    sys.stdout.write(s + end)
    sys.stdout.flush()

def cprint(s, color = colors.foreground["default"], on = colors.background["default"], end = '\n'):
    forceWrite(on + color + s + colors.RESET, end = end)

if __name__ == "__main__":
    cprint("hello", colors.foreground["red"], colors.background["white"])