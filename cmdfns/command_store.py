
from typing import Optional

from cmdfns.command_cls import Command


class CommandStore:
    """Interface for querying commands from a store."""

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
        raise Exception("Not implemented")

    def get_commands(self) -> list[Command]:
        """Returns a list of all commands from the store.

        Returns
        -------
        list[Command]
            List of commands from the store.
        """
        raise Exception("Not implemented")
