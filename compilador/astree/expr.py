from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional

from astree.type import Type

Expr = None

# An assignment expression
#
#     a = 10
@dataclass
class AssignExpr:
    _object: Expr
    value: Expr

# A binary arithmetic operator
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
class BinarithmExpr:
    op: BinarithmOp
    lvalue: Expr
    rvalue: Expr

# A function call expression.
#
#     foo(bar)
@dataclass
class CallExpr:
    lvalue: Expr
    args: List[Expr]

# A compound expression.
#
#     {
#         foo;
#         bar;
#         // ...
#     }
@dataclass
class CompoundExpr:
    exprs: List[Expr]

# A scalar value.
Value = bool | str | int | type(None)

# An integer constant.
@dataclass
class NumberConstant:
    value: int

# A constant expression.
ConstantExpr = Value | NumberConstant

# A for loop.
#
#     porcada (entero a = 0; a < b; a++) {}
@dataclass
class ForExpr:
    bindings: Optional[Expr]
    cond: Expr
    afterthought: Optional[Expr]
    body: Expr

# An if or if..else expression.
#
#    si (a) { } sino { }
@dataclass
class IfExpr:
    cond: Expr
    tbranch: Expr
    fbranch: Optional[Expr]

# A print statement.
#
#     imprimir a
PrintExpr = Expr

# A read statement.
#
#     leer a
ReadExpr = Expr

# A return statement.
#
#     return a
ReturnExpr = Optional[Expr]

# A Javañol expression
Expr = (AssignExpr | BinarithmExpr | CallExpr | ConstantExpr |
        ForExpr | IfExpr | CompoundExpr | PrintExpr |
        ReadExpr | ReturnExpr)
