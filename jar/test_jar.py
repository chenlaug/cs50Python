from jar import Jar
import pytest

def test_init():
    jar = Jar()
    assert jar.size == 0
    assert jar.capacity == 12
    assert str(jar) == ""

def test_str():
    jar = Jar(size = 10)
    assert jar.size == 10
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"
    jar.deposit(1)
    assert jar.size == 11
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"
    jar.deposit(1)
    assert jar.size == 12
    assert str(jar) == "🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪🍪"
    jar.withdraw(11)
    assert jar.size == 1
    assert str(jar) == "🍪"

def test_deposit():
    jar = Jar(size = 10)
    jar.deposit(1)
    assert jar.size == 11

def test_withdraw():
    jar = Jar(size = 10)
    jar.withdraw(1)
    assert jar.size == 9

def test_negatif_capacity():
    with pytest.raises(ValueError):
      Jar(capacity = -1)

def test_tooSize_forCapacity():
    with pytest.raises(ValueError):
      Jar(size = 9, capacity = 8)

def test_withdraw_Error():
    jar = Jar(size = 2)
    with pytest.raises(ValueError):
      jar.withdraw(3)

def test_deposit_Error():
    jar = Jar(size = 2)
    with pytest.raises(ValueError):
      jar.deposit(11)
