
from typing import Any, Callable, Optional

from cmdfns.command_cls import Command
from cmdfns.command_store import CommandStore


class DictCommandStore(CommandStore):
    """Returns commands from a dictionary."""

    _commands: dict[str, Command]

    def __init__(self, commands: dict[str, Callable[..., Any]]):
        """Create a CommandStore that returns command functions from the given
        dictionary.

        Parameters
        ----------
        commands : dict[str, Callable[..., Any]]
            Dictionary mapping command names to command functions.
        """
        self._commands = {}
        for name, function in commands.items():
            self._commands[name] = Command(name, name, function)

    def get_command(self, name: str) -> Optional[Command]:
        """Queries a command from the store.

        Parameters
        ----------
        name : str
            The name of the command to return.

        Returns
        -------
        Optional[_Command]
            The command or None if not found.
        """
        return self._commands.get(name)

    def get_commands(self) -> list[Command]:
        """Returns a list of all commands from the store.

        Returns
        -------
        list[Command]
            List of commands from the store.
        """
        return list(self._commands.values())
