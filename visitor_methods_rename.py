#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import inspect
from parser import Parser
import node_classes as N


class MethodRename(type):
    def __new__(mcls, clsname, bases, clsdict):
        ns2 = dict(clsdict)
        for name, func in clsdict.items():
            if name[:2] == "__" and name[-2:] == "__":
                continue
            func_types = []
            mutate = clsdict.get("_mutate", False)
            if name == "visit" and mutate:
                sig = inspect.signature(func)
                # replace visit(self, n: N.Plus) with visit_Plus(self, N.Plus)
                for pname, parm in sig.parameters.items():
                    if pname == "self":
                        continue
                    if parm.annotation is inspect._empty:
                        raise TypeError(f"Annotate {pname}")
                    func_types.append(parm.annotation.__name__)
                new_visit_name = "visit_" + "_".join(func_types)
                ns2[new_visit_name] = func

        return super().__new__(mcls, clsname, bases, ns2)


class Visitor:
    _mutate = True

    def visit(self, n: N.Node) -> float:
        method_name = f"visit_{type(n).__name__}"
        func = getattr(self, method_name, self.visit_generic)
        return func(n)


class Evalutor(Visitor, metaclass=MethodRename):
    def visit(self, n: N.Num) -> float:
        return n.val

    def visit(self, n: N.Plus) -> float:
        return self.visit(n.left) + self.visit(n.right)

    def visit(self, n: N.Mul) -> float:
        return self.visit(n.left) * self.visit(n.right)


if __name__ == "__main__":
    sexpr = "2 + (3 * 4) + 5"
    n: N.Node = Parser().parse(sexpr)
    print(Evalutor().visit(n))
