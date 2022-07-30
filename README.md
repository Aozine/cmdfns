cmdfns: make Python functions callable from the command-line
============================================================

`cmdfns` allows you to make Python functions callable from the command-line.
First, decorate any functions that you want to make callable with 
`cmdfns.command`, e.g.:

```
from cmdfns import command

@command
def say_hello():
    print("Hello, world")

@command
def say_goodbye():
    print("Goodbye, world")
```

Then define your program entrypoint (e.g. `main.py`) as follows:

```
import cmdfns
import os

if __name__ == "__main__":
    cmdfns.main(search_path=__file__)
```

You can then call the functions from the command-line as follows:

```
$ python main.py say_hello
Hello, world
$ python main.py say_goodbye
Goodbye, world
```

`cmdfns.main()` searches for command functions in Python files in the same
directory as the given `search_path` and recursively in all subdirectories.
Alternatively, you can pass in a custom path for it to search, e.g.:

```
import cmdfns
import os

if __name__ == "__main__":
    # Only search the "commands" subdirectory:
    cmdfns.main(search_path=os.path.join(os.path.dirname(__file__), "commands"))
```

If the named command is not found, or the special `help` command is used, then
usage information is printed to stdout:

```
$ python main.py help
Usage: main.py COMMAND [ARGS]

Where COMMAND is one of:
  say_goodbye
  say_hello

Use 'main.py help COMMAND' for command-specific help
```

Arguments can be passed to command functions either as positional arguments or
as keyword arguments of the form `name=value`, e.g.:

```
from cmdfns import command

@command
def greet(first_name, last_name):
    print(f"Hello, {first_name} {last_name}")
```

```
$ python main.py greet James Bond
Hello, James Bond
$ python main.py greet last_name=Bond first_name=James
Hello, James Bond
```

If a function has type hints then arguments of type `int`, `float` and `bool`
are automatically converted. For `bool` arguments, the strings `"True"`,
`"true"` and `"1"` are all converted to `True`, while `"False"`, `"false"` and
`"0"` are converted to `False`.

```
from cmdfns import command

@command
def print_types(a: int, b: float, c: bool):
    print(f"Argument types: {type(a)} {type(b)} {type(c)}")
```

```
$ python main.py 4 3.2 True
Argument types: <class 'int'> <class 'float'> <class 'bool'>
```

To call asynchronous functions as command functions, use `cmdfns.async_main()`
instead of `cmdfns.main()` as follows:

```
import asyncio
from cmdfns import command

@command
async def say_hello_after_delay():
    print("Hello, world")
```

```
import asyncio
import cmdfns

if __name__ == "__main__":
    asyncio.run(cmdfns.async_main())
```
