from bullet import Bullet
from bullet import styles

client = Bullet(
    **styles.Example,
    **styles.Lime
)

result = client.launch("Choose from a list: ")
print(result)