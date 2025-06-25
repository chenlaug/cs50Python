def main():
  val = input("Input: ")
  print(shorten(val))

def shorten(vowels):
  shorten = ""

  for vowel in vowels:
    if not vowel.lower() in "aeiou":
      shorten += vowel

  return shorten

if __name__ == "__main__":
    main()
