from typing import NoReturn, Optional, cast

from tabla import Token, LexToken
from parse.base import BaseParser
from parse.ident import ParseIdent
from errors import Error
from astree.expr import Expr, BinarithmOp, ConstantExpr, NumberConstant, CallExpr, PrintExpr, BinarithmExpr, CompoundExpr, ReadExpr, AccessExpr, AssignExpr

class ParseExpr:
    def __init__(self, parser: BaseParser):
        self.parser = parser

    def expr(self) -> (Expr | Error):
        obj = self.binarithm(None, 0)

        # =
        tok = self.parser._try(Token.EQUAL)
        if not tok:
            return obj

        error = self.parser.synassert(
            isinstance(obj, AccessExpr),
            "Se esperaba un objeto como destino de la asignación.")
        if type(error) is Error:
            return error

        # Expresión
        expr = self.expr()
        if type(expr) is Error:
            return expr

        return AssignExpr(_object = obj,
                          value = expr)
        
    # WIP
    def binarithm(self, lvalue: Expr, i: int) -> (Expr | Error):
        print(f'binarithm({lvalue}, {i})')
        _lvalue = lvalue
        if not lvalue:
            _lvalue = self.cast(lvalue)
            if type(_lvalue) is Error:
                return _lvalue
        print(f'lvalue = {_lvalue}')
        
        tok = self.parser.lex()
        print(f'tok = {tok}')
        j: int = self.precedence(tok.tipo)
        while j >= i:
            op = self.binop_for_tok(tok.tipo)

            rvalue = self.cast(_lvalue)
            if type(rvalue) is Error:
                return rvalue

            tok = self.parser.lex()
            k: int = self.precedence(tok.tipo)
            while k > j:
                self.parser.unlex()
                rvalue = self.binarithm(rvalue, k)
                if type(rvalue) is Error:
                    return rvalue
                tok = self.parser.lex()
                
                k = self.precedence(tok.tipo)

            _lvalue = BinarithmExpr(op = op,
                                    lvalue = _lvalue,
                                    rvalue = rvalue)
            
            j = self.precedence(tok.tipo)

        self.parser.unlex()
        return _lvalue

    def call(self, lvalue: Expr) -> (Expr | Error):
        args: List[Expr] = []

        while not self.parser._try(Token.R_PAREN):
            # Expresión
            expr = self.expr()
            if type(expr) is Error:
                return epr

            args.append(expr)

            # ,
            if self.parser._try(Token.COMMA):
                continue

            # )
            if self.parser._try(Token.R_PAREN):
                break

        return CallExpr(lvalue = lvalue,
                        args = args)

    def compound_expr(self) -> (Expr | Error):
        items: List[Expr] = []

        # {
        lbracket = self.parser.want(Token.L_BRACKET)
        if type(lbracket) is Error:
            return lbracket

        while True:
            # }
            item = self.parser.peek(Token.R_BRACKET)
            if item: break
            
            item = self.expr()
            if type(item) is Error:
                return item
            
            items.append(item)

            # ;
            semicolon = self.parser.want(Token.SEMICOLON)
            if type(semicolon) is Error:
                return semicolon

        # }
        rbracket = self.parser.want(Token.R_BRACKET)
        if type(rbracket) is Error:
            return rbracket

        return CompoundExpr(exprs = items)

    def builtin(self) -> (Expr | Error):
        tok: LexToken = self.parser.peek(Token.PRINT, Token.READ)
        if not tok:
            return self.postfix(None)

        if tok.tipo == Token.PRINT:
            return self.print_expr()
        elif tok.tipo == Token.READ:
            return self.read_expr()
            
    def postfix(self, lvalue: Optional[Expr]) -> (Expr | Error):
        _lvalue: Optional[Expr] = lvalue
        if not lvalue:
            _lvalue = self.plain_expression()
            if type(_lvalue) == Error:
                return _lvalue

        tok: LexToken = self.parser._try(Token.L_PAREN)
        if not tok:
            return _lvalue

        _next: Optional[LexToken] = None
        if tok == Token.L_PAREN:
            return self.call(_lvalue)

        return self.postfix(_next)

    def print_expr(self) -> (Expr | Error):
        _print = self.parser.want(Token.PRINT)
        if type(_print) is Error:
            return _print

        lparen = self.parser.want(Token.L_PAREN)
        if type(lparen) is Error:
            return lparen

        expr = self.expr()
        if type(expr) is Error:
            return expr

        rparen = self.parser.want(Token.R_PAREN)
        if type(rparen) is Error:
            return rparen

        return PrintExpr(expr = expr)

    def read_expr(self) -> (Expr | Error):
        _read = self.parser.want(Token.READ)
        if type(_read) is Error:
            return _read

        ident = ParseIdent(self.parser).ident()
        if type(ident) is Error:
            return ident
        
        return ReadExpr(expr = ident)

    # WIP
    def cast(self, lvalue: Optional[Expr]) -> (Expr | Error):
        return self.unarithm()

    # WIP
    def constant(self) -> (Expr | Error):
        tok: LexToken = self.parser.lex()
        expr: Optional[ConstantExpr] = None
        if tok.tipo == Token.STRING_LIT:
            expr: str = tok.valor
        elif tok.tipo == Token.INT_LIT:
            expr = NumberConstant(value = tok.valor)
        elif tok.tipo == Token.BOOLEAN_LIT:
            expr: bool = tok.valor
        else:
            return Error(msg = "Se esperaba una constante.", numlinea = tok.numlinea)
        return expr

    # WIP
    def plain_expression(self) -> (Expr | Error):
        tok: LexToken = self.parser.peek()
        if tok.tipo in [Token.BOOLEAN_LIT, Token.CHAR_LIT, Token.INT_LIT, Token.STRING_LIT]:
            return self.constant()
        elif tok.tipo == Token.L_PAREN:
            lparen = self.parser.want(Token.L_PAREN)
            if type(lparen) is Error:
                return lparen
            expr = self.expr()
            if type(expr) is Error:
                return expr
            rparen = self.parser.want(Token.R_PAREN)
            if type(rparen) is Error:
                return rparen
            return expr
        elif tok.tipo == Token.IDENT:
            ident = ParseIdent(self.parser).ident()
            if type(ident) is Error:
                return ident
            return ident

    def unarithm(self) -> (Expr | Error):
        return self.builtin()

    def binop_for_tok(self, tok: Token) -> (BinarithmOp | NoReturn):
        if tok is Token.SLASH:
            return BinarithmOp.DIV
        elif tok is Token.GT:
            return BinarithmOp.GT
        elif tok is Token.GEQ:
            return BinarithmOp.GTEQ
        elif tok is Token.EQEQ:
            return BinarithmOp.LEQUAL
        elif tok is Token.LT:
            return BinarithmOp.LESS
        elif tok is Token.LEQ:
            return BinarithmOp.LESSEQ
        elif tok is Token.MINUS:
            return BinarithmOp.MINUS
        elif tok is Token.NOTEQ:
            return BinarithmOp.NEQUAL
        elif tok is Token.PLUS:
            return BinarithmOp.PLUS
        elif tok is Token.TIMES:
            return BinarithmOp.TIMES

    def precedence(self, tok: Token) -> int:
        if tok in [Token.EQEQ, Token.NOTEQ]:
            return 0
        elif tok in [Token.PLUS, Token.MINUS]:
            return 1
        elif tok in [Token.TIMES, Token.SLASH]:
            return 2
        return -1
