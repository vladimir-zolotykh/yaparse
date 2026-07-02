#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from dataclasses import dataclass, field


@dataclass
class Node:
    val: str | float


@dataclass
class Num(Node):
    def __repr__(self):
        return f"{self.__class__.__name__}({self.val})"


@dataclass
class BinOp(Node):
    left: Node | None = None
    right: Node | None = None


@dataclass
class Plus(BinOp):
    val: str = field(init=False, default="+")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left}, {self.right})"


@dataclass
class Minus(BinOp):
    pass


@dataclass
class Mul(BinOp):
    val: str = field(init=False, default="*")

    def __repr__(self):
        return f"{self.__class__.__name__}({self.left}, {self.right})"


@dataclass
class Div(BinOp):
    pass
