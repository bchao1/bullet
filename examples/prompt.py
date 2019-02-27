from bullet import Bullet, Prompt, Check, Input, YesNo, Numbers
from bullet import styles

cli = Prompt(
    [
        YesNo("Are you a student? "),
        Input("Who are you? "),
        Numbers("How old are you? "),
        Bullet("What is your favorite programming language? ",
              choices = ["C++", "Python", "Javascript", "Not here!"]),
    ],
    spacing = 2
)

result = cli.launch()
print(result)