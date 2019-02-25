from bullet import Bullet
from bullet import styles

client = Bullet(
    **styles.Example,
    **styles.Christmas
)

result = client.launch("Choose from a list: ")
print(result)