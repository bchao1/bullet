import sys
from .charDef import *
from . import colors
from . import utils
from . import cursor
import readline

# Reusable private utility class
class myInput:
    def __init__(self, password = False, hidden = '*'):
        self.buffer = []
        self.pos = 0
        self.password = password
        self.hidden = hidden

    def moveCursor(self, pos):
        if pos < 0 or pos > len(self.buffer):
            return False
        if self.pos <= pos:
            while self.pos != pos:
                if self.password:
                    utils.forceWrite(self.hidden)
                else:
                    utils.forceWrite(self.buffer[self.pos])
                self.pos += 1
        else:
            while self.pos != pos:
                utils.forceWrite("\b")
                self.pos -= 1
        return True

    def insertChar(self, c):
        self.buffer.insert(self.pos, c)
        if self.password:
            utils.forceWrite(self.hidden * (len(self.buffer) - self.pos))
        else:
            utils.forceWrite(''.join(self.buffer[self.pos:]))
        utils.forceWrite("\b" * (len(self.buffer) - self.pos - 1))
        self.pos += 1

    def getInput(self):
        ret = ''.join(self.buffer).strip()
        self.buffer = []
        self.pos = 0
        return ret

    def deleteChar(self):
        if self.pos == len(self.buffer):
            return
        self.buffer.pop(self.pos)
        if self.hidden:
            utils.forceWrite(self.hidden * (len(self.buffer) - self.pos) + ' ')
        else:
            utils.forceWrite(''.join(self.buffer[self.pos:]) + ' ')
        utils.forceWrite("\b" * (len(self.buffer) - self.pos + 1))

    def input(self):
        while True:
            c = utils.getchar()
            i = c if c == UNDEFINED_KEY else ord(c)

            if i == NEWLINE_KEY:
                utils.forceWrite('\n')
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
                self.moveCursor(self.pos + 1)
            elif i == ARROW_LEFT_KEY:
                self.moveCursor(self.pos - 1)
            else:
                if self.password:
                    if c != ' ':
                        self.insertChar(c)
                else:
                    self.insertChar(c)

class Bullet:
    def __init__(
            self, 
            prompt: str               = "",
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

        self.prompt = prompt
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

    def launch(self):
        if self.prompt:
            utils.forceWrite(' ' * self.indent + self.prompt + '\n')
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
            prompt: str               = "",
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

        self.prompt = prompt
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

    def launch(self):
        if self.prompt:
            utils.forceWrite(' ' * self.indent + self.prompt + '\n')
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

class YesNo:
    def __init__(self, prompt, indent = 0):
        self.indent = indent
        if not prompt:
            raise ValueError("Prompt can not be empty!")
        self.prompt = prompt

    def valid(self, ans):
        if ans.lower() not in ['y', 'n']:
            utils.moveCursorUp(1)
            utils.forceWrite(' ' * self.indent + "[y/n] " + self.prompt)
            utils.forceWrite(' ' * len(ans))
            utils.forceWrite('\b' * len(ans))
            return False
        return True
        
    def launch(self):
        my_input = myInput()
        utils.forceWrite(' ' * self.indent + "[y/n] " + self.prompt)
        while True:
            ans = my_input.input()
            if not self.valid(ans):
                continue
            else:
                return True if ans.lower() == 'y' else False

class Input:
    def __init__(self, prompt, indent = 0):
        self.indent = indent
        if not prompt:
            raise ValueError("Prompt can not be empty!")
        self.prompt = prompt
        
    def launch(self):
        utils.forceWrite(' ' * self.indent + self.prompt)
        return myInput().input()

class Password:
    def __init__(self, prompt, indent = 0, hidden = '*'):
        self.indent = indent
        if not prompt:
            raise ValueError("Prompt can not be empty!")
        self.prompt = prompt
        self.hidden = hidden
        
    def launch(self):
        utils.forceWrite(' ' * self.indent + self.prompt)
        return myInput(password = True, hidden = self.hidden).input()

class Prompt:
    def __init__(self, components, spacing):
        if not components:
            raise ValueError("Prompt components cannot be empty!")
        self.components = components
        self.spacing = spacing
        self.result = []
    
    def launch(self):
        for ui in self.components:
            self.result.append((ui.prompt, ui.launch()))
            utils.forceWrite("\n" * self.spacing)
        return self.result