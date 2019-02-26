import sys
from .charDef import *
from . import colors
from . import utils
from . import cursor

class Bullet:
    def __init__(
            self, 
            choices: list             = [], 
            bullet: str               = "●", 
            bullet_color: str         = colors.foreground["white"],
            word_color: str           = colors.foreground["white"],
            word_on_switch: str       = colors.foreground["black"],
            background_color: str     = colors.background["black"],
            background_on_switch: str = colors.background["white"],
            pad_right                 = 0,
            indent: int               = 0,
            align                     = 0,
            margin: int               = 0,
            shift: int                = 0,
        ):

        if not choices:
            raise ValueError("Choices can not be empty!")
        if indent < 0:
            raise ValueError("Indent must be > 0!")
        if margin < 0:
            raise ValueError("Margin must be > 0!")

        self.choices = choices
        self.pos = 0

        self.indent = indent
        self.align = align
        self.margin = margin
        self.shift = shift

        self.bullet = bullet
        self.bullet_color = bullet_color

        self.word_color = word_color
        self.word_on_switch = word_on_switch
        self.background_color = background_color
        self.background_on_switch = background_on_switch
        self.pad_right = pad_right

        self.max_width = len(max(self.choices, key = len)) + self.pad_right
    
    def renderBullets(self):
        for i in range(len(self.choices)):
            self.printBullet(i)
            utils.forceWrite('\n')
            
    def printBullet(self, idx):
        utils.forceWrite(' ' * (self.indent + self.align))
        back_color = self.background_on_switch if idx == self.pos else self.background_color
        word_color = self.word_on_switch if idx == self.pos else self.word_color
        if idx == self.pos:
            utils.cprint("{}".format(self.bullet) + " " * self.margin, self.bullet_color, back_color, end = '')
        else:
            utils.cprint(" " * (len(self.bullet) + self.margin), self.bullet_color, back_color, end = '')
        utils.cprint(self.choices[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.choices[idx])), on = back_color, end = '')
        utils.moveCursorHead()

    def moveBullet(self, up = True):
        if up:
            if self.pos - 1 < 0:
                return
            else:
                utils.clearLine()
                old_pos = self.pos
                self.pos -= 1
                self.printBullet(old_pos)
                utils.moveCursorUp(1)
                self.printBullet(self.pos)
        else:
            if self.pos + 1 >= len(self.choices):
                return
            else:
                utils.clearLine()
                old_pos = self.pos
                self.pos += 1
                self.printBullet(old_pos)
                utils.moveCursorDown(1)
                self.printBullet(self.pos)

    def launch(self, prompt = ""):
        if prompt:
            utils.forceWrite(' ' * self.indent + prompt + '\n')
            utils.forceWrite('\n' * self.shift)
        self.renderBullets()
        utils.moveCursorUp(len(self.choices))
        cursor.hide_cursor()
        while True:
            c = utils.getchar()
            i = c if c == UNDEFINED_KEY else ord(c)
            if i == NEWLINE_KEY:
                utils.moveCursorDown(len(self.choices) - self.pos)
                cursor.show_cursor()
                return self.choices[self.pos]
            elif i == ARROW_UP_KEY:
                self.moveBullet()
            elif i == ARROW_DOWN_KEY:
                self.moveBullet(up = False)

class Check:
    def __init__(
            self, 
            choices: list             = [], 
            check: str                = "√", 
            check_color: str          = colors.foreground["white"],
            check_on_switch: str      = colors.foreground["black"], 
            word_color: str           = colors.foreground["white"],
            word_on_switch: str       = colors.foreground["black"],
            background_color: str     = colors.background["black"],
            background_on_switch: str = colors.background["white"],
            pad_right                 = 0,
            indent: int               = 0,
            align                     = 0,
            margin: int               = 0,
            shift: int                = 0,
        ):

        if not choices:
            raise ValueError("Choices can not be empty!")
        if indent < 0:
            raise ValueError("Indent must be > 0!")
        if margin < 0:
            raise ValueError("Margin must be > 0!")

        self.choices = choices
        self.checked = [False] * len(self.choices)
        self.pos = 0

        self.indent = indent
        self.align = align
        self.margin = margin
        self.shift = shift

        self.check = check
        self.check_color = check_color
        self.check_on_switch = check_on_switch

        self.word_color = word_color
        self.word_on_switch = word_on_switch
        self.background_color = background_color
        self.background_on_switch = background_on_switch
        self.pad_right = pad_right

        self.max_width = len(max(self.choices, key = len)) + self.pad_right
    
    def renderRows(self):
        for i in range(len(self.choices)):
            self.printRow(i)
            utils.forceWrite('\n')
            
    def printRow(self, idx):
        utils.forceWrite(' ' * (self.indent + self.align))
        back_color = self.background_on_switch if idx == self.pos else self.background_color
        word_color = self.word_on_switch if idx == self.pos else self.word_color
        check_color = self.check_on_switch if idx == self.pos else self.check_color
        if self.checked[idx]:
            utils.cprint("{}".format(self.check) + " " * self.margin, check_color, back_color, end = '')
        else:
            utils.cprint(" " * (len(self.check) + self.margin), check_color, back_color, end = '')
        utils.cprint(self.choices[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.choices[idx])), on = back_color, end = '')
        utils.moveCursorHead()

    def checkRow(self):
        self.checked[self.pos] = True
        self.printRow(self.pos)
    
    def uncheckRow(self):
        self.checked[self.pos] = False
        self.printRow(self.pos)

    def movePos(self, up = True):
        if up:
            if self.pos - 1 < 0:
                return
            else:
                utils.clearLine()
                old_pos = self.pos
                self.pos -= 1
                self.printRow(old_pos)
                utils.moveCursorUp(1)
                self.printRow(self.pos)
        else:
            if self.pos + 1 >= len(self.choices):
                return
            else:
                utils.clearLine()
                old_pos = self.pos
                self.pos += 1
                self.printRow(old_pos)
                utils.moveCursorDown(1)
                self.printRow(self.pos)

    def launch(self, prompt = ""):
        if prompt:
            utils.forceWrite(' ' * self.indent + prompt + '\n')
            utils.forceWrite('\n' * self.shift)
        self.renderRows()
        utils.moveCursorUp(len(self.choices))
        cursor.hide_cursor()
        while True:
            c = utils.getchar()
            i = c if c == UNDEFINED_KEY else ord(c)
            if i == NEWLINE_KEY:
                utils.moveCursorDown(len(self.choices) - self.pos)
                cursor.show_cursor()
                return [self.choices[i] for i in range(len(self.choices)) if self.checked[i]]
            elif i == ARROW_UP_KEY:
                self.movePos()
            elif i == ARROW_DOWN_KEY:
                self.movePos(up = False)
            elif i == ARROW_RIGHT_KEY:
                self.checkRow()
            elif i == ARROW_LEFT_KEY:
                self.uncheckRow()

''' Unfinished Stuff...
class Input:
    def __init__(
            self, 
            word_color = colors.foreground["white"],
            word_on_input = colors.foreground["cyan"], 
            word_on_cursor = colors.foreground["cyan"],
            background_color = colors.background["black"], 
            background_on_input = colors.background["yellow"],
            background_on_cursor = colors.background["yellow"]
        ):

        self.word_color = word_color
        self.word_on_input = word_on_input
        self.word_on_cursor = word_on_cursor
        self.background_color = background_color
        self.background_on_input = background_on_input
        self.background_on_cursor = background_on_cursor

        self.buffer = []
        self.pos = 0
    
    def moveCursorRight(self):
        if self.pos + 1 > len(self.buffer):
            return False
        utils.forceWrite(self.buffer[self.pos])
        self.pos += 1
        return True

    def moveCursorLeft(self):
        if self.pos < 1:
            return False
        utils.forceWrite('\b')
        self.pos -= 1
        return True

    def insertChar(self, c):
        self.resetColors()
        self.buffer.insert(self.pos, c)
        utils.cprint(self.buffer[self.pos], self.word_on_input, self.background_on_input, end = '')
        utils.forceWrite(''.join(self.buffer[self.pos + 1:]))
        utils.forceWrite("\b" * (len(self.buffer) - self.pos - 1))
        self.pos += 1

    def deleteChar(self):
        if self.pos == len(self.buffer):
            return
        self.buffer.pop(self.pos)
        utils.forceWrite(''.join(self.buffer[self.pos:]) + ' ')
        utils.forceWrite("\b" * (len(self.buffer) - self.pos + 1))

    def getInput(self):
        ret = ''.join(self.buffer).strip()
        self.buffer = []
        return ret
    
    def resetColors(self):
        pass

    def launch(self, prompt = ""):
        #cursor.hide_cursor()
        utils.forceWrite(prompt)
        while True:
            c = utils.getchar()
            i = c if c == UNDEFINED_KEY else ord(c)

            if i == NEWLINE_KEY:
                utils.forceWrite('\n')
                #cursor.show_cursor()
                return self.getInput()
            elif i == LINE_BEGIN_KEY or \
                 i == HOME_KEY       or \
                 i == LINE_END_KEY   or \
                 i == END_KEY        or \
                 i == ARROW_UP_KEY   or \
                 i == ARROW_DOWN_KEY or \
                 i == PG_UP_KEY      or \
                 i == PG_DOWN_KEY    or \
                 i == TAB_KEY        or \
                 i == UNDEFINED_KEY:
                return
            elif i == BACK_SPACE_KEY:
                if self.moveCursor(self.pos - 1):
                    self.deleteChar()
            elif i == DELETE_KEY:
                self.deleteChar()
            elif i == ARROW_RIGHT_KEY:
                self.moveCursorRight()
            elif i == ARROW_LEFT_KEY:
                self.moveCursorLeft()
            else:
                self.insertChar(c)
'''