from bullet import Bullet

cli = Bullet(
        prompt = "\nPlease choose a fruit: ",
        choices = ["apple", "banana", "orange", "watermelon", "strawberry"], 
        indent = 0,
        align = 5, 
        margin = 2,
        shift = 0,
        bullet = "",
        pad_right = 5,
        return_index = True
    )

result = cli.launch()
print("You chose:", result)
