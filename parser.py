#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator, cast
import node_classes as N
import iter_tokens as T

PLUS = T.Tokens.PLUS
MINUS = T.Tokens.MINUS
MUL = T.Tokens.MUL
DIV = T.Tokens.DIV


class Parser:
    def __init__(self):
        self.token: T.Token | None = cast(T.Token, T.Tokens.WS)
        self.tokens: Iterator[T.Token] = iter(())

    def _advance(self):
        try:
            self.token = next(self.tokens)
        except StopIteration:
            self.token = None
        return self.token

    def _expect(self, expected: T.Token) -> None:
        if self.token != expected:
            raise SyntaxError(f"Got {self.token}: expected {expected}")
        self._consume()

    def _consume(self) -> None:
        """Consume one token unconditionally"""
        self.token = next(self.tokens)

    def expr(self) -> N.Node:
        res = self.term()
        # op: T.Token
        while (op := self.token) and (op in (PLUS, MINUS)):
            self._consume()
            right = self.term()
            res = N.Plus(res, right) if op == PLUS else N.Minus(res, right)
        return res

    def term(self) -> N.Node:
        res = self.factor()
        # op: T.Token
        while (op := self.token) and (op in (MUL, DIV)):
            self._consume()
            right = self.factor()
            res = N.Mul(res, right) if op == MUL else N.Div(res, right)
        return res

    def factor(self) -> N.Node:
        res: N.Node
        if self.token == T.Tokens.LPAREN:
            self._consume()
            res = self.expr()
            self._expect(cast(T.Token, T.Tokens.RPAREN))
        else:
            assert self.token
            # res = N.Num(float(self.token.val))
            res = N.Num(cast(float, self.token.val))
            self._advance()
        return res

    def parse(self, sexpr: str) -> N.Node:
        self.tokens = T.iter_tokens(sexpr)
        self._advance()
        # return self.expr()
        return N.Plus(N.Plus(N.Num(2), N.Mul(N.Num(3), N.Num(4))), N.Num(5))


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    n: N.Node = Parser().parse(sexpr)
    n2 = N.Plus(N.Plus(N.Num(2), N.Mul(N.Num(3), N.Num(4))), N.Num(5))
    assert n == n2
