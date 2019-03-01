from bullet import ScrollBar

cli = ScrollBar("Choose from a list: ", 
    ["Item {}".format(i) for i in range(1, 11)],
    height = 5,
    align = 5
)
result = cli.launch()
print(result)