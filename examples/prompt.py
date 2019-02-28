from bullet import Bullet, VerticalPrompt, Check, Input, YesNo, Numbers
from bullet import styles
from bullet import colors

cli = VerticalPrompt(
    [
        YesNo("Are you a student? "),
        Input("Who are you? "),
        Numbers("How old are you? "),
        Bullet("What is your favorite programming language? ",
              choices = ["C++", "Python", "Javascript", "Not here!"]),
    ],
    spacing = 1,
    separator = "-",
    separator_color = colors.foreground["cyan"]
)

result = cli.launch()
cli.summarize()