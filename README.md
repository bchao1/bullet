# `bullets` : A Robust Python List Prompt Package
<p align=center>
<img src="./assets/list.png" width="400"/>
<br>
<a target="_blank"><img src="https://img.shields.io/badge/platform-linux-lightgrey.svg"></a>
<a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.6-green.svg"></a>
<a target="_blank" href="https://opensource.org/licenses/MIT" title="License: MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
<a target="_blank" href="http://makeapullrequest.com" title="PRs Welcome"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"></a>
</p>

***
> 🎨 Customize bullet list prompts in your CLI tool without effecting previous or future outputs.
***

<p align=center><img src="./assets/demo.gif" width="600"/></p>

## Usage

```python
from bullets import BulletCli

cli = BulletCli()
result = cli.launch(prompt = "Choose from a list: ")
print(result)
```

## Examples