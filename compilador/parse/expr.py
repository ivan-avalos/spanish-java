#!/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2022  Iván Alejandro Ávalos Díaz <avalos@disroot.org>
#                     Edgar Alexis López Martínez <edgarmlmp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import NoReturn, Optional, cast

from tabla import Token, LexToken
from parse.base import BaseParser
from parse.ident import ParseIdent
from errors import Error
from astree.expr import *

class ParseExpr:
    def __init__(self, parser: BaseParser):
        self.parser = parser

    def expr(self) -> (Expr | Error):
        obj = None
        tok = self.parser.peek(Token.IF, Token.BREAK, Token.CONTINUE,
                               Token.RETURN, Token.WHILE)
        if not tok:
            obj = self.binarithm(None, 0)
        elif tok.tipo == Token.IF:
            obj = self.if_expr()
        elif tok.tipo in [Token.BREAK, Token.CONTINUE, Token.RETURN]:
            obj = self.control()
        elif tok.tipo == Token.WHILE:
            obj = self.while_expr()

        if type(obj) is Error:
            return obj

        # =
        tok = self.parser._try(Token.EQUAL)
        if not tok:
            return obj

        error = self.parser.synassert(
            isinstance(obj, AccessExpr),
            "Se esperaba un objeto como destino de la asignación.",
            numlinea = tok.numlinea)
        if type(error) is Error:
            return error

        # Expresión
        expr = self.expr()
        if type(expr) is Error:
            return expr

        return AssignExpr(_object = obj,
                          value = expr)
        
    def binarithm(self, lvalue: Expr, i: int) -> (Expr | Error):
        _lvalue = lvalue
        if not lvalue:
            _lvalue = self.cast(lvalue)
            if type(_lvalue) is Error:
                return _lvalue
        
        tok = self.parser.lex()
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
                return expr

            args.append(expr)

            # ,
            if self.parser._try(Token.COMMA):
                continue

            # )
            if self.parser._try(Token.R_PAREN):
                break

        return CallExpr(lvalue = lvalue,
                        args = args)

    def cast(self, lvalue: Optional[Expr]) -> (Expr | Error):
        return self.unarithm()

    def compound_expr(self) -> (Expr | Error):
        items: List[Expr] = []

        # {
        lbracket = self.parser.want(Token.L_BRACKET)
        if type(lbracket) is Error:
            return lbracket

        while not self.parser.peek(Token.R_BRACKET):
            # Expresión
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

    def constant(self) -> (Expr | Error):
        tok: LexToken = self.parser.lex()
        expr: Optional[ConstantExpr] = None
        if tok.tipo in [Token.STRING_LIT, Token.BOOLEAN_LIT]:
            expr = Value(value = tok.valor)
        elif tok.tipo == Token.INT_LIT:
            expr = NumberConstant(value = tok.valor)
        else:
            return Error(msg = "Se esperaba una constante.", numlinea = tok.numlinea)
        return expr

    def control(self) -> (Expr | Error):
        tok = self.parser.want(Token.BREAK, Token.CONTINUE, Token.RETURN)
        if type(tok) is Error:
            return tok

        expr = None
        if tok.tipo == Token.BREAK:
            expr = BreakExpr()
        elif tok.tipo == Token.CONTINUE:
            expr = ContinueExpr()
        elif tok.tipo == Token.RETURN:
            tok = self.parser.peek(Token.COMMA, Token.SEMICOLON, Token.EOF)
            if not tok:
                _expr = self.expr()
                if type(_expr) is Error:
                    return _expr
                expr = ReturnExpr(expr = _expr)
            else:
                expr = ReturnExpr(expr = None)

        return expr

    def builtin(self) -> (Expr | Error):
        tok: LexToken = self.parser.peek(Token.PRINT, Token.READ)
        if not tok:
            return self.postfix(None)

        if tok.tipo == Token.PRINT:
            return self.print_expr()
        elif tok.tipo == Token.READ:
            return self.read_expr()

    def if_expr(self) -> (Expr | Error):
        # si
        _if = self.parser.want(Token.IF)
        if type(_if) is Error:
            return _if

        # (
        lparen = self.parser.want(Token.L_PAREN)
        if type(lparen) is Error:
            return lparen

        # Condición
        cond = self.expr()
        if type(cond) is Error:
            return cond

        # )
        rparen = self.parser.want(Token.R_PAREN)
        if type(rparen) is Error:
            return rparen

        # Verdadero
        tbranch = self.expr()
        if type(tbranch) is Error:
            return tbranch

        # Falso
        fbranch = None
        if self.parser._try(Token.ELSE):
            fbranch = self.expr()
            if type(fbranch) is Error:
                return fbranch

        return IfExpr(cond = cond,
                      tbranch = tbranch,
                      fbranch = fbranch)
            
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
        if tok.tipo == Token.L_PAREN:
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
        
        return ReadExpr(expr = AccessExpr(ident = ident))
    
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
            return AccessIdentifier(ident = ident)

    def unarithm(self) -> (Expr | Error):
        if self.parser._try(Token.L_BRACKET):
            self.parser.unlex()
            return self.compound_expr()
        return self.builtin()

    def while_expr(self) -> (Expr | Error):
        # mientras
        _while = self.parser.want(Token.WHILE)
        if type(_while) is Error:
            return _while

        # (
        lparen = self.parser.want(Token.L_PAREN)
        if type(lparen) is Error:
            return lparen

        # Condición
        cond = self.expr()
        if type(cond) is Error:
            return cond

        # )
        rparen = self.parser.want(Token.R_PAREN)
        if type(rparen) is Error:
            return rparen

        # Expresión
        body = self.expr()
        if type(body) is Error:
            return body
        
        return WhileExpr(cond = cond,
                         body = body)

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
        if tok == Token.OR:
            return 0
        elif tok == Token.AND:
            return 1
        elif tok in [Token.EQEQ, Token.NOTEQ]:
            return 2
        elif tok in [Token.LT, Token.LEQ, Token.GT, Token.GEQ]:
            return 3
        elif tok in [Token.PLUS, Token.MINUS]:
            return 4
        elif tok in [Token.TIMES, Token.SLASH]:
            return 5
        return -1
