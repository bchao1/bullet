from bullet import Check

cli = Check(prompt="Choose from a list: ", choices=["item 1", "item 2", "item 3"])
result = cli.launch()
print(result)