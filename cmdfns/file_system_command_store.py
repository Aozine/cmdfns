
import glob
from importlib.machinery import SourceFileLoader
from inspect import getmembers, isfunction
import json
import os
from types import ModuleType
from typing import Any, Callable, Optional

from cmdfns.command_cls import Command
from cmdfns.command_store import CommandStore


class FileSystemCommandStore(CommandStore):
    """Loads commands from Python files in the file system."""

    _search_path: str
    _index_path: Optional[str]
    _command_cache: dict[str, Command]
    _command_index: dict[str, str]

    def __init__(self, search_path: str, index_path: Optional[str] = None):
        """Create a CommandStore that looks for commands in the file system
        under the given search path.

        The store will search recursively for all Python files under
        search_path, then look for functions within them that have the
        @command decorator.

        If index_path is specified then it is used to write out an index
        file which is then loaded on subsequent runs to speed up command
        look-up.

        Parameters
        ----------
        search_path : str
            The path to search for Python files containing command functions.
        index_path : Optional[str], optional
            The path to write an index file to for speeding up subsequent
            command look-ups.
        """
        self._search_path = search_path
        self._index_path = index_path
        self._command_cache = {}
        self._command_index = {}

    def get_command(self, name: str) -> Optional[Command]:
        """Queries a command from the store.

        Parameters
        ----------
        name : str
            The name of the command to return.

        Returns
        -------
        Optional[Command]
            The command or None if not found.
        """
        command: Optional[Command] = self._find_command_from_cache(name)
        if not command:
            command = self._find_command_from_index(name)
        if not command:
            command = self._find_command_from_search_path(name)
        return command

    def get_commands(self) -> list[Command]:
        """Returns a list of all commands from the store.

        Returns
        -------
        list[Command]
            List of commands from the store.
        """
        self._populate_cache_from_search_path()
        return list(self._command_cache.values())

    def _find_command_from_cache(self, command_name: str) \
            -> Optional[Command]:
        return self._command_cache.get(command_name)

    def _find_command_from_index(self, command_name: str) \
            -> Optional[Command]:
        if not self._command_index:
            self._command_index = self._load_command_index()
        command_python_file = self._command_index.get(command_name)
        if not command_python_file or not os.path.exists(command_python_file):
            return None
        try:
            self._command_cache.update(
                self._load_commands_from_python_file(command_python_file))
        except Exception:
            pass
        return self._command_cache.get(command_name)

    def _find_command_from_search_path(self, command_name: str
                                       ) -> Optional[Command]:
        self._populate_cache_from_search_path()
        return self._command_cache.get(command_name)
    
    def _populate_cache_from_search_path(self) -> None:
        self._command_cache = self._find_commands_in_search_path()
        self._save_command_index()

    def _save_command_index(self) -> None:
        if self._index_path is None:
            return
        with open(self._index_path, 'w') as file:
            json.dump(
                {command.name: command.path
                    for command in self._command_cache.values()}, file)

    def _load_command_index(self) -> dict[str, str]:
        if self._index_path is None or not os.path.exists(self._index_path):
            return {}
        try:
            with open(self._index_path, 'r') as file:
                return json.load(file)
        except Exception:
            return {}

    def _find_commands_in_search_path(self) -> dict[str, Command]:
        commands: dict[str, Command] = {}
        python_files = self._find_python_files_in_search_path()
        for python_file in python_files:
            commands.update(self._load_commands_from_python_file(python_file))
        return commands

    def _load_commands_from_python_file(self, path: str) \
            -> dict[str, Command]:
        commands: dict[str, Command] = {}
        module = self._import_python_file(path)
        for (name, fn) in self._find_commands_in_module(module).items():
            commands[name] = Command(name, path, fn)
        return commands

    def _find_commands_in_module(self, module: ModuleType) \
            -> dict[str, Callable[..., Any]]:
        commands: dict[str, Callable[..., Any]] = {}
        for (_, member_obj) in getmembers(module):
            if isfunction(member_obj) and hasattr(member_obj, "_command"):
                command_name: str = member_obj._command["name"]  # type: ignore
                commands[command_name] = member_obj
        return commands

    def _import_python_file(self, path: str) -> ModuleType:
        return SourceFileLoader(
            self._python_file_path_to_module_name(path),
            path).load_module()

    def _python_file_path_to_module_name(self, path: str) -> str:
        filename: str = os.path.basename(path)
        if filename.endswith(".py"):
            filename = filename[:-3]
        return filename

    def _find_python_files_in_search_path(self) -> list[str]:
        python_files: list[str] = []
        for filename in glob.iglob(os.path.join(self._search_path, "**/*.py"),
                                   recursive=True):
            python_files.append(filename)
        return python_files
