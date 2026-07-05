#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import MutableMapping, Any
from types import MethodType
import inspect
import pytest
from parser import Parser
import node_bare as N


class MultiMethod:
    def __init__(self, name):
        self._name = name
        self.methods = {}

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return MethodType(self, instance)

    def register(self, func):
        sig = inspect.signature(func)
        types = tuple(p.annotation for k, p in sig.parameters.items() if k != "self")
        self.methods[types] = func

    def __call__(self, *args):
        types = tuple(type(a) for a in args[1:])
        return self.methods[types](*args)


class MultiDict(dict):
    def __setitem__(self, key, val):
        if key[:2] == "__" and key[-2:] == "__":
            super().__setitem__(key, val)
            return
        if key not in self:
            super().__setitem__(key, val)
            return
        oval = self[key]
        if isinstance(oval, MultiMethod):
            mm = oval
            mm.register(val)
            super().__setitem__(key, mm)
        else:
            mm = MultiMethod(key)
            mm.register(oval)
            mm.register(val)
            super().__setitem__(key, mm)


class MultiMeta(type):
    @classmethod
    def __prepare__(
        mcls, clsname: str, bases: tuple[type, ...], /, **kwds: Any
    ) -> MutableMapping[str, object]:
        return MultiDict()


class Evalutor(metaclass=MultiMeta):
    _mutate = True

    def visit(self, n: N.Num) -> float:
        return n.val

    def visit(self, n: N.Plus) -> float:  # noqa: F811
        return self.visit(n.left) + self.visit(n.right)

    def visit(self, n: N.Minus) -> float:  # noqa: F811
        return self.visit(n.left) - self.visit(n.right)

    def visit(self, n: N.Mul) -> float:  # noqa: F811
        return self.visit(n.left) * self.visit(n.right)

    def visit(self, n: N.Div) -> float:  # noqa: F811
        return self.visit(n.left) / self.visit(n.right)


@pytest.mark.parametrize(
    "sexpr, expected",
    [
        ("2 + (3 * 4) + 5", 19.0),
        ("18 / (3 * 2)", 3.0),
        ("(2 + 3) * 4", 20.0),
    ],
)
def test_evaluator(sexpr, expected):
    n = Parser().parse(sexpr)
    assert Evalutor().visit(n) == expected


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    n: N.Node = Parser().parse(sexpr)
    print(Evalutor().visit(n))
