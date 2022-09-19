
import os
from typing import Any, Optional, Callable

from cmdfns.command_executor import CommandExecutor
from cmdfns.command_store import CommandStore
from cmdfns.dict_command_store import DictCommandStore
from cmdfns.file_system_command_store import FileSystemCommandStore


def main(search_path: Optional[str] = None,
         functions: Optional[dict[str, Callable[..., Any]]] = None,
         index_path: Optional[str] = None) -> Any:
    """Executes the command function specified by sys.argv, returning any
    result.

    The command function whose name matches sys.argv[1] is executed, with any
    subsequent values passed as positional arguments, except for those of the
    format "name=value" which are passed as keyword arguments. If no command
    function is found with the given name then usage help is printed to
    stdout.

    Exactly one of `search_path` or `functions` must be provided.

    If `search_path` is provided then this will search for functions decorated
    with `@cmdfns.command` in Python files in the same directory and
    recursively in any subdirectories of the given path.

    If `functions` is provided then it will be queried for command functions.

    If `index_path` is specified then it is used to write out an index
    file which is then loaded on subsequent runs to speed up command
    look-up.

    Parameters
    ----------
    search_path : Optional[str], optional
        The path to search for Python files containing command functions.
    index_path : Optional[str], optional
        The path to write an index file to for speeding up subsequent command
        look-ups.

    Returns
    -------
    Any
        The result of the command function, if any.
    """
    if search_path is not None and functions is not None or \
       search_path is None and functions is None:
        raise Exception("Exactly one of search_path or functions must be " +
                        "provided")
    command_store: CommandStore
    if search_path is not None:
        if os.path.isfile(search_path):
            search_path = os.path.dirname(search_path)
        search_path = os.path.abspath(search_path)
        command_store = FileSystemCommandStore(search_path, index_path)
    elif functions is not None:
        command_store = DictCommandStore(functions)
    else:
        raise Exception("Not implemented")
    return CommandExecutor(command_store).execute_command_from_argv()


def interactive_main(search_path: Optional[str] = None,
                     functions: Optional[dict[str, Callable[..., Any]]] = None,
                     index_path: Optional[str] = None,
                     exe_name: Optional[str] = None) -> None:
    """Interactively executes commands read from sys.stdin.

    Repeatedly reads commands from sys.stdin and executes them, with any
    values after each command name passed as positional arguments, except
    for those of the format "name=value" which are passed as keyword
    arguments. If no command function is found with the given name then usage
    help is printed to stdout. Terminates when the `quit` command is executed.

    Exactly one of `search_path` or `functions` must be provided.

    If `search_path` is provided then this will search for functions decorated
    with `@cmdfns.command` in Python files in the same directory and
    recursively in any subdirectories of the given path.

    If `functions` is provided then it will be queried for command functions.

    If `index_path` is specified then it is used to write out an index
    file which is then loaded on subsequent runs to speed up command
    look-up.

    Parameters
    ----------
    search_path : Optional[str], optional
        The path to search for Python files containing command functions.
    index_path : Optional[str], optional
        The path to write an index file to for speeding up subsequent command
        look-ups.
    exe_name : Optional[str], optional
        Optional executable name to use in help text (defaults to
        sys.argv[1]).
    """
    if search_path is not None and functions is not None or \
       search_path is None and functions is None:
        raise Exception("Exactly one of search_path or functions must be " +
                        "provided")
    command_store: CommandStore
    if search_path is not None:
        if os.path.isfile(search_path):
            search_path = os.path.dirname(search_path)
        search_path = os.path.abspath(search_path)
        command_store = FileSystemCommandStore(search_path, index_path)
    elif functions is not None:
        command_store = DictCommandStore(functions)
    else:
        raise Exception("Not implemented")
    return CommandExecutor(
        command_store, exe_name=exe_name).execute_command_from_stdin()


async def async_main(search_path: Optional[str] = None,
                     functions: Optional[dict[str, Callable[..., Any]]] = None,
                     index_path: Optional[str] = None,
                     exe_name: Optional[str] = None) -> Any:
    """Searches for command functions under the given search path and executes
    the one named in sys.argv.

    This function searches recursively for all Python files under search_path
    containing functions with the @cmdfns.command decorator. It then executes
    the function whose name matches sys.argv[1] and returns any result. If the
    command function is an async function then it is awaited.

    If no command function is found with the given name then usage help is
    printed to stdout.

    Subsequent values in sys.argv are passed as positional arguments, except
    for those of the format "name=value" which are passed as keyword
    arguments.

    Exactly one of `search_path` or `functions` must be provided.

    If `search_path` is provided then this will search for functions decorated
    with `@cmdfns.command` in Python files in the same directory and
    recursively in any subdirectories of the given path.

    If `functions` is provided then it will be queried for command functions.

    If `index_path` is specified then it is used to write out an index
    file which is then loaded on subsequent runs to speed up command
    look-up.

    Parameters
    ----------
    search_path : str
        The path to search for Python files containing command functions.
    index_path : Optional[str], optional
        The path to write an index file to for speeding up subsequent command
        look-ups.
    exe_name : Optional[str], optional
        Optional executable name to use in help text (defaults to
        sys.argv[1]).

    Returns
    -------
    Any
        The result of the command function, if any.
    """
    if search_path is not None and functions is not None or \
       search_path is None and functions is None:
        raise Exception("Exactly one of search_path or functions must be " +
                        "provided")
    command_store: CommandStore
    if search_path is not None:
        if os.path.isfile(search_path):
            search_path = os.path.dirname(search_path)
        search_path = os.path.abspath(search_path)
        command_store = FileSystemCommandStore(search_path, index_path)
    elif functions is not None:
        command_store = DictCommandStore(functions)
    else:
        raise Exception("Not implemented")
    return await CommandExecutor(
        command_store, exe_name=exe_name).execute_command_from_argv_async()


async def async_interactive_main(
        search_path: Optional[str] = None,
        functions: Optional[dict[str, Callable[..., Any]]] = None,
        index_path: Optional[str] = None) -> None:
    """Interactively executes commands read from sys.stdin.

    Repeatedly reads commands from sys.stdin and executes them, with any
    values after each command name passed as positional arguments, except
    for those of the format "name=value" which are passed as keyword
    arguments. If the command function is an async function then it is
    awaited. If no command function is found with the given name then usage
    help is printed to stdout. Terminates when the `quit` command is executed.

    Exactly one of `search_path` or `functions` must be provided.

    If `search_path` is provided then this will search for functions decorated
    with `@cmdfns.command` in Python files in the same directory and
    recursively in any subdirectories of the given path.

    If `functions` is provided then it will be queried for command functions.

    If `index_path` is specified then it is used to write out an index
    file which is then loaded on subsequent runs to speed up command
    look-up.

    Parameters
    ----------
    search_path : Optional[str], optional
        The path to search for Python files containing command functions.
    index_path : Optional[str], optional
        The path to write an index file to for speeding up subsequent command
        look-ups.
    """
    if search_path is not None and functions is not None or \
       search_path is None and functions is None:
        raise Exception("Exactly one of search_path or functions must be " +
                        "provided")
    command_store: CommandStore
    if search_path is not None:
        if os.path.isfile(search_path):
            search_path = os.path.dirname(search_path)
        search_path = os.path.abspath(search_path)
        command_store = FileSystemCommandStore(search_path, index_path)
    elif functions is not None:
        command_store = DictCommandStore(functions)
    else:
        raise Exception("Not implemented")
    return await CommandExecutor(
        command_store).execute_command_from_stdin_async()
