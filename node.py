#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from dataclasses import dataclass


@dataclass
class Node:
    val: str | float


@dataclass
class Num(Node):
    pass


@dataclass
class BinOp(Node):
    left: Node | None = None
    right: Node | None = None


@dataclass
class Plus(BinOp):
    pass


@dataclass
class Minus(BinOp):
    pass


@dataclass
class Mul(BinOp):
    pass


@dataclass
class Div(BinOp):
    pass
