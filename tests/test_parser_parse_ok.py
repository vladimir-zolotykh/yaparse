import pytest

import parser as P
import node_bare as N


@pytest.mark.parametrize(
    "sexpr, expected",
    [
        ("2", N.Num(2)),
        ("2 + 3", N.Plus(N.Num(2), N.Num(3))),
        ("2 - 3", N.Minus(N.Num(2), N.Num(3))),
        ("2 * 3", N.Mul(N.Num(2), N.Num(3))),
        ("2 / 3", N.Div(N.Num(2), N.Num(3))),
        (
            "2 + 3 * 4",
            N.Plus(
                N.Num(2),
                N.Mul(N.Num(3), N.Num(4)),
            ),
        ),
        (
            "2 * 3 + 4",
            N.Plus(
                N.Mul(N.Num(2), N.Num(3)),
                N.Num(4),
            ),
        ),
        (
            "(2 + 3) * 4",
            N.Mul(
                N.Plus(N.Num(2), N.Num(3)),
                N.Num(4),
            ),
        ),
        (
            "2 + (3 * 4) + 5",
            N.Plus(
                N.Plus(
                    N.Num(2),
                    N.Mul(N.Num(3), N.Num(4)),
                ),
                N.Num(5),
            ),
        ),
        # ("((2))", N.Num(2)),
        (
            "2 - 3 - 4",
            N.Minus(
                N.Minus(N.Num(2), N.Num(3)),
                N.Num(4),
            ),
        ),
        (
            "2 / 3 / 4",
            N.Div(
                N.Div(N.Num(2), N.Num(3)),
                N.Num(4),
            ),
        ),
    ],
)
def test_parse_ok(sexpr, expected):
    assert P.Parser().parse(sexpr) == expected
