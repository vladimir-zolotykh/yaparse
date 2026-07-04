#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Node:
    def __init__(self, val: str | float):
        self.val = val

    def __eq__(self, other):
        return type(self) is type(other) and self.__dict__ == other.__dict__


class Num(Node):
    def __init__(self, val: str | float):
        super().__init__(float(val))

    def __repr__(self):
        return f"Num({self.val})"


class BinOp(Node):
    def __init__(self, left, right):
        super().__init__(
            {"Plus": "+", "Minus": "-", "Mul": "*", "Div": "/"}[type(self).__name__]
        )
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{type(self).__name__}({self.left!r}, {self.right!r})"


class Plus(BinOp):
    pass


class Minus(BinOp):
    pass


class Mul(BinOp):
    pass


class Div(BinOp):
    pass
