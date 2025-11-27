import pytest

from app import add


def test_add_basic():
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(1.5, 2.5) == 4.0


def test_add_int_and_float():
    assert add(1, 2.5) == pytest.approx(3.5)
