from bullet import Bullet
from bullet import Check
from bullet import styles

client = Check(prompt="Choose from a list: ", **styles.Example, **styles.Exam)
print("\n", end="")
result = client.launch()
print(result)
