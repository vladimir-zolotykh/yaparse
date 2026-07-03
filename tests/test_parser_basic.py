import pytest
import parser as P
import node_classes as N


def test_parser_basic1():
    sexpr = "2 + (3 * 4) + 5"
    n: N.Node = P.Parser().parse(sexpr)
    expected: N.Node = N.Plus(
        N.Plus(N.Num(2.0), N.Mul(N.Num(3.0), N.Num(4.0))), N.Num(5.0)
    )
    assert n == expected


def test_parser_basic2():
    sexpr = "2"
    n = P.Parser().parse(sexpr)
    assert n == N.Num(2)
