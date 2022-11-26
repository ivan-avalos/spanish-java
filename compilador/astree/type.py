import uuid
import graphviz as gv
from pprint import pformat
from dataclasses import dataclass
from typing import List
from enum import Enum

from astree.graphable import Graphable
from tabla import Token

Type = None

# A built-in primitive type (int, bool, str, etc).
class BuiltinType(Enum):
    BOOLEAN = Token.BOOLEAN
    STRING = Token.STRING
    CHAR = Token.CHAR
    INT = Token.INT
    VOID = Token.VOID

    def __str__(self):
        return self.value.value

# A parameter to a function type.
@dataclass
class FuncParam(Graphable):
    name: str
    _type: Type

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'FuncParam')
        dot.edge(parent, name, label = edge)
        name_name = uuid.uuid1().hex
        dot.node(name_name, self.name)
        dot.edge(name, name_name, 'name')
        name_type = uuid.uuid1().hex
        dot.node(name_type, str(self._type))
        dot.edge(name, name_type, 'type')

# funcion vacio ... (a: int, b: int ...)
@dataclass
class FuncType(Graphable):
    result: Type
    params: List[FuncParam]

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'FuncType')
        dot.edge(parent, name, label = edge)
        name_result = uuid.uuid1().hex
        dot.node(name_result, str(self.result))
        dot.edge(name, name_result, 'result')
        for p in self.params:
            p.graph(dot, name, 'param')

Type = BuiltinType
