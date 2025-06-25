from fuel import convert, gauge
import pytest

def test_convert_75():
  assert convert("3/4") == 75

def test_convert_25():
  assert convert("1/4") == 25

def test_convert_0():
  assert convert("0/4") == 0

def test_convert_100():
  assert convert("4/4") == 100

def test_convert_XMoreY():
  with pytest.raises(ValueError):
    convert("4/3")

def test_convert_Yis0():
  with pytest.raises(ZeroDivisionError):
    convert("4/0")

def test_gauge_75():
  assert gauge(75) == "75%"

def test_gauge_99():
  assert gauge(99) == "F"

def test_gauge_1():
  assert gauge(1) == "E"

def test_gauge_E():
  assert gauge(0) == "E"

def test_gauge_F():
  assert gauge(100) == "F"
