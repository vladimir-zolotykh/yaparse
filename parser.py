#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Iterator, cast
import pytest
import node_bare as N
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
        self.token = next(self.tokens, None)

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
            res = N.Num(float(str(self.token.val)))
            self._advance()
        return res

    def parse(self, sexpr: str) -> N.Node:
        self.tokens = T.iter_tokens(sexpr)
        self._advance()
        res = self.expr()
        if self.token is not None:
            raise SyntaxError(f"EOF expected, got {self.token}")
        return res


def test_plus_num2():
    n: N.Node = Parser().parse("2")
    assert n == N.Num(2)


def test_parse_paren_nested():
    sexpr = "((2))"
    expected = N.Num(2)
    assert Parser().parse(sexpr) == expected


@pytest.mark.parametrize(
    "sexpr",
    [
        "2 3",
        "2 + 3 4",
        "2 (3)",
        "(2) 3",
    ],
)
def test_trailing_garbage(sexpr):
    with pytest.raises(SyntaxError):
        Parser().parse(sexpr)


if __name__ == "__main__":
    sexpr = "2 + 3"
    n = Parser().parse(sexpr)
    print(n)  # Plus(Num(2), Num(3))

    sexpr = "2 + (3 * 4) + 5"
    n = Parser().parse(sexpr)
    print(n)  # Plus(Plus(Num(2), Mul(Num(3), Num(4))), Num(5))
