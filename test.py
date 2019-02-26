from bullet import Check
from bullet import Bullet
from bullet import styles

cli = Check(**styles.Example)
result = cli.launch("Choose something! ")
print(result)