#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import TypeVar, Generic
from dataclasses import dataclass
import re

TokenType = TypeVar("TokenType")


@dataclass
class Token(Generic[TokenType]):
    pat: str
    name: str = ""
    val: TokenType | None = None


class TokenNs(type):
    def __new__(mcls, clsname, bases, clsdict):
        for name, val in clsdict.items():
            if isinstance(val, Token):
                val.name = name
        return super().__new__(mcls, clsname, bases, clsdict)

    def __iter__(cls):
        for name, tok in cls.__dict__.items():
            if isinstance(tok, Token):
                yield tok


class Tokens(metaclass=TokenNs):
    NAME = Token(r"[a-zA-Z_][a-zA-Z_0-9]*")
    NUM = Token(r"\d+")


def iter_tokens(sexpr: str = ""):
    for tok in Tokens:
        print(tok)


if __name__ == "__main__":
    iter_tokens()
    print(Tokens.NAME.name)
