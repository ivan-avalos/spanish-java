from typing import Optional

from type import Type
from ident import Ident
from expr import Expr

# A global declaration.
#
#     entero a = 0;
@dataclass
class DeclGlobal:
    ident: Ident
    _type: Type
    init: Optional[Expr]

# A function declaration.
#
#     vacio main() { ... }
@dataclass
class DeclFunc:
    ident: Ident
    prototype: Type
    body: Optional[Expr]

# A Javañol declaration
Decl = DeclGlobal | DeclFunc
