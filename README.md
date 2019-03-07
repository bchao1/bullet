# `bullet` : Beautiful Python Prompts Made Simple
<p align=center>
<br><br><br>
<img src="./assets/icon.png" width="400">
<br><br><br>
<a target="_blank"><img src="https://img.shields.io/badge/platform-linux-lightgrey.svg"></a>
<a target="_blank" href="https://www.python.org/downloads/" title="Python version"><img src="https://img.shields.io/badge/python-%3E=_3.6-green.svg"></a>
<a target="_blank" href="https://opensource.org/licenses/MIT" title="License: MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
<a target="_blank" href="http://makeapullrequest.com" title="PRs Welcome"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg"></a>
</p>

***
> 🎨 Customize prompts in your Python CLI tool. Extensive support for formatting, colors, background colors, styling, and etc. Also supports emojis!
***

<p align="center">
    <img src="./assets/gifs/demo.gif" width=800>
</p>

> See the sample code for the above demo in `./examples/prompt.py`.

## ✨ New Feature: `ScrollBar`

<p align="center">
    <img src="./assets/gifs/scrollbar.gif" width=400>
</p>

> See the sample code for the above demo in `./examples/scrollbar.py`.

## Bullet-lists and checkboxes
> 🎨 Robust support for user-defined styles.
<table>
    <tr>
        <th>./examples/classic.py</th>
        <th>./examples/colorful.py</th>
        <th>./examples/star.py</th>
    </tr>
    <tr>
        <td><img src="./assets/gifs/classic.gif" width="200"/></td>
        <td><img src="./assets/gifs/colorful.gif" width="200"/></td>
        <td><img src="./assets/gifs/star.gif" width="200"/></td>
    </tr>
    <tr>
        <th>Vanilla checkbox</th>
        <th>Checkbox + styles.Exam</th>
        <th>Bullet + styles.Greece</th>
    </tr>
    <tr>
        <td><img src="./assets/gifs/checkbox.gif" width="200"/></td>
        <td><img src="./assets/gifs/exam.gif" width="200"/></td>
        <td><img src="./assets/gifs/greece.gif" width="200"/></td>
    </tr>
    <tr>
        <th>Bullet + styles.Ocean</th>
        <th>Bullet + styles.Lime</th>
        <th>Bullet + styles.Christmas</th>
    </tr>
    <tr>
        <td><img src="./assets/gifs/ocean.gif" width="200"/></td>
        <td><img src="./assets/gifs/lime.gif" width="200"/></td>
        <td><img src="./assets/gifs/christmas.gif" width="200"/></td>
    </tr>
</table>

## Other input prompts
> ⛔ Passwords
<img src="./assets/gifs/password.gif" width="600"/>

> 👍 Yes/No Questions
<img src="./assets/gifs/yesno.gif" width="600"/>

> 🔢 Numbers
<img src="./assets/gifs/numbers.gif" width="600"/>

## Setting up `bullet`
> From PyPI
```shell
$ pip install bullet
```
> Build from Source
```shell
$ git clone https://github.com/Mckinsey666/bullet.git
$ cd bullet
$ pip install .
```
> With Docker
```shell
$ git clone https://github.com/Mckinsey666/bullet.git
$ cd bullet
$ docker run -it --rm -v $PWD/examples:/usr/src/app Mckinsey666/bullet python colorful.py
```
## Documentation
📖 See <a href="./DOCUMENTATION.md"> Documentation</a>.

> Currently supported prompts: `Bullet`, `Check`, `Input`, `Numbers`, `Password`, `YesNo`, `VerticalPrompt`, `SlidePrompt`, `Scrollbar`.

## Contributing
🎉 Directly send PRs! I'd also love to see your color schemes, and they can possibly be added to the default style library!

## Todo
- Windows Support
