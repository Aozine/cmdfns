
import os
from typing import Any, Optional

from cmdfns.command_executor import CommandExecutor
from cmdfns.file_system_command_store import FileSystemCommandStore

def main(search_path: str, index_path: Optional[str] = None) -> Any:
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
    if os.path.isfile(search_path):
        search_path = os.path.dirname(search_path)
    search_path = os.path.abspath(search_path)
    return CommandExecutor(
            FileSystemCommandStore(search_path, index_path)
        ).execute_command_from_argv()

