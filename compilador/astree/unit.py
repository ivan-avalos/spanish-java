from dataclasses import dataclass
from typing import List

from astree.decl import Decl

# A single compilation unit, representing all of the members of a namespace.
@dataclass
class Unit:
    decls: List[Decl]
