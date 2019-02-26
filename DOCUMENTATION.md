# `bullet` : Documentation
<p align=center>
<img src="./assets/list.png" width="400"/>
<br>

***
> 👷 To fully customize your list prompt, you'll have to take total control of formatting and colors. Here's what you need to know.
***

## Table of Contents

- Overview
    - [Using `bullet`](#topic_1)
    - [Defining Choices](#topic_2)
    - [Customize Bullets and Checks](#topic_3)
    - [Customize Colors](#topic_4)
    - [Formatting](#topic_5)
    - [Use Default Style Schemes](#topic_6)
- [Using `Bullet` Object](#topic_7)
- [Using `Check` Object](#topic_8)
- [Using `Input` Object](#topic_9)
- [Using `YesNo` Object](#topic_10)


## Using `bullet`<a name="topic_1"></a>
> Always create a CLI UI object with a prompt specified.
```python
from bullet import Bullet, Check, YesNo, Input # and etc...
cli = Bullet(prompt = "...")  # Create a Bullet or Check object
result = cli.launch()  # Launch a prompt
```

## Defining Choices<a name="topic_2"></a>
```python
cli = Bullet(choices = ["first item", "second item", "thrid item"])
```

## Customize Bullets and Checks<a name="topic_3"></a>
```python
cli = Bullet(bullet = "★")
cli = Check(check = "√")
```

## Customize Colors<a name="topic_4"></a>
```python
from bullet import colors
```
> 🎨 The following colors are supported in `bullets`. 
```
black, red, green, yellow, blue, magenta, cyan, white
```
> 🎨 Remember to specify `foreground` and `background`.
```python
black_foreground = colors.foreground["black"]
white_background = colors.background["white"]
```
> 🎨 Define the following colors when initializing `Bullet` and `Check` objects.
- Use foreground colors:
    - `bullet_color`
    - `check_color`
    - `check_on_switch`
    - `word_color`
    - `word_on_switch`
- Use background colors:
    - `background_color`
    - `background_on_switch`

## Formatting<a name="topic_5"></a>
> 📐 Define the following UI components (not all is needed for some objects).
- `indent`: distance from left-boundary to start of prompt.
- `pad_right`: extended background length.
- `align`: distance between bullet (or check) and start of prompt.
- `margin`: distance between list item and bullets (or checks).
- `shift`: number of new lines between prompt and first item.

<p align=center>
<img src="./assets/formatting.png" width="600"/>
</p>

## Use Default Style Schemes<a name="topic_6"></a>
> 👷 Currently only styles for `Bullet` is supported.
```python
from bullet import styles
client = Bullet(**styles.Greece)
```

## ⌨️ Using `Bullet` Object<a name="topic_7"></a>
> Single-choice prompt
- Move current position up and down using **arrow keys**. 
- Returns the chosen item after pressing **enter**.

## ⌨️ Using `Check` Object<a name="topic_8"></a>
> Multiple-choice prompt
- Move current position up and down using **arrow keys**. 
- Check an item by pressing **right arrow**. 
- Un-check an item by pressing **left arrow**.
- Returns the a list of chosen items after pressing **enter**.

## ⌨️ Using `Input` Object<a name="topic_9"></a>
> Just vanilla user input.

## ⌨️ Using `YesNo` Object<a name="topic_10"></a>
> Guarded Yes/No question.
- Only enter `y/Y` or `n/N`. Other invalid inputs will be guarded, and the user will be asked to re-enter.