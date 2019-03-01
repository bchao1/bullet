from bullet import ScrollBar
from bullet import colors
import random
''' Pumping bars. '''

n = [random.randint(0, 15) for _ in range(1000)]
choices = []
# Do some interpolation
for i in range(0, len(n) - 1):
    choices.append(n[i])
    choices.append(int((n[i] + n[i + 1]) / 2))
choices = list(map(lambda i : "▉" * i, choices))

cli = ScrollBar(
    prompt="",
    choices=choices,
    height = 1,
    pointer = "",
    word_color=colors.bright(colors.foreground["cyan"]),
    word_on_switch=colors.bright(colors.foreground["cyan"]),
    background_color=colors.background["black"],
    background_on_switch=colors.background["black"]
)
print('\n')
cli.launch()