# `bullet` : Documentation
<p align=center>
<img src="./assets/icon.png" width="400"/>
<br>

***
> 👷 To fully customize your prompts, you'll have to take total control of formatting and colors. Here's what you need to know.
***

## Table of Contents

- General
    - [Using `bullet` Objects](#topic_1)
    - [Defining Choices](#topic_2)
    - [Customize Bullets, Checks, and Hidden Characters](#topic_3)
    - [Customize Colors](#topic_4)
    - [Formatting](#topic_5)
    - [Use Default Style Schemes](#topic_6)
- `bullet` Objects
    - [Using `Bullet` Object](#topic_7)
    - [Using `Check` Object](#topic_8)
    - [Using `Input` Object](#topic_9)
    - [Using `YesNo` Object](#topic_10)
    - [Using `Password` Object](#topic_11)
    - [Using `Numbers` Object](#topic_12)
    - [Using Prompt Objects](#topic_13)
        - [Using `VerticalPrompt` Object](#topic_14)
        - [Using `SlidePrompt` Object](#topic_15)
    - [Using `ScrollBar` Object](#topic_16)
- [More Customization: Extending Existing Prompts](#topic_17)
    - [A List of Default Keyboard Events](#topic_18)

# General

## Using `bullet` Objects <a name="topic_1"></a>
> Always create an UI object with a prompt specified.
```python
from bullet import Bullet, Check, YesNo, Input # and etc...
cli = Bullet(prompt = "Choose from the items below: ")  # Create a Bullet or Check object
result = cli.launch()  # Launch a prompt
```

## Defining Choices<a name="topic_2"></a>
```python
cli = Bullet(choices = ["first item", "second item", "third item"])
```

## Customize Bullets, Checks, and Hidden Characters<a name="topic_3"></a>
```python
cli = Bullet(bullet = "★")
cli = Check(check = "√")
cli = Password(hidden = "*")
cli = ScrollBar(pointer = "→")
```
> You can also use emojis! 

## Customize Colors<a name="topic_4"></a>
> It is recommended to EXPLICITLY specify ALL colors for an UI object.

```python
from bullet import colors
```
> 🎨 The following colors (both background and foreground) are supported in `bullets`. Note that `default` is the color of your default terminal.
```
default, black, red, green, yellow, blue, magenta, cyan, white
```

> 🎨 Remember to specify `foreground` and `background`.
```python
black_foreground = colors.foreground["black"]
white_background = colors.background["white"]
```
> 🎨 You can wrap a color with the `bright` function
```python
bright_cyan = colors.bright(colors.foreground["cyan"])
```

> 🎨 Define the following colors when initializing the UI components.
- Use foreground colors:
    - `bullet_color`
    - `check_color`
    - `pointer_color`
    - `indicator_color`
    - `check_on_switch`
    - `word_color`
    - `word_on_switch`
    - `separator_color`
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

# `bullet` Objects
## ⌨️ Using `Bullet` Object<a name="topic_7"></a>
> Single-choice prompt.
- Define `bullet` when initializing `Bullet` object.
- Move current position up and down using **arrow keys**. 
- Returns the chosen item after pressing **enter**.

## ⌨️ Using `Check` Object<a name="topic_8"></a>
> Multiple-choice prompt.
- Define `check` when initializing `Check` object.
- Move current position up and down using **arrow keys**. 
- Check/Un-check an item by pressing **space**.
- Returns the a list of chosen items after pressing **enter**.

## ⌨️ Using `Input` Object<a name="topic_9"></a>
> Just vanilla user input.

- `strip: bool`: whether to strip trailing spaces.
- `pattern: str`: Default is `""`. If defined, user input should match pattern.

## ⌨️ Using `YesNo` Object<a name="topic_10"></a>
> Guarded Yes/No question.
- Only enter `y/Y` or `n/N`. Other invalid inputs will be guarded, and the user will be asked to re-enter.

## ⌨️ Using `Password` Object<a name="topic_11"></a>
> Enter passwords. 
- Define `hidden` when initializing `Password` object. This would be the character shown on the terminal when passwords are entered.
- In convention, space characters `' '` are guarded and should not be in a password.

## ⌨️ Using `Numbers` Object<a name="topic_12"></a>
> Enter numeric values.
- Non-numeric values will be guarded, and the user will be asked to re-enter.
- Define `type` to cast return value. For example, `type = float`, will cast return value to `float`.

## ⌨️ Using `Prompt` Objects<a name="topic_13"></a>
> Wrapping it all up.

### Using `VerticalPrompt` Object<a name="topic_14"></a>
- Stack `bullet` UI components into one vertically-rendered prompt.
- Returns a list of tuples `(prompt, result)`.
- `spacing`: number of lines between adjacent UI components.
- Or, if `separator` is defined, each UI will be separated by a sequence of `separator` characters.
- See `./examples/prompt.py` to get a better understanding.

```python
cli = VerticalPrompt(
    [
        YesNo("Are you a student? "),
        Input("Who are you? "),
        Numbers("How old are you? "),
        Bullet("What is your favorite programming language? ",
              choices = ["C++", "Python", "Javascript", "Not here!"]),
    ],
    spacing = 1
)

result = cli.launch()
```

### Using  `SlidePrompt` Object<a name="topic_15"></a>
- Link `bullet` UI components into a multi-stage prompt. Previous prompts will be cleared upon entering the next stage.
- Returns a list of tuples `(prompt, result)`.

> For `Prompt` ojects, call `summarize()` after launching the prompt to print out user input.

## ⌨️ Using `ScrollBar` Object<a name="topic_16"></a>
> **Enhanced `Bullet`**: Too many items? It's OK!
- `pointer`: points to item currently selected.
- `up_indicator`, `down_indicator`: indicators shown in first and last row of the rendered items.
- `height`: maximum items rendered on terminal.
    - For example, your can have 100 choices (`len(choices) = 100`) but define `height = 5`.

# More Customization: Extending Existing Prompts<a name="topic_17"></a>
> See `./examples/check.py` for the big picture of what's going on.

In `bullet`, you can easily inherit a base class (existing `bullet` objects) and create your customized prompt. This is done by introducing the `keyhandler` module to register user-defined keyboard events.
```python
from bullet import keyhandler
```
Say you want the user to choose at least 1 and at most 3 items from a list of 5 items. You can inherit the `Check` class, and **register** a customized keyboard event as a method.
```python
@keyhandler.register(NEWLINE_KEY)
def accept(self):
    # do some validation checks: chosen items >= 1 and <= 3.
```
Note that `accept()` is the method for **all** prompts to return user input. The binded keyboard event by default is `NEWLINE_KEY` pressed.
## A List of Default Keyboard Events<a name="topic_18"></a>
> See `./bullet/charDef.py`
- `LINE_BEGIN_KEY` : Ctrl + H
- `LINE_END_KEY`: Ctrl + E 
- `TAB_KEY`         
- `NEWLINE_KEY`: Enter
- `ESC_KEY`         
- `BACK_SPACE_KEY` 
- `ARROW_UP_KEY`    
- `ARROW_DOWN_KEY`  
- `ARROW_RIGHT_KEY`  
- `ARROW_LEFT_KEY` 
- `INSERT_KEY`     
- `DELETE_KEY`   
- `END_KEY`         
- `PG_UP_KEY`      
- `PG_DOWN_KEY`    
- `SPACE_CHAR`
- `INTERRUPT_KEY`: Ctrl + C