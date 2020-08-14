from bullet import ScrollBar
from bullet import emojis
from bullet import colors

cli = ScrollBar(
    "How are you feeling today? ", 
    emojis.feelings[0],
    height = 5,
    align = 5,
    margin = 0,
    pointer = "👉",
    background_on_switch = colors.background['default'],
    word_on_switch = colors.foreground['default'],
    return_index = True
)
print('\n')
result = cli.launch()
print(result)