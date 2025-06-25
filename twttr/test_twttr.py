from twttr import shorten

def test_shorten_laughan():
    assert shorten("laughan") == "lghn"

def test_shorten_twitter():
    assert shorten("twitter") == "twttr"

def test_shorten_capitalized():
    assert shorten("TWITTER") == "TWTTR"

def test_shorten_numbers():
    assert shorten("laughan2000") == "lghn2000"

def test_shorten_punctuation():
    assert shorten("Est ce que laughan est le plus beau des mecs ? oui !!!") == "st c q lghn st l pls b ds mcs ?  !!!"
