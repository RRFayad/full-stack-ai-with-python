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
