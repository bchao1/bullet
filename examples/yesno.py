from bullet import YesNo

client = YesNo("Are you a good student? ", default = 'y')

res = client.launch()
print(res)