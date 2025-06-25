from seasons import get_date, get_minutes_since, format_minutes_to_words
from datetime import date

def test_get_date():
    assert get_date("2000-06-30") == date(2000, 6, 30)

def test_get_minutes_since():
    dob = date(2000, 1, 1)
    today = date(2025, 1, 1)
    minutes = get_minutes_since(dob)
    assert isinstance(minutes, int)
    assert minutes > 0

def test_format_minutes_to_words():
    assert format_minutes_to_words(13137120) == "Thirteen million, one hundred thirty-seven thousand, one hundred twenty minutes"
