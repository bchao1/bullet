from bullets import BulletCli
from bullets import colors

cli = BulletCli(
        choices = ["apple", "banana", "orange", "watermelon", "strawberry"], 
        indent = 0,
        align = 5, 
        margin = 2,
        bullet = "●",
        bullet_color=colors.foreground["black"],
        word_color=colors.foreground["red"],
        word_on_switch=colors.foreground["green"],
        background_color=colors.background["cyan"],
        background_on_switch=colors.background["yellow"],
        pad_right = 20
    )

result = cli.launch("Please choose a fruit: ")
print("You chose:", result)
