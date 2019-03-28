from bullet import Bullet, SlidePrompt, Check, Input, YesNo, Numbers
from bullet import styles
from bullet import colors

cli = SlidePrompt(
    [
        YesNo("Are you a student? ", 
            word_color = colors.foreground["yellow"]),
        Input("Who are you? ",
            default = "Batman",
            word_color = colors.foreground["yellow"]),
        Input("Really? ",
            word_color = colors.foreground["yellow"]),
        Numbers("How old are you? ", 
            word_color = colors.foreground["yellow"], 
            type = int),
        Bullet("What is your favorite programming language? ",
            choices = ["C++", "Python", "Javascript", "Not here!"],
            bullet = " >",
            margin = 2,
            bullet_color = colors.bright(colors.foreground["cyan"]),
            background_color = colors.background["black"],
            background_on_switch = colors.background["black"],
            word_color = colors.foreground["white"],
            word_on_switch = colors.foreground["white"]
        ),
        Check("What food do you like? ",
            choices = ["🍣   Sushi", 
                       "🍜   Ramen",
                       "🌭   Hotdogs", 
                       "🍔   Hamburgers", 
                       "🍕   Pizza",
                       "🍝   Spaghetti",
                       "🍰   Cakes",
                       "🍩   Donuts"],
            check = " √",
            margin = 2,
            check_color = colors.bright(colors.foreground["red"]),
            check_on_switch = colors.bright(colors.foreground["red"]),
            background_color = colors.background["black"],
            background_on_switch = colors.background["white"],
            word_color = colors.foreground["white"],
            word_on_switch = colors.foreground["black"]
        ),
    ]
)

print('\n')
result = cli.launch()
cli.summarize()