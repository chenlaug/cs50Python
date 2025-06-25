from working import convert
import pytest

def test_convert():
  assert convert("9:00 AM to 5:00 PM") == "09:00 to 17:00"
  assert convert("9 AM to 5 PM") == "09:00 to 17:00"
  assert convert("9:00 AM to 5 PM") == "09:00 to 17:00"
  assert convert("9 AM to 5:00 PM") == "09:00 to 17:00"
  assert convert("12 AM to 12 PM") == "00:00 to 12:00"
  assert convert("12 PM to 12 AM") == "12:00 to 00:00"

def test_invalid_time_format():
    with pytest.raises(ValueError):
        convert("25:00 AM to 5:00 PM")

def test_invalid_minutes():
    with pytest.raises(ValueError):
        convert("10:60 AM to 5:00 PM")

def test_missing_am_pm():
    with pytest.raises(ValueError):
        convert("9:00 to 17:00")

def test_bad_separator():
    with pytest.raises(ValueError):
        convert("9:00 AM - 5:00 PM")
