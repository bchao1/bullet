from bullet import YesNo

cli = YesNo(prompt = "Are you a student? ")
print('\n', end = '')
result = cli.launch()
print(result)