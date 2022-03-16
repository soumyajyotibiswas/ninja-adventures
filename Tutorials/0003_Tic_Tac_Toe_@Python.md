# Python scripting basics - Rock, paper and scissors game

## Contents

* [Summary](#Al0)
* [Code](#Al1)
  * [Let's talk logic](#Al2)
  * [Building the score board and displaying it](#Al3)
  * [Inputs from players](#Al4)
    * [Validating player provided name](#Al41)
    * [Validating player provided symbol](#Al42)
    * [Setting the symbol for the computer](#Al43)
    * [Checking which cells are available to add input to](#Al44)
    * [Validating if a player is providing correct input for cell value](#Al45)
    * [Auto populating the last cell](#Al46)
  * [Checking who won](#Al5)
* [Bonus](#Al6)
  * [Adding a time delay](#Al61)
  * [Ascii art](#Al62)
* [Putting it all together](#Al7)

## Summary <a name="Al0"></a>

Okay, who hasn't played tic-tac-toe? Okay, try noughts and crosses? Still no? This is one of the classic games out there, quick, short and fun. Take a look at the [wikipedia page](https://en.wikipedia.org/wiki/Tic-tac-toe).
Today we are going to build the game from scratch, to be played on a terminal, and yes, we are going to use python. So let's begin shall we?

[LINK TO GITHUB VIDEO](https://user-images.githubusercontent.com/79418979/158605078-c6cc8327-47ec-417f-ae15-b0ddc737ee50.mp4)
![tic-tac-toe](https://user-images.githubusercontent.com/79418979/158604872-9eff5f80-5295-4979-9d9c-f375165849a5.gif)

## Code <a name="Al1"></a>

### Let's talk logic <a name="Al2"></a>

Tic-tac-toe is played between two players on a 3x3 grid. One playes chooses 'X' and the other player chooses 'O'. Anyone can play first, but for our game, let us consider whoever chooses 'X' gets to play first. Any player who gets three 'X' or 'O' in a row or column or diagonally wins the game. If at the end of the game, no player is able to achieve that, the game ends in a draw.

The following table demostrates how a 3x3 grid would look like. Each row and its associated column number is displayed as the cell value. For row 1 column 1 it is R1C1, row 2 column 2 it is R2C2, etc.

|   R1C1   |   R1C2   |   R1C3    |
|----------|----------|-----------|
|   R2C1   |   R2C2   |   R2C3    |
|   R3C1   |   R3C2   |   R3C3    |

For a player to win, they have to get their chosen symbol of 'X' or 'O' in one of the following series. It doesn't matter the order which they went for one first.

|Winning Combinations|
|----------|
|R1C1,R1C2,R1C3|
|R2C1,R2C2,R2C3|
|R3C1,R3C2,R3C3|
|R1C1,R2C1,R3C1|
|R1C2,R2C2,R3C2|
|R1C3,R2C3,R3C3|
|R1C1,R2C2,R3C3|
|R3C1,R2C2,R1C3|

We will do the following in order

1. Display the set of rules to the player.

2. Ask the player to enter their name, and if they don't we will assign one, say Bob. How does Bob sound?

3. Ask the player if they want 'X' as their playing symbol or 'O', and assign the other one to the computer.

4. Let our computer side player green our human.

5. Design a pretty looking score board to keep track of their scores.

6. While the game is being played we will

   6.1. Display the cell locations which are not yet occupied by 'X' or 'O'.

   6.2. Let the computer decide randomly which cell value to pick as its choice. I am keeping this basic. At a later point of time, will add difficulty levels to the game, and will let the computer play offensive.

   6.3. After both the player and computer has provided their input, check if anyone has won.

### Building the score board and displaying it <a name="Al3"></a>

We will use two modules here, pandas, and [tabulate](https://pypi.org/project/tabulate/). Pandas will give as the dataframe to store data into, and we will tabulate to make it pretty.

You can install both into your environment using the following command:

```bash
python3.10 -m pip install pandas
python3.10 -m pip install tabulate
```

```python
#This is how our dataframe will look like
>>> import pandas
>>> pandas.DataFrame([['11','12','13'],['21','22','23'],['31','32','33']],columns=['C1','C2','C3'],index=['R1','R2','R3'])
    C1  C2  C3
R1  11  12  13
R2  21  22  23
R3  31  32  33
>>>
```

```python
# This is how our final scoreboard will look like on display
>>> import tabulate
>>> d = pandas.DataFrame([['11','12','13'],['21','22','23'],['31','32','33']],columns=['C1','C2','C3'],index=['R1','R2','R3'])
>>> print(tabulate.tabulate(d, tablefmt = 'fancy_grid', showindex=False))
╒════╤════╤════╕
│ 11 │ 12 │ 13 │
├────┼────┼────┤
│ 21 │ 22 │ 23 │
├────┼────┼────┤
│ 31 │ 32 │ 33 │
╘════╧════╧════╛
```

### Inputs from players <a name="Al4"></a>

#### Validating player provided name <a name="Al41"></a>

Store the user provided name in a global variable. If the name is empty assign a default name Bob.

```python
>>> validate_user_input_name()
Enter your name: SB
>>> print(user_input_name)
Sb
>>> validate_user_input_name()
Enter your name: 
>>> print(user_input_name)
Bob
```

#### Validating player provided symbol <a name="Al42"></a>

Ask the player if they want to choose 'X' as their symbol or 'O' and assign the opposite to the computer to play with. Any invalid attempts, a total of three will end the game.

```python
>>> validate_user_input_name()
Enter your name: sb
>>> user_input_name
'SB'
>>> validate_user_input_symbol()
Player SB enter either ['X', 'O'] without the quotes : x
>>> user_input_symbol
'X'
>>> validate_user_input_symbol()
Player SB enter either ['X', 'O'] without the quotes : z
Player SB enter either ['X', 'O'] without the quotes : a
Player SB enter either ['X', 'O'] without the quotes : b
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 13, in validate_user_input_symbol
ValueError: Maximum '3' invalid symbol choice attempts reached. Thank you for playing.
>>> cpu_input_symbol
'O'
>>> validate_user_input_symbol()
Player SB enter either ['X', 'O'] without the quotes : O
>>> user_input_symbol
'O'
>>> cpu_input_symbol
'X'
>>> 
```

#### Setting the symbol for the computer <a name="Al43"></a>

In the above section you see that the computer player symbol is automatically set the moment the player chooses a correct symbol. We use a simple if else statement for that.

```python
if user_input_symbol == 'X':
    cpu_input_symbol = 'O'
else:
    cpu_input_symbol = 'X'
```

#### Checking which cells are available to add input to <a name="Al44"></a>

By using list comprehensions we can quickly find out which cells does not have a 'X' or 'O' value in it.

```python
# score_board is our dataframe
# symbol choices is a list of ['X','O']
([score_board.iloc[a][b] for a in range(3) for b in range(3) if score_board.iloc[a][b] not in symbol_choices])
```

#### Validating if a player is providing correct input for cell value <a name="Al45"></a>

Display the cells available for input using the previous method then ask for user input. If the input provided by the user is incorrect three times, exit.

```python
empty_slots = get_empty_slots()
invalid_input_count = 0
while invalid_input_count < 3:
    user_input_cell_choice = input(f"\nEnter either {empty_slots} without the quotes : ")
    if user_input_cell_choice not in empty_slots:
        invalid_input_count += 1
    else:
        return user_input_cell_choice
if invalid_input_count == 3:
    raise ValueError(f"Maximum '{invalid_input_count}' invalid input choice attempts reached. Thank you for playing.")
```

#### Auto populating the last cell <a name="Al46"></a>

The game will be played for 4 rounds, if no one has won before that, and at the start of round 5, only one cell will be left, we can assign it the value of 'X'. We are using 'X' since we are assuming that player using the 'X' symbol starts the game. 

X|O|X|O|X|O|X|O|X &larr; this will always be 'X'

### Checking who won <a name="Al5"></a>

As described previously in our [code logic](#Al2) section, the winning combinations are as follows:

|Winning Combinations|
|----------|
|R1C1,R1C2,R1C3|
|R2C1,R2C2,R2C3|
|R3C1,R3C2,R3C3|
|R1C1,R2C1,R3C1|
|R1C2,R2C2,R3C2|
|R1C3,R2C3,R3C3|
|R1C1,R2C2,R3C3|
|R3C1,R2C2,R1C3|

A simple iteration of 'X' and 'O' and comparing it with the dataframe values, will show us if any of the players have already won or now.

```python
# symbol_choices = ['X','O']
for symbol_choice in symbol_choices:
    for i in range(3):
        if (symbol_choice == score_board.iloc[i][0] == score_board.iloc[i][1] == score_board.iloc[i][2]) or (symbol_choice == score_board.iloc[0][i] == score_board.iloc[1][i] == score_board.iloc[2][i]):
            return(True,symbol_choice,player_choices[symbol_choice])
    if (symbol_choice == score_board.iloc[0][0] == score_board.iloc[1][1] == score_board.iloc[2][2]) or (symbol_choice == score_board.iloc[0][2] == score_board.iloc[1][1] == score_board.iloc[2][0]):
        return(True,symbol_choice,player_choices[symbol_choice])    
return (False,symbol_choice,player_choices[symbol_choice])
```

## Bonus <a name="Al6"></a>

### Adding a time delay <a name="Al61"></a>

The [time](https://docs.python.org/3/library/time.html) module has the sleep command which can be used to introduce a time delay, making it look like the computer player is actually thinking about a choice.

```python
>>>import time
>>>time.sleep(2) # this is in seconds.
```
### Ascii art <a name="Al62"></a>

```text

   ###     ######   ######  #### ####       ###    ########  ######## 
  ## ##   ##    ## ##    ##  ##   ##       ## ##   ##     ##    ##    
 ##   ##  ##       ##        ##   ##      ##   ##  ##     ##    ##    
##     ##  ######  ##        ##   ##     ##     ## ########     ##    
#########       ## ##        ##   ##     ######### ##   ##      ##    
##     ## ##    ## ##    ##  ##   ##     ##     ## ##    ##     ##    
##     ##  ######   ######  #### ####    ##     ## ##     ##    ##    

```

If you do not know [this](https://ascii.co.uk/) or [this](https://www.asciiart.eu/) website already, do pay them a visit. Its fun to add some ascii graphics to terminal code. Our friend "The Machinee" is from here it self.

## Putting it all together <a name="Al7"></a>

Visit my [GitHub](https://github.com/soumyajyotibiswas/ninja-adventures/blob/main/Code/Python/Projects/Tic_Tac_Toe/0000005_tic_tac_toe.py) page to check out the complete code to create a tic-tac-toe game that can be played on the terminal.
