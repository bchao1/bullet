import sys

# Keyboard mapping macros 

LINE_BEGIN_KEY  = 1
LINE_END_KEY    = 5
TAB_KEY         = ord('\t')
NEWLINE_KEY     = 13 # Could be platform dependent. Advised to check
ESC_KEY         = 27
BACK_SPACE_KEY  = 127
ARROW_KEY_FLAG  = 1 << 8
ARROW_KEY_INT   = 91
ARROW_UP_KEY    = 65 + ARROW_KEY_FLAG
ARROW_DOWN_KEY  = 66 + ARROW_KEY_FLAG
ARROW_RIGHT_KEY  = 67 + ARROW_KEY_FLAG
ARROW_LEFT_KEY = 68 + ARROW_KEY_FLAG
ARROW_KEY_BEGIN = ARROW_UP_KEY
ARROW_KEY_END   = ARROW_LEFT_KEY
MOD_KEY_FLAG    = 1 << 9
MOD_KEY_INT     = 91
HOME_KEY        = 49 + MOD_KEY_FLAG
INSERT_KEY      = 50 + MOD_KEY_FLAG
DELETE_KEY      = 51 + MOD_KEY_FLAG
END_KEY         = 52 + MOD_KEY_FLAG
PG_UP_KEY       = 53 + MOD_KEY_FLAG
PG_DOWN_KEY     = 54 + MOD_KEY_FLAG
MOD_KEY_BEGIN   = HOME_KEY
MOD_KEY_END     = PG_DOWN_KEY
MOD_KEY_DUMMY   = 126
UNDEFINED_KEY   = sys.maxsize
BEEP_CHAR       = 7
BACK_SPACE_CHAR = 8
SPACE_CHAR      = ord(' ')
INTERRUPT_KEY   = 3

if sys.platform == "win32":
    WIN_CH_BUFFER = []
    WIN_CHAR_MAP = {
        b"\xe0H": ARROW_UP_KEY - ARROW_KEY_FLAG,
        b"\x00H": ARROW_UP_KEY - ARROW_KEY_FLAG,
        b"\xe0P": ARROW_DOWN_KEY - ARROW_KEY_FLAG,
        b"\x00P": ARROW_DOWN_KEY - ARROW_KEY_FLAG,
        b"\xe0M": ARROW_RIGHT_KEY - ARROW_KEY_FLAG,
        b"\x00M": ARROW_RIGHT_KEY - ARROW_KEY_FLAG,
        b"\xe0K": ARROW_LEFT_KEY - ARROW_KEY_FLAG,
        b"\x00K": ARROW_LEFT_KEY - ARROW_KEY_FLAG,
        b"\xe0G": HOME_KEY - MOD_KEY_FLAG,
        b"\x00G": HOME_KEY - MOD_KEY_FLAG,
        b"\xe0R": INSERT_KEY - MOD_KEY_FLAG,
        b"\x00R": INSERT_KEY - MOD_KEY_FLAG,
        b"\xe0S": DELETE_KEY - MOD_KEY_FLAG,
        b"\x00S": DELETE_KEY - MOD_KEY_FLAG,
        b"\xe0O": END_KEY - MOD_KEY_FLAG,
        b"\x00O": END_KEY - MOD_KEY_FLAG,
        b"\xe0I": PG_UP_KEY - MOD_KEY_FLAG,
        b"\x00I": PG_UP_KEY - MOD_KEY_FLAG,
        b"\xe0Q": PG_DOWN_KEY - MOD_KEY_FLAG,
        b"\x00Q": PG_DOWN_KEY - MOD_KEY_FLAG
        }
