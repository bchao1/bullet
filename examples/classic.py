from bullets import Bullet
from bullets import colors

cli = Bullet(
        choices = ["apple", "banana", "orange", "watermelon", "strawberry"], 
        indent = 0,
        align = 5, 
        margin = 2,
        shift = 0,
        bullet = "",
        bullet_color=colors.foreground["white"],
        word_color=colors.foreground["white"],
        word_on_switch=colors.foreground["black"],
        background_color=colors.background["black"],
        background_on_switch=colors.background["white"],
        pad_right = 5
    )

result = cli.launch("\nPlease choose a fruit: ")
print("You chose:", result)
