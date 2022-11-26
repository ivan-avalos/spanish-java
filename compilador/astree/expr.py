import uuid
import graphviz as gv
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional

from astree.graphable import Graphable
from astree.type import Type
from astree.ident import Ident

Expr = None

# An identifier access expression.
#
#     a
@dataclass
class AccessIdentifier(Graphable):
    ident: Ident

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, self.ident)
        dot.edge(parent, name, label = edge)

# An access expression.
AccessExpr = AccessIdentifier

# An assignment expression.
#
#     a = 10
@dataclass
class AssignExpr(Graphable):
    _object: AccessExpr
    value: Expr

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'AssignExpr')
        dot.edge(parent, name, label = edge)
        self._object.graph(dot, name, 'object')
        if isinstance(self.value, Graphable):
            self.value.graph(dot, name, 'value')

# A binary arithmetic operator.
class BinarithmOp(Enum):
    BAND = '&'
    BOR = '|'
    DIV = '/'
    GT = '>'
    GTEQ = '>='
    LAND = '&&'
    LEQUAL = '=='
    LESS = '<'
    LESSEQ = '<='
    LOR = '||'
    MINUS = '-'
    NEQUAL = '!='
    PLUS = '+'
    TIMES = '*'

# A binary arithmetic expression.
#
#     a * b
@dataclass
class BinarithmExpr(Graphable):
    op: BinarithmOp
    lvalue: Expr
    rvalue: Expr

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'BinarithmExpr')
        dot.edge(parent, name, label = edge)
        name_op = uuid.uuid1().hex
        dot.node(name_op, self.op.value)
        dot.edge(name, name_op, 'op')
        if isinstance(self.lvalue, Graphable):
            self.lvalue.graph(dot, name, 'lvalue')
        if isinstance(self.rvalue, Graphable):
            self.rvalue.graph(dot, name, 'rvalue')

# A break expression.
#
#     detener
@dataclass
class BreakExpr(Graphable):
    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'BreakExpr')
        dot.edge(parent, name, label = edge)

# A function call expression.
#
#     foo(bar)
@dataclass
class CallExpr(Graphable):
    lvalue: Expr
    args: List[Expr]

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'CallExpr')
        dot.edge(parent, name, label = edge)
        if isinstance(self.lvalue, Graphable):
            self.lvalue.graph(dot, name, 'lvalue')
        for a in self.args:
            if isinstance(a, Graphable):
                a.graph(dot, name, 'arg')

# A compound expression.
#
#     {
#         foo;
#         bar;
#         // ...
#     }
@dataclass
class CompoundExpr(Graphable):
    exprs: List[Expr]

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'CompoundExpr')
        dot.edge(parent, name, label = edge)
        for e in self.exprs:
            if isinstance(e, Graphable):
                e.graph(dot, name, 'expr')

# A continue expression.
#
#     continuar
@dataclass
class ContinueExpr(Graphable):
    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'ContinueExpr')
        dot.edge(parent, name, label = edge)

# A scalar value.
@dataclass
class Value(Graphable):
    value: bool | str | int

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, str(self.value))
        dot.edge(parent, name, label = edge)

# An integer constant.
@dataclass
class NumberConstant(Graphable):
    value: int

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, str(self.value))
        dot.edge(parent, name, label = edge)

# A constant expression.
ConstantExpr = Value | NumberConstant

# An if or if..else expression.
#
#    si (a) { } sino { }
@dataclass
class IfExpr(Graphable):
    cond: Expr
    tbranch: Expr
    fbranch: Optional[Expr]

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'IfExpr')
        dot.edge(parent, name, label = edge)
        if isinstance(self.cond, Graphable):
            self.cond.graph(dot, name, 'cond')
        if isinstance(self.tbranch, Graphable):
            self.tbranch.graph(dot, name, 'tbranch')
        if self.fbranch and isinstance(self.fbranch, Graphable):
            self.fbranch.graph(dot, name, 'fbranch')

# A print statement.
#
#     imprimir a
@dataclass
class PrintExpr(Graphable):
    expr: Expr

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'PrintExpr')
        dot.edge(parent, name, label = edge)
        if isinstance(self.expr, Graphable):
            self.expr.graph(dot, name, 'expr')

# A read statement.
#
#     leer a
@dataclass
class ReadExpr(Graphable):
    expr: AccessExpr

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'ReadExpr')
        dot.edge(parent, name, label = edge)
        self.expr.graph(dot, name, 'expr')

# A return statement.
#
#     retorna a
@dataclass
class ReturnExpr(Graphable):
    expr: Optional[Expr]

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'ReturnExpr')
        dot.edge(parent, name, label = edge)
        if self.expr and isinstance(self.expr, Graphable):
            self.expr.graph(dot, name, 'expr')

# A while expression.
#
#     mientras (cond) { }
@dataclass
class WhileExpr(Graphable):
    cond: Expr
    body: Expr

    def graph(self, dot: gv.Digraph, parent: str = None, edge: str = None) -> None:
        name = uuid.uuid1().hex
        dot.node(name, 'WhileExpr')
        dot.edge(parent, name, label = edge)
        if isinstance(self.cond, Graphable):
            self.cond.graph(dot, name, 'cond')
        if isinstance(self.body, Graphable):
            self.body.graph(dot, name, 'body')

# A Javañol expression.
Expr = (AccessExpr | AssignExpr | BinarithmExpr | BreakExpr |
        CallExpr | ConstantExpr | ContinueExpr | IfExpr |
        CompoundExpr | PrintExpr | ReadExpr | ReturnExpr)
