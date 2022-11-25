from dataclasses import dataclass
from typing import List
from enum import Enum

from tabla import Token

Type = None

# A built-in primitive type (int, bool, str, etc).
class BuiltinType(Enum):
    BOOLEAN = Token.BOOLEAN
    STRING = Token.STRING
    CHAR = Token.CHAR
    INT = Token.INT
    VOID = Token.VOID

# A parameter to a function type.
@dataclass
class FuncParam:
    name: str
    _type: Type

# funcion vacio ... (a: int, b: int ...)
@dataclass
class FuncType:
    result: Type
    params: List[FuncParam]

Type = BuiltinType
