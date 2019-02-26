from bullet import Bullet
from bullet import Check
from bullet import styles

client = Check(
    **styles.Example,
    **styles.Exam
)
print('\n', end = '')
result = client.launch("Choose from a list: ")
print(result)