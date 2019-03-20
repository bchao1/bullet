from bullet import Bullet


BulletDict = Bullet(
        prompt = "\nPlease choose a fruit: ",
        choices = {"apple":["this is apple "], "banana":["no you"], "orange":2, "watermelon":3, "strawberry":4},
        indent = 0,
        align = 5,
        margin = 2,
        shift = 0,
        bullet = "",
        pad_right = 5
    )

result = BulletDict.launch()
print("You chose:", result)

