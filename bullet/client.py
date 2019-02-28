import sys
from .charDef import *
from . import colors
from . import utils
from . import cursor
import readline

# Reusable private utility class
class myInput:
    def __init__(self, 
            word_color: str = colors.foreground["default"], 
            password: bool = False, 
            hidden: str = '*'
        ):
        ''' Constructor for myInput 
        Args:
            word_color: color of input characters.
            password: Whether input is password.
            hidden: Character to be outputted for password input.
        '''
        self.buffer = [] # Buffer to store entered characters
        self.pos = 0  # Current cursor position
        self.password = password
        self.hidden = hidden
        self.word_color = word_color

    def moveCursor(self, pos):
        ''' Move cursort to pos in buffer. '''
        if pos < 0 or pos > len(self.buffer):
            return False
        if self.pos <= pos:
            while self.pos != pos:
                if self.password:
                    utils.cprint(self.hidden, color = self.word_color, end = '')
                else:
                    utils.cprint(self.buffer[self.pos], color = self.word_color, end = '')
                self.pos += 1
        else:
            while self.pos != pos:
                utils.forceWrite("\b")
                self.pos -= 1
        return True

    def insertChar(self, c):
        ''' Insert character c to buffer at current position. '''
        self.buffer.insert(self.pos, c)
        if self.password:
            utils.cprint(self.hidden * (len(self.buffer) - self.pos), color = self.word_color, end = '')
        else:
            utils.cprint(''.join(self.buffer[self.pos:]), color = self.word_color, end = '')
        utils.forceWrite("\b" * (len(self.buffer) - self.pos - 1))
        self.pos += 1

    def getInput(self):
        ''' Return content in buffer. '''
        ret = ''.join(self.buffer)
        self.buffer = []
        self.pos = 0
        return ret

    def deleteChar(self):
        ''' Remove character at current cursor position. '''
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
            bullet_color: str         = colors.foreground["default"],
            word_color: str           = colors.foreground["default"],
            word_on_switch: str       = colors.REVERSE,
            background_color: str     = colors.background["default"],
            background_on_switch: str = colors.REVERSE,
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
                ret = self.choices[self.pos]
                self.pos = 0
                return ret
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
            check_color: str          = colors.foreground["default"],
            check_on_switch: str      = colors.REVERSE,
            word_color: str           = colors.foreground["default"],
            word_on_switch: str       = colors.REVERSE,
            background_color: str     = colors.background["default"],
            background_on_switch: str = colors.REVERSE,
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

    def toggleRow(self):
        self.checked[self.pos] = not self.checked[self.pos]
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
                ret = [self.choices[i] for i in range(len(self.choices)) if self.checked[i]]
                self.pos = 0
                self.checked = [False] * len(self.choices)
                return ret
            elif i == ARROW_UP_KEY:
                self.movePos()
            elif i == ARROW_DOWN_KEY:
                self.movePos(up = False)
            elif i == SPACE_CHAR:
                self.toggleRow()

class YesNo:
    def __init__(
            self, 
            prompt, 
            indent = 0, 
            word_color = colors.foreground["default"]
        ):
        self.indent = indent
        if not prompt:
            raise ValueError("Prompt can not be empty!")
        self.prompt = prompt
        self.word_color = word_color

    def valid(self, ans):
        if ans.lower() not in ['y', 'n']:
            utils.moveCursorUp(1)
            utils.forceWrite(' ' * self.indent + "[y/n] " + self.prompt)
            utils.forceWrite(' ' * len(ans))
            utils.forceWrite('\b' * len(ans))
            return False
        return True
        
    def launch(self):
        my_input = myInput(word_color = self.word_color)
        utils.forceWrite(' ' * self.indent + "[y/n] " + self.prompt)
        while True:
            ans = my_input.input()
            if not self.valid(ans):
                continue
            else:
                return True if ans.lower() == 'y' else False

class Input:
    def __init__(
            self, 
            prompt, 
            indent = 0, 
            word_color = colors.foreground["default"]
        ):
        self.indent = indent
        if not prompt:
            raise ValueError("Prompt can not be empty!")
        self.prompt = prompt
        self.word_color = word_color
        
    def launch(self):
        utils.forceWrite(' ' * self.indent + self.prompt)
        return myInput(word_color = self.word_color).input()

class Password:
    def __init__(
            self, 
            prompt, 
            indent = 0, 
            hidden = '*', 
            word_color = colors.foreground["default"]
        ):
        self.indent = indent
        if not prompt:
            raise ValueError("Prompt can not be empty!")
        self.prompt = prompt
        self.hidden = hidden
        self.word_color = word_color
        
    def launch(self):
        utils.forceWrite(' ' * self.indent + self.prompt)
        return myInput(password = True, hidden = self.hidden, word_color = self.word_color).input()

class Numbers:
    def __init__(
            self, 
            prompt, 
            indent = 0, 
            word_color = colors.foreground["default"]
        ):
        self.indent = indent
        if not prompt:
            raise ValueError("Prompt can not be empty!")
        self.prompt = prompt
        self.word_color = word_color
    
    def valid(self, ans):
        try:
            float(ans)
            return True
        except:
            utils.moveCursorUp(1)
            utils.forceWrite(' ' * self.indent + self.prompt)
            utils.forceWrite(' ' * len(ans))
            utils.forceWrite('\b' * len(ans))
            return False
        
    def launch(self):
        my_input = myInput(word_color = self.word_color)
        utils.forceWrite(' ' * self.indent + self.prompt)
        while True:
            ans = my_input.input()
            if not self.valid(ans):
                continue
            else:
                return float(ans)

class VerticalPrompt:
    def __init__(
            self, 
            components, 
            spacing = 1, 
            separator = "",
            separator_color = colors.foreground["default"]
        ):

        if not components:
            raise ValueError("Prompt components cannot be empty!")
        self.components = components
        self.spacing = spacing
        self.separator = separator
        self.separator_color = separator_color
        self.separator_len = len(max(self.components, key = lambda ui: len(ui.prompt)).prompt)
        self.result = []

    def summarize(self):
        for prompt, answer in self.result:
            print(prompt, answer)
        
    def launch(self):
        for ui in self.components:
            self.result.append((ui.prompt, ui.launch()))
            if not self.separator:
                utils.forceWrite("\n" * self.spacing)
            else:
                utils.cprint(self.separator * self.separator_len, color = self.separator_color)
        return self.result

# Unfinished
'''
class ScrollBar:
    def __init__(
            self, 
            prompt: str               = "",
            choices: list             = [], 
            word_color: str           = colors.foreground["default"],
            word_on_switch: str       = colors.REVERSE,
            background_color: str     = colors.background["default"],
            background_on_switch: str = colors.REVERSE,
            pad_right                 = 0,
            indent: int               = 0,
            align                     = 0,
            margin: int               = 0,
            shift: int                = 0,
            height                    = None
        ):

        if not choices:
            raise ValueError("Choices can not be empty!")
        if indent < 0:
            raise ValueError("Indent must be > 0!")
        if margin < 0:
            raise ValueError("Margin must be > 0!")

        self.prompt = prompt
        self.choices = choices
        self.pos = 0 # Position of item at current cursor.

        self.indent = indent
        self.align = align
        self.margin = margin
        self.shift = shift
        self.pad_right = pad_right

        self.word_color = word_color
        self.word_on_switch = word_on_switch
        self.background_color = background_color
        self.background_on_switch = background_on_switch

        self.max_width = len(max(self.choices, key = len)) + self.pad_right
        self.height = height if height else len(self.choices)  # Size of the scrollbar window.

        self.top = 0 # Position of the top-most item rendered.
        # scrollbar won't move if pos is in range [top, top + height)
        # scrollbar moves up if pos < top
        # scrollbar moves down if pos > top + height - 1
    
    def renderRows(self):
        for i in range(self.top, self.top + self.height):
            self.printRow(i)
            utils.forceWrite('\n')
            
    def printRow(self, idx):
        utils.forceWrite(' ' * (self.indent + self.align))
        back_color = self.background_on_switch if idx == self.pos else self.background_color
        word_color = self.word_on_switch if idx == self.pos else self.word_color

        utils.cprint(" " * self.margin, on = back_color, end = '')
        utils.cprint(self.choices[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.choices[idx])), on = back_color, end = '')
        utils.moveCursorHead()

    def moveRow(self, up = True):
        if up:
            if self.pos == self.top:
                if self.top == 0:
                    return # Already reached top-most position
                else:
                    utils.clearConsoleDown(self.height)
                    self.pos, self.top = self.pos - 1, self.top - 1
                    self.renderRows()
                    utils.moveCursorUp(self.height)
            else:
                #utils.moveCursorUp(1)
                utils.clearLine()
                old_pos = self.pos
                self.pos -= 1
                self.printRow(old_pos)
                utils.moveCursorUp(1)
                self.printRow(self.pos)
        else:
            if self.pos == self.top + self.height - 1:
                if self.top + self.height == len(self.choices):
                    return
                else:
                    utils.clearConsoleUp(self.height)
                    if self.top == 0:
                        utils.moveCursorDown(1)
                    self.pos, self.top = self.pos + 1, self.top + 1
                    self.renderRows()
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
        utils.moveCursorUp(self.height)
        cursor.hide_cursor()
        while True:
            c = utils.getchar()
            i = c if c == UNDEFINED_KEY else ord(c)
            if i == NEWLINE_KEY:
                d = self.top + self.height - self.pos
                if self.pos == len(self.choices) - 1:
                    d -= 2
                utils.moveCursorDown(d)
                cursor.show_cursor()
                ret = self.choices[self.pos]
                self.pos = 0
                return ret
            elif i == ARROW_UP_KEY:
                self.moveRow()
            elif i == ARROW_DOWN_KEY:
                self.moveRow(up = False)
'''

class HorizontalPrompt:
    def __init__(
            self, 
            components
        ):
        self.idx = 0
        self.components = components
        if not components:
            raise ValueError("Prompt components cannot be empty!")
        self.result = []
        self.max_height = self.getMaxHeight()

    def getMaxHeight(self):
        max_h = 0
        for ui in self.components:
            if type(ui).__name__ == "Bullet" or type(ui).__name__ == "Check":
                max_h = max(max_h, 1 + ui.shift + len(ui.choices))
        return max_h

    def summarize(self):
        for prompt, answer in self.result:
            print(prompt, answer)

    def launch(self):
        for ui in self.components:
            self.result.append((ui.prompt, ui.launch()))
            utils.clearConsoleUp(self.max_height)
        return self.result
