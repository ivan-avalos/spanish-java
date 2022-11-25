
from errors import Error
from astree.unit import Unit
from parse.base import BaseParser
from parse.decl import ParseDecl

class ParseUnit:
    def __init__(self, parser: BaseParser):
        self.parser: BaseParser = parser

    def unit(self) -> (Unit | Error):
        decls = ParseDecl(self.parser).decls()
        if type(decls) is Error:
            return decls
        return Unit(decls = decls)
