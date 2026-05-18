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

## Section 9 - OOP

- In python, when you instanciate an object from a class, you can see it in the object type
  - `print(type(ginger_tea) is Chai)`

- _Shadowing / attribute lookup:_ Specific behavior:
  - We were seeing `del` for deleting attributes from an object
    - If we delete an attribute, but a class attribute with the same name exists, Python falls back to it (otherwise, it will break the code)

- Methods:
  - **Instance methods** use `self` as the first parameter.
    - `self` refers to the current object/instance.
    - Python passes `self` automatically when calling `object.method()`.
  - **Class methods** (refers to the class itself) use `cls` as the first parameter and need `@classmethod`.
    - So if I change an attribute by this method, for example, it changes for the whole class, not only the opbject
  - **Static methods** use neither `self` nor `cls` and need `@staticmethod`

- `__init__(self, *args, **kwargs)`
  - `__init__` is used for initiating the object from a class - Its created automatically with `self` as arg
  - If need need more args for instanciation, I need to create a custom init method

- 4 Pilars of OOP
  - Abstraction
    - "Hide implementation and only show whats is necessary" - Basically creating the class
  - Encapsulation
    - Make some properties private
      - Like the `self.__arms_qty = 2` in our example
      - **Important:** So we need to create getters and setters to handle the private data
      - **Getters and Setters:**
        - Practical use: avoid changing important data directly and centralize the rules for reading/updating it

      ```python
      class BankAccount:
          def __init__(self, balance):
              self.__balance = balance

          @property
          def balance(self):
              return self.__balance

          @balance.setter
          def balance(self, value):
              if value < 0:
                  raise ValueError("Balance cannot be negative")
              self.__balance = value

      account = BankAccount(100)
      print(account.balance)  # getter

      account.balance = 150  # setter
      ```

  - Inheritance
    - Inheriting props from a higher hierarchycal class
      - `class Dog(Animal)`

    - `super()`
      - super() is about the parent class
      - e.g.: `super().__init__(eat, sleep)`

  - Polimorphism
    - Which is basically have different forms
      - So if we are creating a parent class Animal, each child class has `talk(self)` method, like bark, roar, etc, this is the concept of polymorphism

- Compositions
  - Creating classes using otther classes, being a **HAS-A** relationship
    - E.g.:

      ```python
      class Engine():
      def start(self):
      print("Engine started")

      class Motorcycle():
      def **init**(self):
      self.engine = Engine()

          def start(self):
              self.engine.start()
              print("Motorcycle started")
      ```

## Section 10 - Handling Exceptions

- We can write the `try` `except` definng the type of error, e.g.:

  ```python
    def process_order(item, quantity):
    try:
        #Code than can break
        raise TypeError("Quantity must be a number")    # I can raise an error would be raised automatically
    except KeyError:
        #Run if error (Key Error in this case)
    except:
        #Run if any error (Despite ot Key Error in this case)
    else:
        #Run if NO error
    finally:
        #Always run
  ```

- Customize exceptions

  ```python
    class OutOfIngredientsError(Exception):
    pass

    def make_chai(milk, sugar):
      if milk == 0 or sugar == 0:
          raise OutOfIngredientsError("Missing milk or sugar")
      print("chai is ready...")


    make_chai(0, 1)
  ```

- **with** operator:
  - with operator is a syntax for: `__enter()__` `__exit()__` and handle an exception
  ```python
    with open("order.txt", "w") as file:
      file.write("ginger tea - 4 cups")
  ```

## Section 11 - MultiThreading, Multiprocessing, GIL

- Concurrency
  - Basically, its the concept of dividing to task to be executed in chuncks at once
    - threading.Thread
      - [Threading example](./assets/python-udemy-main/12_threads_concurrency/01_threading.py)
        - In this example:
          i. the thread ensures the 2nd loading snippet runs whie the 1st is "loading" / sleeping;
          ii. `order_thread.start()` starts the thread
          iii. `order_thread.join()` stops the code running until this thread is finished
    - asyncio

- Parallelism
  - multiprocessing
    - [multiprocessing example](./assets/python-udemy-main/12_threads_concurrency/02_multiprocessing.py)
    - `concurrent.futures.ProcessPoolExecutor`

- GIL - Global Interpreter Lock
  - Threads in the same Python process share the same GIL.
  - Because of that, only one thread can execute Python bytecode at a time inside that process.
  - A new `Process` creates a separate Python interpreter.
  - Each process has its own GIL.
  - So multiprocessing can run CPU-heavy Python code truly in parallel across CPU cores.

- Lock
  - The lock is used to avoid race condition
  - In this case, 2 different loops could affect the global counter value at once - so lock avoids it

  ```python
    import threading

    counter = 0
    lock = threading.Lock()

    def increament():
        global counter
        for _ in range(100000):
            with lock:
                counter += 1

    threads = [threading.Thread(target=increament) for _ in range(10)]
    [t.start() for t in threads]
    [t.join() for t in threads]

    print(f"Final counter: {counter}")
  ```

- **Obs.:** Files 09 and 10 compares thread \* process (process was 2x faster)

- Sharing data between processes
  - Unlike threads, processes do not naturally share normal Python variables
  - For that, `multiprocessing` gives us special shared tools like `Queue` and `Value`

- `Queue`
  - Use `Queue` when one process needs to send data/messages to another process
  - Think of it as a safe pipe between processes
  - In [11_process_queue.py](./assets/python-udemy-main/12_threads_concurrency/11_process_queue.py):
    - the child process does `queue.put("Masala chai is ready")`
    - the main process reads it later with `queue.get()`
  - Best for:
    - passing results
    - sending tasks
    - communication between processes

- `Value`
  - Use `Value` when processes need to share one simple variable in memory
  - In [12_process_value.py](./assets/python-udemy-main/12_threads_concurrency/12_process_value.py):
    - `Value('i', 0)` creates one shared integer starting at `0`
    - each process increments the same `counter.value`
    - `with counter.get_lock():` prevents race conditions while updating it
  - Best for:
    - one shared number, flag, or small piece of state

- Rule of thumb
  - `Queue` = send data between processes
  - `Value` = share one small mutable value between processes

## Section 12 - Asyncio

- Like JS, `async` and `await`

- Problems to be solved:
  - Async makes it equally faster as using threds / processes
  - Main concepts:
    - `asyncio.gather`

- Asyncio is not a total substitution for multiprocessing or multithreading; they can be combined.
  - Example: [04_thread_async.py](./assets/python-udemy-main/13_async_python/04_thread_async.py)
  - In this example, `asyncio` keeps the async event loop free while `run_in_executor()` sends the blocking function to a separate thread.
  - This is useful when we have blocking code, like `time.sleep()` or a sync library, but still want to use it inside an async program.

- Daemon thread:
  - A background thread that does not block the program from exiting
  - If only daemon threads are left, Python exits
  - Useful for non-critical background tasks (avoid it for important work because it may stop before finishing)
