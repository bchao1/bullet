from bullet import Bullet, Prompt, Check, Input, YesNo
from bullet import styles

cli = Prompt(
    [
        Bullet("Choose from a list: ", **styles.Example),
        Check("Choose from a list: ", **styles.Example),
        Input("Who are you? "),
        YesNo("Are you a student? ")
    ],
    spacing = 2
)

result = cli.launch()
print(result)