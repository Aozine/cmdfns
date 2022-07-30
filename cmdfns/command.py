
from typing import Any, Callable


def command(fn_or_name: str | Callable[..., Any]) -> Callable[..., Any]:
    """Decorator for marking a function as a command that can be called from
    the command-line.

    Examples:

        @command
        def test_command():
            ...

        @command("a_custom_name")
        def another_test_command():
            ...

    Parameters
    ----------
    fn_or_name : str | Callable[..., Any]
        Optional custom command name, if not provided then the function
        name is used.

    Returns
    -------
    Callable[..., Any]
        The decorated function.
    """
    if isinstance(fn_or_name, Callable):
        fn_or_name._command = {"name": fn_or_name.__name__}  # type: ignore
        return fn_or_name
    else:
        def decorator_fn(fn: Callable[..., Any]) -> Callable[..., Any]:
            name: str = fn_or_name
            if name is None:
                name = fn.__name__
            fn._command = {"name": name}  # type: ignore
            return fn
        return decorator_fn
