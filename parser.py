#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator, cast
import node as N
import iter_tokens as T


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
        while (op := self.token) and (op in (T.Tokens.PLUS, T.Tokens.MINUS)):
            self._consume()
            right = self.term()
            res = N.Plus(res, right) if op == T.Tokens.PLUS else N.Minus(res, right)
        return res

    def term(self) -> N.Node:
        res = self.factor()
        # op: T.Token
        while (op := self.token) and (op in (T.Tokens.MUL, T.Tokens.DIV)):
            self._consume()
            right = self.factor()
            res = N.Mul(res, right) if op == T.Tokens.MUL else N.Div(res, right)
        return res

    def factor(self) -> N.Node:
        res: N.Node
        if self.token == T.Tokens.LPAREN:
            self._consume()
            res = self.expr()
            self._expect(cast(T.Token, T.Tokens.RPAREN))
        else:
            assert self.token and isinstance(self.token.val, float)
            res = N.Num(float(self.token.val))
            self._advance()
        return res

    def parse(self, sexpr: str) -> N.Node:
        self.tokens = T.iter_tokens(sexpr)
        self._advance()
        return self.expr()


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    n: N.Node = Parser().parse(sexpr)
    print(n)
