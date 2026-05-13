# full-stack-ai-with-python

### Intro Notes

- Virtual Env
  - `python3 venv .venv`
  - `.venv/bin/activate`
  - Usually we want to have a .txt requirements file

- PEP 8
  - Conventions for code formatting

  ## Section 3 - Data Types
  - Everything is a object, which its own id, type, and value

  - Mutable and Imutable
    - We can check if its mutable (referencing to the sma e object in memory by the `id()`)

- Numbers, Booleans and Operators
  - float, integer, compelx numbers
    - `//`gets only the integer of a division - `10 // 3` returns 3
    - `**` is powered of
    - For big numbers, python allow `1_000_000_000` for readability

- Strings
  - `[x:y:z]` - For strings, we use this for start, end (not including) and step
  - Also if the step is negative, it will reverse - example: `[::-1]` reverses the string

- Tuples (immutable lists)
  - ()

- Lists
  - []

- Sets
  - {}
  - `|` for union, `&` for getting the intersection and `-` for removing

- Dictionary
  - key value pairs

- Bytes and Bytearray
  - used to represent raw binary data — data stored as bytes, not normal text
  - might be used for pdf data, audio, etc

- Advanced Data Types
  - datetime, time, calendar
  - timedelta

## Section 4 - Conditionals in Python

- Some if, elif, else logic, with operators (and, or, not)
  - **Python ternary operator** `delivery_fees = 0 if order_amount > 300 else 30`

- Also we have the `match-case`:
  ```python
    match variable_name:
        case "x":
            print ("x")
        case "y":
            print ("y")
        case _:
            print ("z")
  ```

## Section 5 - Loops in Python

- for, while

- iterable functions:
  - range() - returns a iterable range
  - enumarate() - enumarates a list
  - zip() - zip combines 2 lists

- Inside loop:
  - `continue` (skip one)
  - `break` (finish loop)

- We can have an `else` for a `for` loop, for example:

  ```python
      staff = [("Amit", 16), ("Zara", 17), ("Raj", 15)]

      for name, age in staff:
          if age <= 18:
              print(f"{name} is eligible to manage the staff")
              break
      else:
          print(f"No one is eligible to manage the staff")
  ```

- Walrus Operator `:=`: It allows us to assign value to a variable inside an expression
  - `if (n := len(a)) > 10:` - Now we have the `n` value assigned (and as python does not scope inside a if block, its for the whole file)

## Section 6 - Functions in Python

- About Scopes:
  - We can manipulate scopes with `nonlocal` or `global` (e.g.: declaring a `global` variabel inside a function)

- Arg and Kwargs
  - In Python, functions arguments are not necessairly positional only, I can explicitly declare the keywords
    - e.g.: `make_chai(tea="Green", sugar="Medium", milk="No")` - with declared keywords, the order does not matter
  - **Important:**
    - Everytime I have `**` in the function args, they are keyargs, which mean I have to explicity delcare the key value
      - `def do_something(*args, **kwargs)`
    - ```python
        def special_chai(*ingredients, **extras):
          print("Ingredients", ingredients)
          print("Extras", extras)

        special_chai("Cinnamon", "Cardmom", sweetener="Honey", foam="yes")
      ```

    - In this example, `ingredients` is a _tuple_, while `extras` is a _dict_

- Multiple returns:

  ```python
    def chai_report():
      return 100, 20, 10 # sold, remaining

    sold, remaining, not_paid = chai_report()
  ```

  - **Obs:** If I do not destructure, its a list

- Types os functions
  - Pure vs Impure Functions
    - Pure: does not depend on a outer variable
    - We should always avoid impures

  - Recursive Functions
    - Function calls itself

  - Lambda Functions (Anonymous)
    - ```python
        strong_chai = list(filter(lambda chai: chai!="kadak", chai_types))
      ```

- Documenting Functions
  - If in the 1st line of the function, we add a comment with 3 ", we can access it later with _dunder_ docs
  - ```python
      def do_nothing():
          """This function does nothing"""
          return

      print (do_nothing.__doc__)  #Prints my description
    ```

## Section 7 - Comprehensions

- Comprehensions are basically sugar syntar for loops, using a single line of code (filtering, mapping, etc)
  - Are not only about DX, but also cleaner as faster code
  - Works for any iterable, like lists, sets, dictionaries and generators

- How it works:
  - `result = [expression for item in iterable if condition]`

    ```python
      fruits = ["apple", "banana", "orange", "avocado"]

      fruits_with_a_in_upper = [fruit.upper() for fruit in fruits if fruit[0].casefold() == "a"]
    ```

## Section 8 - Generators and Decorators

### Generators

- Generators are memory optimized, since it does not store each step, only gives us the final result
  - This is more memory efficient than having a list

    ```python
      # generator function
    def get_chai_gen():
      yield "Cup 1"
      yield "Cup 2"
      yield "Cup 3"

    print(next(chai))
    print(next(chai))
    print(next(chai))
    ```

  - Lets say I have a database of fahrenheit temperature, and I need to check the max in Celsius - given that I will never need the celsius full list anymore, I can use a generator

```python
  fahrenheit_temperatures = [70, 72, 75, 80, 90]

  celsius_temperatures = (
      (temp - 32) * 5 / 9
      for temp in fahrenheit_temperatures
  )

  max_celsius = max(celsius_temperatures)
```

- A more complex example, sending values:
  - Basically:
    - Next calls the generator;
    - Each time it runs, it pauses in the `yield` to receive a value (via `send()`)

```python
  def chai_customer():
    print("Welcome ! What chai would you like ?")
    order = yield
    while True:
        print(f"Preparing: {order}")
        order = yield

  stall = chai_customer()
  next(stall) # start the generator

  stall.send("Masala Chai")
  stall.send("Lemon Chai")
```

### Decorators

- Decorators are "on top" of something
  - It basically wraps a function to perform something else - like we could log that a specific process started, and tiem the duration after
  - **Obs.:** The `@wraps` serves to keep the original metaData (without iw, the name printed at the end would be `wrapper`, with it, its greet)

```python
from functools import wraps

def log_activity(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"🚀 Calling: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"✅ Finished: {func.__name__}")
        return result
    return wrapper

@log_activity
def brew_chai(type, milk="no"):
    print(f"Brewing {type} chai and milk status {milk}")

brew_chai("Masala")
```
