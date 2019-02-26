from bullet import YesNo

cli = YesNo("Are you an NTUEE Student? ", indent = 10)
result = cli.launch()
print(result)