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
    pointer_color=colors.foreground["cyan"],
    word_color = colors.foreground["white"],
    word_on_switch=colors.foreground["white"],
    background_color=colors.background["black"],
    background_on_switch=colors.background["black"]
)
result = cli.launch()