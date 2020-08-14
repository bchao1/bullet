import sys
from .charDef import *
from . import colors
from . import utils
from . import cursor
from . import keyhandler
import readline
import re

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

@keyhandler.init
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
            return_index: bool        = False
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
        self.return_index = return_index
    
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

    @keyhandler.register(ARROW_UP_KEY)
    def moveUp(self):
        if self.pos - 1 < 0:
            return
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos -= 1
            self.printBullet(old_pos)
            utils.moveCursorUp(1)
            self.printBullet(self.pos)

    @keyhandler.register(ARROW_DOWN_KEY)
    def moveDown(self):
        if self.pos + 1 >= len(self.choices):
            return
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos += 1
            self.printBullet(old_pos)
            utils.moveCursorDown(1)
            self.printBullet(self.pos)

    @keyhandler.register(NEWLINE_KEY)
    def accept(self):
        utils.moveCursorDown(len(self.choices) - self.pos)
        ret = self.choices[self.pos]
        if self.return_index:
            return ret, self.pos
        self.pos = 0
        return ret

    @keyhandler.register(INTERRUPT_KEY)
    def interrupt(self):
        utils.moveCursorDown(len(self.choices) - self.pos)
        raise KeyboardInterrupt

    def launch(self, default = None):
        if self.prompt:
            utils.forceWrite(' ' * self.indent + self.prompt + '\n')
            utils.forceWrite('\n' * self.shift)
        if default is not None:
            if type(default).__name__ != 'int':
                raise TypeError("'default' should be an integer value!")
            if not 0 <= int(default) < len(self.choices):
                raise ValueError("'default' should be in range [0, len(choices))!")
            self.pos = default
        self.renderBullets()
        utils.moveCursorUp(len(self.choices) - self.pos)
        with cursor.hide():
            while True:
                ret = self.handle_input()
                if ret is not None:
                    return ret

@keyhandler.init
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
            return_index: bool        = False
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
        self.return_index = return_index
    
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

    @keyhandler.register(SPACE_CHAR)
    def toggleRow(self):
        self.checked[self.pos] = not self.checked[self.pos]
        self.printRow(self.pos)

    @keyhandler.register(ARROW_UP_KEY)
    def moveUp(self):
        if self.pos - 1 < 0:
            return
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos -= 1
            self.printRow(old_pos)
            utils.moveCursorUp(1)
            self.printRow(self.pos)

    @keyhandler.register(ARROW_DOWN_KEY)
    def moveDown(self):
        if self.pos + 1 >= len(self.choices):
            return
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos += 1
            self.printRow(old_pos)
            utils.moveCursorDown(1)
            self.printRow(self.pos)

    @keyhandler.register(NEWLINE_KEY)
    def accept(self):
        utils.moveCursorDown(len(self.choices) - self.pos)
        ret = [self.choices[i] for i in range(len(self.choices)) if self.checked[i]]
        ret_idx = [i for i in range(len(self.choices)) if self.checked[i]]
        self.pos = 0
        self.checked = [False] * len(self.choices)
        if self.return_index:
            return ret, ret_idx
        return ret

    @keyhandler.register(INTERRUPT_KEY)
    def interrupt(self):
        utils.moveCursorDown(len(self.choices) - self.pos)
        raise KeyboardInterrupt

    def launch(self, default = None):
        if self.prompt:
            utils.forceWrite(' ' * self.indent + self.prompt + '\n')
            utils.forceWrite('\n' * self.shift)
        if default is None:
            default = []
        if default:
            if not type(default).__name__ == 'list':
                raise TypeError("`default` should be a list of integers!")
            if not all([type(i).__name__ == 'int' for i in default]):
                raise TypeError("Indices in `default` should be integer type!")
            if not all([0 <= i < len(self.choices) for i in default]):
                raise ValueError("All indices in `default` should be in range [0, len(choices))!")
            for i in default:
                self.checked[i] = True
        self.renderRows()
        utils.moveCursorUp(len(self.choices))
        with cursor.hide():
            while True:
                ret = self.handle_input()
                if ret is not None:
                    return ret

class YesNo:
    def __init__(
            self,
            prompt,
            default="y",
            indent=0,
            word_color=colors.foreground["default"],
            prompt_prefix="[y/n] "
        ):
        self.indent = indent
        if not prompt:
            raise ValueError("Prompt can not be empty!")
        if default.lower() not in ["y", "n"]:
            raise ValueError("`default` can only be 'y' or 'n'!")
        self.default = "[{}]".format(default.lower())
        self.prompt = prompt_prefix + prompt
        self.word_color = word_color

    def valid(self, ans):
        if ans is None:
            return False
        ans = ans.lower()
        if "yes".startswith(ans) or "no".startswith(ans):
            return True
        utils.moveCursorUp(1)
        utils.forceWrite(' ' * self.indent + self.prompt + self.default)
        utils.forceWrite(' ' * len(ans))
        utils.forceWrite('\b' * len(ans))
        return False

    def launch(self):
        my_input = myInput(word_color = self.word_color)
        utils.forceWrite(' ' * self.indent + self.prompt + self.default)
        while True:
            ans = my_input.input()
            if ans == "":
                return self.default.strip('[]') == 'y'
            if not self.valid(ans):
                continue
            else:
                return 'yes'.startswith(ans.lower())

class Input:
    def __init__(
            self, 
            prompt,
            default = "",
            indent = 0, 
            word_color = colors.foreground["default"],
            strip = False,
            pattern = ""
        ):
        self.indent = indent
        if not prompt:
            raise ValueError("Prompt can not be empty!")
        self.default = "[{}]".format(default) if default else ""
        self.prompt = prompt
        self.word_color = word_color
        self.strip = strip
        self.pattern = pattern
    
    def valid(self, ans):
        if not bool(re.match(self.pattern, ans)):
            utils.moveCursorUp(1)
            utils.forceWrite(' ' * self.indent + self.prompt + self.default)
            utils.forceWrite(' ' * len(ans))
            utils.forceWrite('\b' * len(ans))
            return False
        return True

    def launch(self):
        utils.forceWrite(' ' * self.indent + self.prompt + self.default)
        sess = myInput(word_color = self.word_color)
        if not self.pattern:
            while True:
                result = sess.input()
                if result == "":
                    if self.default != "":
                        return self.default[1:-1]
                    else:
                        utils.moveCursorUp(1)
                        utils.forceWrite(' ' * self.indent + self.prompt + self.default)
                        utils.forceWrite(' ' * len(result))
                        utils.forceWrite('\b' * len(result))
                else:
                    break
        else:
            while True:
                result = sess.input()
                if self.valid(result):
                    break
        return result.strip() if self.strip else result

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
            word_color = colors.foreground["default"],
            type = float
        ):
        self.indent = indent
        if not prompt:
            raise ValueError("Prompt can not be empty!")
        self.prompt = prompt
        self.word_color = word_color
        self.type = type
    
    def valid(self, ans):
        try:
            self.type(ans)
            return True
        except:
            utils.moveCursorUp(1)
            utils.forceWrite(' ' * self.indent + self.prompt)
            utils.forceWrite(' ' * len(ans))
            utils.forceWrite('\b' * len(ans))
            return False
        
    def launch(self, default = None):
        if default is not None:
            try:
                self.type(default)
            except:
                raise ValueError("`default` should be a " + str(self.type))
        my_input = myInput(word_color = self.word_color)
        utils.forceWrite(' ' * self.indent + self.prompt)
        while True:
            ans = my_input.input()
            if ans == "" and default is not None:
                return default
            if not self.valid(ans):
                continue
            else:
                return self.type(ans)

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

@keyhandler.init
class ScrollBar:
    def __init__(
            self, 
            prompt: str               = "",
            choices: list             = [], 
            pointer                   = "→",
            up_indicator: str         = "↑",
            down_indicator: str       = "↓",
            pointer_color: str        = colors.foreground["default"],
            indicator_color: str      = colors.foreground["default"],
            word_color: str           = colors.foreground["default"],
            word_on_switch: str       = colors.REVERSE,
            background_color: str     = colors.background["default"],
            background_on_switch: str = colors.REVERSE,
            pad_right                 = 0,
            indent: int               = 0,
            align                     = 0,
            margin: int               = 0,
            shift: int                = 0,
            height                    = None,
            return_index: bool        = False
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
        self.pointer = pointer
        self.up_indicator = up_indicator
        self.down_indicator = down_indicator

        self.pointer_color = pointer_color
        self.indicator_color = indicator_color
        self.word_color = word_color
        self.word_on_switch = word_on_switch
        self.background_color = background_color
        self.background_on_switch = background_on_switch

        self.max_width = len(max(self.choices, key = len)) + self.pad_right
        self.height = min(len(self.choices), # Size of the scrollbar window.
                          height if height else len(self.choices))

        self.top = 0 # Position of the top-most item rendered.
        # scrollbar won't move if pos is in range [top, top + height)
        # scrollbar moves up if pos < top
        # scrollbar moves down if pos > top + height - 1

        self.return_index = return_index
    
    def renderRows(self):
        self.printRow(self.top, indicator = self.up_indicator if self.top != 0 else '')
        utils.forceWrite('\n')

        i = self.top
        for i in range(self.top + 1, self.top + self.height - 1):
            self.printRow(i)
            utils.forceWrite('\n')

        if i < len(self.choices) - 1:
            self.printRow(i + 1, indicator= self.down_indicator if self.top + self.height != len(self.choices) else '')
            utils.forceWrite('\n')
            
    def printRow(self, idx, indicator=''):
        utils.forceWrite(' ' * (self.indent + self.align))
        back_color = self.background_on_switch if idx == self.pos else self.background_color
        word_color = self.word_on_switch if idx == self.pos else self.word_color

        if idx == self.pos:
            utils.cprint("{}".format(self.pointer) + " " * self.margin, self.pointer_color, back_color, end = '')
        else:
            utils.cprint(" " * (len(self.pointer) + self.margin), self.pointer_color, back_color, end = '')
        utils.cprint(self.choices[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.choices[idx])), on = back_color, end = '')
        utils.cprint(indicator, color = self.indicator_color, end = '')
        utils.moveCursorHead()

    @keyhandler.register(ARROW_UP_KEY)
    def moveUp(self):
        if self.pos == self.top:
            if self.top == 0:
                return # Already reached top-most position
            else:
                utils.clearConsoleDown(self.height)
                self.pos, self.top = self.pos - 1, self.top - 1
                self.renderRows()
                utils.moveCursorUp(self.height)
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos -= 1
            show_arrow = (old_pos == self.top + self.height - 1 and
                          self.top + self.height < len(self.choices))
            self.printRow(old_pos, indicator = self.down_indicator if show_arrow else '')
            utils.moveCursorUp(1)
            self.printRow(self.pos)

    @keyhandler.register(ARROW_DOWN_KEY)
    def moveDown(self):
        if self.pos == self.top + self.height - 1:
            if self.top + self.height == len(self.choices):
                return
            else:
                utils.clearConsoleUp(self.height)
                utils.moveCursorDown(1)
                self.pos, self.top = self.pos + 1, self.top + 1
                self.renderRows()
                utils.moveCursorUp(1)
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos += 1
            show_arrow = (old_pos == self.top and self.top > 0)
            self.printRow(old_pos, indicator = self.up_indicator if show_arrow else '')
            utils.moveCursorDown(1)
            self.printRow(self.pos)

    @keyhandler.register(NEWLINE_KEY)
    def accept(self):
        d = self.top + self.height - self.pos
        utils.moveCursorDown(d)
        ret = self.choices[self.pos]
        if self.return_index:
            return ret, self.pos
        self.pos = 0
        return ret

    @keyhandler.register(INTERRUPT_KEY)
    def interrupt(self):
        d = self.top + self.height - self.pos
        utils.moveCursorDown(d)
        raise KeyboardInterrupt

    def launch(self):
        if self.prompt:
            utils.forceWrite(' ' * self.indent + self.prompt + '\n')
            utils.forceWrite('\n' * self.shift)
        self.renderRows()
        utils.moveCursorUp(self.height)
        with cursor.hide():
            while True:
                ret = self.handle_input()
                if ret is not None:
                    return ret

class SlidePrompt:
    def __init__(
            self, 
            components
        ):
        self.idx = 0
        self.components = components
        if not components:
            raise ValueError("Prompt components cannot be empty!")
        self.result = []

    def summarize(self):
        for prompt, answer in self.result:
            print(prompt, answer)

    def launch(self):
        for ui in self.components:
            self.result.append((ui.prompt, ui.launch()))
            d = 1
            if type(ui).__name__ == "Bullet" or type(ui).__name__ == "Check":
                d = 1 + ui.shift + len(ui.choices)
            utils.clearConsoleUp(d + 1)
            utils.moveCursorDown(1)
        return self.result
