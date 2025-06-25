import random

def main():
  operationNbr = 0
  good = 0
  level = get_level()
  while operationNbr != 10:
    x = generate_integer(level)
    y = generate_integer(level)
    calcul = int(input(f"{x} + {y} = ").strip())
    if calcul == x + y:
      good += 1
    else:
      fail = 1
      while fail < 3:
        print("EEE")
        calcul = int(input(f"{x} + {y} = ").strip())
        if calcul != x+y:
           fail += 1
        else:
           good += 1
           break
      else:
        print(x+y)

    operationNbr += 1

  else:
     print(good)


def get_level():
  while True:
    try:
      level = int(input("Level: ").strip())
      if level in [1,2,3]:
        return level
      else:
        print(f"Le level: {level} il y a que les levels 1, 2 et 3")
    except ValueError:
      print("EEE")

def generate_integer(level):
    match level:
      case 1:
          return random.randint(0, 9)
      case 2:
          return random.randint(10, 99)
      case 3:
            return random.randint(100, 999)

if __name__ == "__main__":
  main()
