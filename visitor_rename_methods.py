#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import MutableMapping, Any
import inspect
import pytest
from parser import Parser
import node_bare as N


class MultiDict(dict):
    def __setitem__(self, key, val):
        if key[:2] == "__" and key[-2:] == "__":
            super().__setitem__(key, val)
        if key == "visit":
            sig = inspect.signature(val)
            func_types = []
            for name, parm in sig.parameters.items():
                if name == "self":
                    continue
                if parm.annotation is inspect._empty:
                    raise TypeError(f"Annotate {name}")
                func_types.append(parm.annotation.__name__)
            new_visit_name = "visit_" + "_".join(func_types)
            super().__setitem__(new_visit_name, val)


class RenameMeta(type):
    def visit(self, n: N.Node) -> float:
        depth = getattr(self, "_depth", 0)
        self.method_name = f"visit_{type(n).__name__}"
        print(f'{"  " * depth}{self.method_name}')
        func = getattr(self, self.method_name, self.visit_generic)
        try:
            self._depth = depth + 1
            res = func(n)
        finally:
            self._depth = depth
        print(f'{"  " * depth}->{res}')
        return res

    def visit_generic(self, n: N.Node) -> float:
        raise TypeError(f"{self.method_name} not found")

    def __new__(mcls, clsname, bases, ns):
        ns2 = dict(ns)
        ns2["visit"] = mcls.visit
        ns2["visit_generic"] = mcls.visit_generic
        return super().__new__(mcls, clsname, bases, ns2)

    @classmethod
    def __prepare__(
        mcls, clsname: str, bases: tuple[type, ...], /, **kwds: Any
    ) -> MutableMapping[str, object]:
        return MultiDict()


class Evalutor(metaclass=RenameMeta):
    def visit(self, n: N.Num) -> float:
        return n.val

    def visit(self, n: N.Plus) -> float:  # noqa: F811
        return self.visit(n.left) + self.visit(n.right)

    def visit(self, n: N.Minus) -> float:  # noqa: F811
        return self.visit(n.left) + self.visit(n.right)

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
