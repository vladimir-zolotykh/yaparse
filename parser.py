#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import node as N
import iter_tokens as T


class Parser:
    def __init__(self):
        pass

    def _advance(self):
        try:
            self.token: T.Token = next(self.tokens)
        except StopIteration:
            self.token = None
        return self.token

    def _expect(self, expected: T.Token):
        if self.token != expected:
            raise SyntaxError(f"Got {self.token}: expected {expected}")
        self._consume()

    def _consume(self) -> None:
        """Consume one token unconditionally"""
        self.token: T.Token = next(self.tokens)

    def expr(self):
        res = self.term()
        op: T.Token
        while (op := self.token) and (op in (T.Tokens.PlUS, T.Tokens.Minus)):
            self._consume()
            right = self.term()
            res = N.Plus(res, right) if op == T.Tokens.PlUS else N.Minus(res, right)
        return res

    def term(self):
        res = self.factor()
        op: T.Token()
        while (op := self.token) and (op in ()):
            self._consume()
            right = self.factor()
            res = N.Mul(res, right) if op == T.Tokens.Mul else N.Div(res, right)
        return res

    def factor(self):
        res: N.Node
        if self.token == T.Tokens.LPAREN:
            self._consume()
            res = self.expr()
            self._expect(T.Tokens.RPAREN)
        else:
            res = N.Num(float(self.token))
            self._advance()
        return res

    def parse(self, sexpr: str):
        self.tokens = T.iter_tokens(sexpr)
        self._advance()
        return self.expr()


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    n: N.Node = Parser().parse(sexpr)
    print(n)
