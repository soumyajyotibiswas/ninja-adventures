# Python scripting basics - Rock, paper and scissors game

![Rock paper scissors game using python](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/6nogn8xccqbp0h3mnr0s.gif)

## Contents

* [Summary](#Al0)
* [Code](#Al1)
  * [Let's talk logic](#Al2)
  * [Of all things random](#Al3)
  * [Validating user input](#Al4)
    * [Validating user provided name](#Al41)
    * [Validating user provided input](#Al42)
* [Bonus](#Al5)
  * [Clearing screen for readibility](#Al6)
  * [Displaying a scoreboard](#Al7)
  * [Ascii art](#Al8)
* [Putting it all together](#Al9)

## Summary <a name="Al0"></a>

I have always enjoyed an occasional game of Rock, paper and scissors with my friends. What better way to demonstrate the use of randomness generator in python. We could have just done a simple head and tails, but why not this. Walk with me and see how we can create a simple Rock, paper, scissors game that we can play on the terminal.

## Code <a name="Al1"></a>

### Let's talk logic <a name="Al2"></a>

Rock beats scissors, scissors beats paper, and paper beats rock. When playing against an opponent, the possibilities are that either you and your opponent will pick the same or will pick two different elements. If you both pick the same element it will be considered a draw, and if you and your opponent pick different elements, one will win, and the other will lose the round.

The following table demostrates who would win if both pick different elements.

|          |  TABLE   |           |
|----------|----------|-----------|
| Payer 1  | Player 2 | Who wins? |
|----------|----------|-----------|
| Rock     | Paper    | Player 2  |
| Rock     | Scissors | Player 1  |
| Paper    | Scissors | Player 2  |
| Paper    | Rock     | Player 1  |
| Scissors | Rock     | Player 2  |
| Scissors | Paper    | Player 1  |

While keeping scores, each player gets a point every time they win a round. One point is assigned to a draw column every time it is a draw, which means both players picked the same element. At the end of five rounds, the total score for both players is calculated and the winner is declared. If they both score same, it is a tie.

In our case we will play against the computer. To simplify things, instead of entering 'Rock', 'Paper' and 'Scissors' as characters, which eventually we (I) would mispell, I choose to assign numbers to the elements. 'Rock' == 1, 'Paper' == 2 and 'Scissors' == 3.

To quickly check who wins, we can validate the difference between the value of the element picked by the computer vs the value of the element picked by us. For the computer to win, the difference between its value and ours will either be '-2' or '1'.

### Of all things random <a name="Al3"></a>

Making the computer choose ***randomly*** from a list of choices. The dictionary provided to the computer is {'Rock':1, 'Paper':2, 'Scissors':3}. The values from the ***dict*** is used as a list input to a ***random*** generator. We use the [random module](https://docs.python.org/3/library/random.html) to do this. We use [**random.choice**](https://docs.python.org/3/library/random.html#random.choice) to let the computer choose one value from a list of values.

```python
>>> import random
>>> print(machine_choices)
{'Rock': 1, 'Paper': 2, 'Scissors': 3}
>>> def get_machine_choice():
...     return(random.choice(list(machine_choices.values())))
... 
>>> get_machine_choice()
1
>>> get_machine_choice()
3
>>> get_machine_choice()
2
>>> get_machine_choice()
2
>>> get_machine_choice()
2
>>> get_machine_choice()
1
```

### Validating user provided input <a name="Al4"></a>

#### User provided name validation <a name="Al41"></a>

Store the user provided name in a global variable. If the name is empty assign a default name Bob.

```python
def validate_user_input_name():
    global user_input_name # Declaring the name provided by the user to modify the global variable.
    user_input_name = input("\nEnter your name: ") # Take user input for name
    if len(user_input_name.strip()) == 0: # If a space / carriage return is provided instead of a name, default to a name, in our case, Bob. We love Bob.
        user_input_name = 'Bob'

# OUTPUT

>> def validate_user_input_name():
...     global user_input_name # Declaring the name provided by the user to modify the global variable.
...     user_input_name = input("\nEnter your name: ") # Take user input for name
...     if len(user_input_name.strip()) == 0: # If a space / carriage return is provided instead of a name, default to a name, in our case, Bob. We love Bob.
...         user_input_name = 'Bob'
... 
>>> validate_user_input_name()
Enter your name: Sb
>>> print(user_input_name)
Sb
>>> validate_user_input_name()
Enter your name: 
>>> print(user_input_name)
Bob
```

#### User provided input validation <a name="Al42"></a>

Return ***True*** if user provided input is either '1' or '2' or '3'. If it is anything else return ***False***, including for empty spaces and carriage returns.

```python
def validate_user_input():
    global user_input # Declaring the user_input provided by the user to modify the global variable.
    user_input = input("\nEnter either 'Rock':1, 'Paper':2 or 'Scissors':3: ")
    if len((str(user_input)).strip()) == 0: # Removing all carriage returns / empty space cases
        return False
    elif int(user_input) not in list(machine_choices.values()): # Removing all invalid integer cases
        return False
    else:
        user_input = int(user_input)
        return True

>>> def validate_user_input():
...     global user_input
...     user_input = input("\nEnter either 'Rock':1, 'Paper':2 or 'Scissors':3: ")
...     if len((str(user_input)).strip()) == 0:
...         return False
...     elif int(user_input) not in list(machine_choices.values()):
...         return False
...     else:
...         user_input = int(user_input)
...         return True
... 
>>> validate_user_input()
Enter either 'Rock':1, 'Paper':2 or 'Scissors':3: 1
True
>>> validate_user_input()
Enter either 'Rock':1, 'Paper':2 or 'Scissors':3: 11
False
>>> validate_user_input()
Enter either 'Rock':1, 'Paper':2 or 'Scissors':3: 
False
>>> validate_user_input()
Enter either 'Rock':1, 'Paper':2 or 'Scissors':3:        
False
```

## Bonus <a name="Al5"></a>

### Clearing screen for readibility <a name="Al6"></a>

The [os](https://docs.python.org/3/library/os.html) module has uses the standard c function [system()](https://docs.python.org/3/library/os.html#os.system) to help execute system level commands. For clearing the screen in a linux environment you will use the **clear** command or in case of a windows environment you will use **cls** command.

```python
import os
x = import.system('clear') # Linux environments

x = import.system('clear') # Windows environments
```

### Displaying scores as via a DataFrame <a name="Al7"></a>

Welcome to the world of [pandas](https://pandas.pydata.org/docs/index.html). You can install pandas using the following code

```bash
python3.10 -m pip install pandas
```

The scoreboard that we designed is using pandas.

```python
>>> score_board = pandas.DataFrame(columns=["Player_1_score_card","Player_2_score_card",'Draws'],index=['Round 1','Round 2','Round 3','Round 4','Round 5'])
>>> score_board = score_board.fillna(0)
>>> score_board
         Player_1_score_card  Player_2_score_card  Draws
Round 1                    0                    0      0
Round 2                    0                    0      0
Round 3                    0                    0      0
Round 4                    0                    0      0
Round 5                    0                    0      0
```

### Ascii art <a name="Al8"></a>

```text

   ###     ######   ######  #### ####       ###    ########  ######## 
  ## ##   ##    ## ##    ##  ##   ##       ## ##   ##     ##    ##    
 ##   ##  ##       ##        ##   ##      ##   ##  ##     ##    ##    
##     ##  ######  ##        ##   ##     ##     ## ########     ##    
#########       ## ##        ##   ##     ######### ##   ##      ##    
##     ## ##    ## ##    ##  ##   ##     ##     ## ##    ##     ##    
##     ##  ######   ######  #### ####    ##     ## ##     ##    ##    

```

If you do not know if [this](https://ascii.co.uk/) or [this](https://www.asciiart.eu/) website already, do pay them a visit. Its fun to add some ascii graphics to terminal code. Our friend "The Machinee" is from here it self.

## Putting it all together <a name="Al9"></a>

Visit my [GitHub](https://github.com/soumyajyotibiswas/ninja-adventures/blob/main/Code/Python/0000003_rock_paper_scissors.py) page to check out the complete code to create a Rock, paper, scissors game that can be played on the terminal.
