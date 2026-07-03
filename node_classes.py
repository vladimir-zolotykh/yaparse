#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK


class Node:
    def __init__(self, val: str | float):
        self.val = val


class Num(Node):
    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.val == other.val
        else:
            return False

    def __repr__(self):
        return f"{type(self).__name__}({self.val})"


class BinOp(Node):
    def __init__(self, left, right):
        super().__init__(
            {"Plus": "+", "Minus": "-", "Mul": "*", "Div": "/"}[type(self).__name__]
        )
        self.left = left
        self.right = right

    def __repr__(self):
        return f"{type(self).__name__}({self.left}, {self.right})"


class Plus(BinOp):
    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.left == other.left and self.right == other.right
        else:
            return False


class Minus(BinOp):
    pass


class Mul(BinOp):
    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return self.left == other.left and self.right == other.right
        else:
            return False


class Div(BinOp):
    pass
