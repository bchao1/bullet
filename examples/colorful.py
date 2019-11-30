from bullet import Bullet
from bullet import colors

cli = Bullet(
    prompt="\nPlease choose a fruit: ",
    choices=["apple", "banana", "orange", "watermelon", "strawberry"],
    indent=0,
    align=5,
    margin=2,
    shift=0,
    bullet="●",
    bullet_color=colors.foreground["magenta"],
    word_color=colors.foreground["red"],
    word_on_switch=colors.foreground["green"],
    background_color=colors.background["cyan"],
    background_on_switch=colors.background["yellow"],
    pad_right=5,
)

result = cli.launch()
print("You chose:", result)
