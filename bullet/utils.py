import shutil
import string
import sys

from . import colors

COLUMNS, _ = shutil.get_terminal_size()  ## Size of console

if sys.platform == 'win32':
    import colorama
    from .winCharDef import *
    import msvcrt

    colorama.init()


    def mygetc():
        '''Gets raw characters from input on Windows'''
        c = msvcrt.getch()
        c = c.decode('mbcs')

        return c


    def getchar():
        '''Parses input on Windows'''
        c = mygetc()
        nonesc_characters = [LINE_BEGIN_KEY, LINE_END_KEY, TAB_KEY,
                             INTERRUPT_KEY, NEWLINE_KEY, BACK_SPACE_KEY]
        if ord(c) in nonesc_characters:
            return c

        elif ord(c) == ESC_KEY:
            combo = mygetc()
            if ord(combo) in [
                ARROW_UP_KEY,
                ARROW_DOWN_KEY,
                ARROW_LEFT_KEY,
                ARROW_RIGHT_KEY,
            ]:
                return combo
        else:
            if c in string.printable:
                return c
            else:
                return UNDEFINED_KEY

else:
    import tty, termios
    from .charDef import *


    def mygetc():
        ''' Get raw characters from input. '''
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
                ord(c) == LINE_END_KEY or \
                ord(c) == TAB_KEY or \
                ord(c) == INTERRUPT_KEY or \
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
    # if the line is full, \r on Windows moves cursor to
    # the next line, so we print \b first
    forceWrite("\b\r")


def clearLine():
    ''' Clear content of one line on the console. '''
    forceWrite(" " * COLUMNS + '\b')
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


def forceWrite(s, end=''):
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

    forceWrite(on + color + s + colors.RESET, end=end)