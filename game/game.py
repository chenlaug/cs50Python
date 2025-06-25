import random
import sys
def main():
  into = False
  while True:
    try:

      if not into:
        level = int(input("Level: ").strip())
        trueNbr = random.randint(1, level)
        print(trueNbr)
        into = True

      guess = int(input("Guess: ").strip())

      if guess == trueNbr:
        print("Just right!")
        sys.exit()
      elif guess > trueNbr:
        print("Too large!")
      elif guess < trueNbr:
        print("Too small!")

    except EOFError:
      pass
    except ValueError:
      print("The value has wrong format")
      pass



main()
