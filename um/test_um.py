from um import count

def test_count():
  assert count("Um, thanks, um...") == 2
  assert count("um?") == 1
  assert count("The moon hunt you") == 0
  assert count("um") == 1
  assert count("album") == 0
