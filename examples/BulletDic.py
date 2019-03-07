from bullet import BulletDict
from bullet import colors

cli = BulletDict(
        prompt = "\nPlease choose a fruit: ",
        choices = {"apple":["me","lol"], "banana":1, "orange":2, "watermelon":3, "strawberry":4}, 
        indent = 0,
        align = 5, 
        margin = 2,
        shift = 0,
        bullet = "",
        pad_right = 5
    )

result = cli.launch()
print("You chose:", result)
