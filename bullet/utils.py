import os
import sys
import string
import shutil
from .charDef import *
from . import colors

COLUMNS, _ = shutil.get_terminal_size()  ## Size of console

def mygetc():
    ''' Get raw characters from input. '''
    if os.name == 'nt':
        import msvcrt
        encoding = "mbcs"
        # Flush the keyboard buffer
        while msvcrt.kbhit():
            msvcrt.getwch()
        if (len(WIN_CH_BUFFER) == 0):
            # Read the keystroke
            ch = msvcrt.getwch()
            # If it is a prefix char, get second part
            if ch.encode(encoding) in (b"\x00", b"\xe0"):
                ch2 = ch + msvcrt.getwch()
                # Translate actual Win chars to bullet char types
                try:
                    chx = chr(WIN_CHAR_MAP[ch2.encode(encoding)])
                    WIN_CH_BUFFER.append(chr(MOD_KEY_INT))
                    WIN_CH_BUFFER.append(chx)
                    if ord(chx) in (INSERT_KEY - MOD_KEY_FLAG,
                                    DELETE_KEY - MOD_KEY_FLAG,
                                    PG_UP_KEY - MOD_KEY_FLAG,
                                    PG_DOWN_KEY - MOD_KEY_FLAG):
                        WIN_CH_BUFFER.append(chr(MOD_KEY_DUMMY))
                    ch = chr(ESC_KEY)
                except KeyError:
                    ch = ch2[1]
            else:
                pass
        else:
            ch = WIN_CH_BUFFER.pop(0)
    elif os.name == 'posix':
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def getchar():
    ''' Character input parser. '''
    c = mygetc()
    if ord(c) == LINE_BEGIN_KEY or \
       ord(c) == LINE_END_KEY   or \
       ord(c) == TAB_KEY        or \
       ord(c) == INTERRUPT_KEY  or \
       ord(c) == NEWLINE_KEY:
       return c
    
    elif ord(c) == BACK_SPACE_KEY or ord(c) == BACK_SPACE_CHAR:
        return c
    
    elif ord(c) == ESC_KEY:
        combo = mygetc()
        if ord(combo) == MOD_KEY_INT:
            key = mygetc()
            if ord(key) >= MOD_KEY_BEGIN - MOD_KEY_FLAG and ord(key) <= MOD_KEY_END - MOD_KEY_FLAG:
                if ord(key) in (HOME_KEY - MOD_KEY_FLAG, END_KEY - MOD_KEY_FLAG):
                    return chr(ord(key) + MOD_KEY_FLAG)
                else:
                    trail = mygetc()
                    if ord(trail) == MOD_KEY_DUMMY:
                        return chr(ord(key) + MOD_KEY_FLAG)
                    else:
                        return UNDEFINED_KEY
            elif ARROW_KEY_BEGIN - ARROW_KEY_FLAG <= ord(key) <= ARROW_KEY_END - ARROW_KEY_FLAG:
                return chr(ord(key) + ARROW_KEY_FLAG)
            else:
                return UNDEFINED_KEY
        else:
            return getchar()

    else:
        if c in string.printable:
            return c
        else:
            return UNDEFINED_KEY

    return UNDEFINED_KEY

# Basic command line functions

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
    ''' Move cursor to the start of line. '''
    forceWrite("\r")

def clearLine():
    ''' Clear content of one line on the console. '''
    forceWrite(" " * COLUMNS)
    moveCursorHead()
    
def clearConsoleUp(n):
    ''' Clear n console rows (bottom up). ''' 
    for _ in range(n):
        clearLine()
        moveCursorUp(1)

def clearConsoleDown(n):
    ''' Clear n console rows (top down). ''' 
    for _ in range(n):
        clearLine()
        moveCursorDown(1)
    moveCursorUp(n)

def forceWrite(s, end = ''):
    ''' Dump everthing in the buffer to the console. '''
    sys.stdout.write(s + end)
    sys.stdout.flush()

def cprint(
        s: str, 
        color: str = colors.foreground["default"], 
        on: str = colors.background["default"], 
        end: str = '\n'
    ):
    ''' Colored print function.
    Args:
        s: The string to be printed.
        color: The color of the string.
        on: The color of the background.
        end: Last character appended. 
    Returns:
        None
    '''
    forceWrite(on + color + s + colors.RESET, end = end)
