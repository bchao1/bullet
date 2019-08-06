from bullet import ScrollBar
from bullet import emojis
from bullet import colors

cli = ScrollBar(
    "How are you feeling today? ", 
    emojis.feelings,
    height = 5,
    align = 5,
    margin = 3,
    pointer = "👉",
    background_on_switch = colors.background['default'],
    word_on_switch = colors.foreground['default']
)
print('\n')
result = cli.launch()
print('\n')