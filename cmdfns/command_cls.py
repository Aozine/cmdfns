
from inspect import iscoroutinefunction, Signature, Parameter
from types import MappingProxyType
from typing import Any, Callable, Optional

from cmdfns.invalid_argument import InvalidArgument


class Command:
    """
    Holds information about a command function.
    """

    def __init__(self, name: str, path: str, function: Callable[..., Any]):
        self.name = name
        self.path = path
        self.function = function

    def execute(self, positional_args: list[str],
                keyword_args: dict[str, str]) -> Any:
        parameters: MappingProxyType[str, Parameter] = \
            Signature.from_callable(self.function).parameters
        positional_args = \
            self._convert_positional_args(positional_args, parameters)
        keyword_args = self._convert_keyword_args(keyword_args, parameters)
        return self.function(*positional_args, **keyword_args)

    async def execute_async(self, positional_args: list[str],
                            keyword_args: dict[str, str]) -> Any:
        parameters: MappingProxyType[str, Parameter] = \
            Signature.from_callable(self.function).parameters
        positional_args = \
            self._convert_positional_args(positional_args, parameters)
        keyword_args = self._convert_keyword_args(keyword_args, parameters)
        if iscoroutinefunction(self.function):
            return await self.function(*positional_args, **keyword_args)
        else:
            return self.function(*positional_args, **keyword_args)

    def args_string(self) -> str:
        parameters: MappingProxyType[str, Parameter] = \
            Signature.from_callable(self.function).parameters
        parameter_strs: list[str] = []
        for name, parameter in parameters.items():
            if parameter.default is Parameter.empty:
                parameter_strs.append(name.upper())
            else:
                parameter_strs.append(f"[{name.upper()}]")
        return " ".join(parameter_strs)

    def _convert_positional_args(self, args: list[str],
                                 parameters: MappingProxyType[str, Parameter]
                                 ) -> list[Any]:
        converted_args: list[Any] = []
        parameters_list: list[Parameter] = list(parameters.values())
        for i in range(len(args)):
            arg = args[i]
            if i < len(parameters_list):
                parameter: Parameter = parameters_list[i]
                converted_arg: Any = None
                try:
                    converted_arg = self._convert(
                        arg, parameter.annotation)
                except Exception:
                    raise InvalidArgument(
                        f"Cannot convert '{arg}' to " +
                        f"{parameter.annotation.__name__} for parameter " +
                        f"'{parameter.name}' of command '{self.name}'")
                converted_args.append(converted_arg)
            else:
                converted_args.append(arg)
        return converted_args

    def _convert_keyword_args(self, args: dict[str, str],
                              parameters: MappingProxyType[str, Parameter]
                              ) -> dict[str, Any]:
        converted_args: dict[str, Any] = {}
        for name, arg in args.items():
            parameter: Optional[Parameter] = parameters.get(name)
            if parameter is not None:
                converted_arg: Any = None
                try:
                    converted_arg = self._convert(
                        arg, parameter.annotation)
                except Exception:
                    raise InvalidArgument(
                        f"Cannot convert '{arg}' to " +
                        f"{parameter.annotation.__name__} for parameter " +
                        f"'{parameter.name}' of command '{self.name}'")
                converted_args[name] = converted_arg
            else:
                converted_args[name] = arg
        return converted_args

    def _convert(self, value_str: str, type: type):
        if type is int or type is Optional[int]:
            return int(value_str)
        elif type is float or type is Optional[float]:
            return float(value_str)
        elif type is bool or type is Optional[bool]:
            if value_str == 'True' or value_str == 'true' or \
                    value_str == '1':
                return True
            elif value_str == 'False' or value_str == 'false' or \
                    value_str == '0':
                return False
            else:
                raise Exception("Invalid bool value")
        elif type is str or type is Optional[str] or type is None:
            return value_str
        else:
            raise Exception(f"Unknown type '{type}'")
