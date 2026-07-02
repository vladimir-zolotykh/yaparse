#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import TypeVar, Generic, Iterator, cast
from dataclasses import dataclass
import re

TokenType = TypeVar("TokenType")


@dataclass
class Token(Generic[TokenType]):
    name: str
    pat: str
    val: TokenType | None = None

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self.name == other.name and self.val == other.val
        elif isinstance(other, str):
            return self.name == other
        else:
            return False


class TokenNs(type):
    def __new__(mcls, clsname, bases, clsdict):
        ns = dict(clsdict)
        for name, val in clsdict.items():
            if name[:2] == "__" and name[-2:] == "__":
                continue
            if isinstance(val, str):
                ns[name] = Token(name, f"(?P<{name}>{val})")
        return super().__new__(mcls, clsname, bases, ns)

    def __iter__(cls):
        for name, tok in cls.__dict__.items():
            if isinstance(tok, Token):
                yield name


class Tokens(metaclass=TokenNs):
    NAME = r"[a-zA-Z_][a-zA-Z_0-9]*"
    NUM = r"\d+"
    PLUS = r"\+"
    MINUS = r"-"
    MUL = r"\*"
    DIV = r"/"
    LPAREN = r"\("
    RPAREN = r"\)"
    WS = r"\s+"


def iter_tokens(sexpr: str = "2 + (3 * 4) + 5") -> Iterator[Token]:
    pat = "|".join(getattr(Tokens, name).pat for name in Tokens)
    for match in re.finditer(pat, sexpr):
        if match.lastgroup != "WS":
            tok: Token = getattr(Tokens, cast(str, match.lastgroup))
            tok.val = match.group(0)
            yield tok


if __name__ == "__main__":
    for tok in iter_tokens():
        print(tok)
