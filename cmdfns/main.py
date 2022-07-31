
import os
from typing import Any, Optional

from cmdfns.command_executor import CommandExecutor
from cmdfns.file_system_command_store import FileSystemCommandStore


def main(search_path: Optional[str] = None,
         index_path: Optional[str] = None) -> Any:
    """Executes the command function specified by sys.argv, returning any
    result.

    The command function whose name matches sys.argv[1] is executed, with any
    subsequent values passed as positional arguments, except for those of the
    format "name=value" which are passed as keyword arguments. If no command
    function is found with the given name then usage help is printed to
    stdout.

    If `search_path` is provided then this will search for functions decorated
    with `@cmdfns.command` in Python files in the same directory and
    recursively in any subdirectories of the given path.

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
    if search_path is not None:
        if os.path.isfile(search_path):
            search_path = os.path.dirname(search_path)
        search_path = os.path.abspath(search_path)
        return CommandExecutor(
                FileSystemCommandStore(search_path, index_path)
            ).execute_command_from_argv()
    else:
        raise Exception("No command functions provided, pass search_path")


def interactive_main(search_path: Optional[str] = None,
                     index_path: Optional[str] = None) -> None:
    """Interactively executes commands read from sys.stdin.

    Repeatedly reads commands from sys.stdin and executes them, with any
    values after each command name passed as positional arguments, except
    for those of the format "name=value" which are passed as keyword
    arguments. If no command function is found with the given name then usage
    help is printed to stdout. Terminates when the `quit` command is executed.

    If `search_path` is provided then this will search for functions decorated
    with `@cmdfns.command` in Python files in the same directory and
    recursively in any subdirectories of the given path.

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
    if search_path is not None:
        if os.path.isfile(search_path):
            search_path = os.path.dirname(search_path)
        search_path = os.path.abspath(search_path)
        CommandExecutor(
                FileSystemCommandStore(search_path, index_path)
            ).execute_command_from_stdin()
    else:
        raise Exception("No command functions provided, pass search_path")


async def async_main(search_path: Optional[str] = None,
                     index_path: Optional[str] = None) -> Any:
    """Searches for command functions under the given search path and executes
    the one named in sys.argv.

    This function searches recursively for all Python files under search_path
    containing functions with the @cmdfns.command decorator. It then executes
    the function whose name matches sys.argv[1] and returns any result.

    If no command function is found with the given name then usage help is
    printed to stdout.

    Subsequent values in sys.argv are passed as positional arguments, except
    for those of the format "name=value" which are passed as keyword
    arguments.

    If the command function is an async function then it is awaited.

    If index_path is specified then it is used to write out an index
    file which is then loaded on subsequent runs to speed up command
    look-up.

    Parameters
    ----------
    search_path : str
        The path to search for Python files containing command functions.
    index_path : Optional[str], optional
        The path to write an index file to for speeding up subsequent command
        look-ups.

    Returns
    -------
    Any
        The result of the command function, if any.
    """
    if search_path is not None:
        if os.path.isfile(search_path):
            search_path = os.path.dirname(search_path)
        search_path = os.path.abspath(search_path)
        return await CommandExecutor(
                FileSystemCommandStore(search_path, index_path)
            ).execute_command_from_argv_async()
    else:
        raise Exception("No command functions provided, pass search_path")


async def async_interactive_main(search_path: Optional[str] = None,
                                 index_path: Optional[str] = None) -> None:
    """Interactively executes commands read from sys.stdin.

    Repeatedly reads commands from sys.stdin and executes them, with any
    values after each command name passed as positional arguments, except
    for those of the format "name=value" which are passed as keyword
    arguments. If no command function is found with the given name then usage
    help is printed to stdout. Terminates when the `quit` command is executed.

    If `search_path` is provided then this will search for functions decorated
    with `@cmdfns.command` in Python files in the same directory and
    recursively in any subdirectories of the given path.

    Any command functions that are async functions are awaited.

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
    if search_path is not None:
        if os.path.isfile(search_path):
            search_path = os.path.dirname(search_path)
        search_path = os.path.abspath(search_path)
        await CommandExecutor(
                FileSystemCommandStore(search_path, index_path)
            ).execute_command_from_stdin_async()
    else:
        raise Exception("No command functions provided, pass search_path")
