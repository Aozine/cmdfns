
import aioconsole
import re
import shlex
import sys
from typing import Any, Optional, Tuple

from cmdfns.command_cls import Command
from cmdfns.command_store import CommandStore
from cmdfns.invalid_argument import InvalidArgument


class CommandExecutor:
    """Handles execution of command functions."""

    _KEYWORD_ARG_REGEX = re.compile("([^ =]+)=(.+)")
    _store: CommandStore
    _exe_name: str

    def __init__(self, store: CommandStore, exe_name: Optional[str] = None):
        """Creates a CommandExecuter that looks for commands in the given
        store.

        Parameters
        ----------
        store : CommandStore
            The store to look for commands in.
        exe_name : Optional[str]
            Optional executable name to include in usage help, defaults to
            sys.argv[0].
        """
        self._store = store
        if exe_name:
            self._exe_name = exe_name
        else:
            self._exe_name = sys.argv[0]

    def execute_command_from_argv(self,
                                  argv: Optional[list[str]] = None) -> Any:
        """Execute a command from a list of command-line arguments.

        The first element of argv is assumed to be the Python script name and
        is ignored. The second element is treated as the command name.
        Subsequent elements are treated as command arguments.

        Parameters
        ----------
        argv : Optional[list[str]], optional
            Command-line argument list, if not specified then sys.argv is
            used.

        Returns
        -------
        Any
            The result of the command, if any.
        """
        if argv is None:
            argv = sys.argv
        if len(argv) < 2:
            self._print_usage(True)
            return
        self.execute_command_from_args(argv[1], argv[2:])

    def execute_command_from_args(self, command_name: str,
                                  args: list[str]) -> Any:
        """Execute a command given a command name and list of string
        arguments.

        Arguments are treated as positional arguments unless they are of the
        form "name=value", in which case they are treated as keyword
        arguments.

        If the command function is an async function then it is awaited.

        Parameters
        ----------
        command_name : str
            The name of the command to execute.
        args : list[str]
            A list of command arguments.

        Returns
        -------
        Any
            The result of the command, if any.
        """
        return self._execute_command_from_args(command_name, args, False)

    def execute_command_from_stdin(self):
        """Reads commands from stdin and executes them.

        Returns once the "quit" command has been executed.
        """
        while True:
            argv: list[str] = shlex.split(input("> "))
            command_name = argv[0]
            args = argv[1:]
            if command_name == "quit":
                return
            elif command_name == "help":
                self._print_help(args, True)
            else:
                self.execute_command_from_args(command_name, args)

    async def execute_command_from_argv_async(self,
                                              argv: Optional[list[str]] = None
                                              ) -> Any:
        """Execute a command from a list of command-line arguments.

        The first element of argv is assumed to be the Python script name and
        is ignored. The second element is treated as the command name.
        Subsequent elements are treated as command arguments.

        If the command function is an async function then it is awaited.

        Parameters
        ----------
        argv : Optional[list[str]], optional
            Command-line argument list, if not specified then sys.argv is
            used.

        Returns
        -------
        Any
            The result of the command, if any.
        """
        if argv is None:
            argv = sys.argv
        if len(argv) < 2:
            self._print_usage(False)
            return
        return await self.execute_command_from_args_async(argv[1], argv[2:])

    async def execute_command_from_args_async(self, command_name: str,
                                              args: list[str]) -> Any:
        """Execute a command given a command name and list of string
        arguments.

        Arguments are treated as positional arguments unless they are of the
        form "name=value", in which case they are treated as keyword
        arguments.

        If the command function is an async function then it is awaited.

        Parameters
        ----------
        command_name : str
            The name of the command to execute.
        args : list[str]
            A list of command arguments.

        Returns
        -------
        Any
            The result of the command, if any.
        """
        return await self._execute_command_from_args_async(
            command_name, args, False)

    async def execute_command_from_stdin_async(self):
        """Reads commands from stdin and executes them.

        If the command function is an async function then it is awaited.

        Returns once the "quit" command has been executed.
        """
        while True:
            line: str = await aioconsole.ainput("> ")
            argv: list[str] = shlex.split(line)
            command_name = argv[0]
            args = argv[1:]
            if command_name == "quit":
                return
            elif command_name == "help":
                self._print_help(args, True)
            else:
                await self._execute_command_from_args_async(
                    command_name, args, True)

    def _execute_command_from_args(self, command_name: str,
                                   args: list[str],
                                   interactive: bool) -> Any:
        if command_name == "help":
            self._print_help(args, interactive)
            return
        command: Optional[Command] = self._store.get_command(command_name)
        if not command:
            self._command_not_found(command_name, interactive)
            return
        positional_args, keyword_args = self._parse_args(args)
        try:
            return command.execute(positional_args, keyword_args)
        except InvalidArgument as e:
            print(str(e))

    async def _execute_command_from_args_async(self, command_name: str,
                                               args: list[str],
                                               interactive: bool) -> Any:
        if command_name == "help":
            self._print_help(args, interactive)
            return
        command: Optional[Command] = self._store.get_command(command_name)
        if not command:
            self._command_not_found(command_name, interactive)
            return
        positional_args, keyword_args = self._parse_args(args)
        try:
            return await command.execute_async(positional_args, keyword_args)
        except InvalidArgument as e:
            print(str(e))

    def _parse_args(self, args: list[str]) -> Tuple[list[str], dict[str, str]]:
        positional_args: list[str] = []
        keyword_args: dict[str, str] = {}
        for arg in args:
            match = self._KEYWORD_ARG_REGEX.match(arg)
            if match:
                keyword_args[match.group(1)] = match.group(2)
            else:
                positional_args.append(arg)
        return positional_args, keyword_args

    def _command_not_found(self, command_name: str, interactive: bool) -> None:
        print(f"Command '{command_name}' not found")
        print()
        self._print_usage(interactive)

    def _print_help(self, args: list[str], interactive: bool) -> None:
        if args:
            command_name = args[0]
            command: Optional[Command] = self._store.get_command(command_name)
            if not command:
                self._command_not_found(command_name, interactive)
                return
            self._print_command_help(command, interactive)
            return
        self._print_usage(interactive)

    def _print_command_help(self, command: Command, interactive: bool) -> None:
        print(f"Usage: {self._exe_name} {command.name} " +
              f"{command.args_string()}")
        if command.function.__doc__:
            print()
            print(command.function.__doc__)

    def _print_usage(self, interactive: bool) -> None:
        if interactive:
            print("Usage: > COMMAND [ARGS]")
        else:
            print(f"Usage: {self._exe_name} COMMAND [ARGS]")
        print()
        print("Where COMMAND is one of:")
        for command in self._store.get_commands():
            print(f"  {command.name}")
        print()
        if interactive:
            print("Use 'quit' to quit or 'help COMMAND' for " +
                  "command-specific help")
        else:
            print(f"Use '{self._exe_name} help COMMAND' for " +
                  "command-specific help")
