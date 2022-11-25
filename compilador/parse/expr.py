from parse.base import BaseParser
from errors import Error
from astree.expr import Expr

class ParseExpr:
    def __init__(self, parser: BaseParser):
        self.parser = parser

    def expr(self) -> Expr | Error:
        next(self.parser.iterador)
        return
    
