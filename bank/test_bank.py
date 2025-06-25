from bank import value

def test_value_hello():
  assert value("Hello") == 0

def test_value_hey():
  assert value("Hey") == 20

def test_value_salut():
  assert value("Salut") == 100
