# Python scripting basics - BMI calculator

## Contents

* [Summary](#Al0)
* [Code](#Al1)
  * [Taking data from the user](#Al2)
  * [Calculating the B.M.I](#Al3)
  * [Getting the B.M.I category](#Al4)
  * [Putting the code together](#Al5)

## Summary <a name="Al0"></a>

In today's post I will walk you step by step on how to write a basic python script to calculate your body mass index(B.M.I). We will ask the user for some input, and based on it, calculate their B.M.I and return also tell the user, which category their B.M.I falls under. Body mass index is defined by the formula as below:

```text
B.M.I = [your weight in (Kg) / (your height in (m))^2]
Kg - Kilogram
m - metre
```

There are several defined B.M.I categories, such as:

```text
Underweight = B.M.I below < 18.5.
Normal weight = B.M.I between 18.5-24.9.
Overweight = B.M.I between 25-29.9.
Obesity = B.M.I 30 or above 30.
```

## Code <a name="Al1"></a>

### Taking data from the user <a name="Al2"></a>

* We are going to use the [input](https://docs.python.org/3/library/functions.html#input) function, and store the data provided by the user in a variable.

![Python Input Function](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/3mtgrpatsdpynj39awe9.png)

```python
>>> user_name = input("Enter your name: ")
Enter your name: Soumyajyoti Biswas
>>> print(user_name)
Soumyajyoti Biswas
>>> 
```

* We are going to ask the user for the name of the user, their weight in Kg(s) and their height in cm(s)

```python
user_name = input("Enter your name: ")
user_weight = float(input("Enter your weight in Kg(s): "))
user_height = float(input("Enter your height in cm(s): "))
```

### Calculating the B.M.I <a name="Al3"></a>

* Lets take the data that the user provided and put it through our B.M.I formula. Note that the user is providing their height in cm(s). So we will convert that to metre first. To convert cm to m, you divide it by 100.

```python
>>> user_name = input("Enter your name: ")
Enter your name: Soumyajyoti Biswas
>>> user_weight = float(input("Enter your weight in Kg(s): "))
Enter your weight in Kg(s): 70
>>> user_height = float(input("Enter your height in cm(s): "))
Enter your height in cm(s): 165
>>> bmi = round(user_weight/((user_height/100) ** 2),1)
>>> print(bmi)
25.7
```

* In the above code I did two things:
  * [1] Convert the user input for weight and height from string to a float data type. The input function provides data output as type string. Hence we have to convert it to a float data type to perform numerical operation on it. See what error comes if you do not [Ref1]. You can see the various datatypes [here](https://docs.python.org/3/library/datatypes.html).
  * [2] Round the result of B.M.I calculation to a single decimal. See how the [round function](https://docs.python.org/3/library/functions.html#round) works.

```python
# Error displayed if you try to cast a string to a float. [Ref1]
>>> x = input()
12345
>>> type(x)
<class 'str'>
>>> x + x
'1234512345'
>>> type(x + x)
<class 'str'>
>>> x / 10
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: unsupported operand type(s) for /: 'str' and 'int'
```

### Getting the B.M.I category based on calculated B.M.I <a name="Al4"></a>

* Let us take the calculated B.M.I and try and place it in a category as defined above. We will use the **[If / elif / else](https://docs.python.org/3/tutorial/controlflow.html#if-statements)** to do that.

```python
>>> if bmi < 18.5:
...   result = "Underweight"
... elif bmi >= 18.5 and bmi <= 24.9:
...   result = "Normal"
... elif bmi >= 25 and bmi <= 29.9:
...   result = "Overweight"
... else:
...   result = "Very overweight"
... 
>>> print(result)
Overweight
```

### Putting it all together <a name="Al5"></a>

* Let's put all the code together to build a script

```python
user_name = input("Enter your name: ")
user_weight = float(input("Enter your weight in Kg(s): "))
user_height = float(input("Enter your height in cm(s): "))
bmi = round(user_weight/((user_height/100) ** 2),1)
if bmi < 18.5:
  result = "Underweight"
elif bmi >= 18.5 and bmi <= 24.9:
  result = "Normal"
elif bmi >= 25 and bmi <= 29.9:
  result = "Overweight"
else:
  result = "Very overweight"
print(f"Hello {user_name}. Your BMI is {bmi}. Your body mass index is {result}.")
```

* You can download the file from my [GitHub](https://github.com/soumyajyotibiswas/ninja-adventures/blob/main/Code/Python/0000002_bmi_calculator.py) page.
