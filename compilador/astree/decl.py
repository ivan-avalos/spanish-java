from dataclasses import dataclass
from typing import Optional

from astree.type import Type
from astree.ident import Ident
from astree.expr import Expr

# A global declaration.
#
#     entero a = 0;
@dataclass
class DeclGlobal:
    ident: Ident
    _type: Type
    init: Expr

# A function declaration.
#
#     funcion vacio main() { ... }
@dataclass
class DeclFunc:
    ident: Ident
    prototype: Type
    body: Optional[Expr]

# A Javañol declaration
Decl = DeclGlobal | DeclFunc
