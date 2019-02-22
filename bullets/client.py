import sys
from .charDef import *
from . import colors
from . import utils
from . import cursor

class BulletCli:
    def __init__(
            self, 
            choices: list             = [], 
            bullet: str               = "●", 
            bullet_color: str         = colors.foreground["cyan"],
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
