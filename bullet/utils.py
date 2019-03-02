from contextlib import contextmanager
import os
import sys
import tty, termios
import string
from .charDef import *
from . import colors

_, n = os.popen('stty size', 'r').read().split()
COLUMNS = int(n)  ## Size of console


def _enable_ctrl_c(fd):
    '''when fd is in raw mode, all special processing is disabled.
    This function re-enables the special processing for the INTR character
    (usually CTRL+C) by OR'ing in termios.ISIG to mode[LFLAG].

    See also
    https://github.com/python/cpython/blob/3.7/Lib/tty.py
    http://man7.org/linux/man-pages/man3/termios.3.html
    https://stackoverflow.com/questions/51509348/python-tty-setraw-ctrl-c-doesnt-work-getch
    '''
    LFLAG = 3
    mode = termios.tcgetattr(fd)
    mode[LFLAG] = mode[LFLAG] | termios.ISIG
    termios.tcsetattr(fd, termios.TCIOFLUSH, mode)


@contextmanager
def make_raw_except_interrupt(fd):
    old_settings = termios.tcgetattr(fd)
    tty.setraw(fd)
    _enable_ctrl_c(fd)
    try:
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def mygetc():
    ''' Get raw characters from input. '''
    fd = sys.stdin.fileno()
    with make_raw_except_interrupt(fd):
        try:
            return sys.stdin.read(1)
        except KeyboardInterrupt:
            clearLine()
            sys.exit(0)


def getchar():
    ''' Character input parser. '''
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
