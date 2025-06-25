import inflect
p = inflect.engine()

def main():
  count = 0
  names = []
  while True:
    try:
      name = input("Name: ").strip()
      count += 1
      names.append(name)

    except EOFError:
      print("")
      print("Adieu, adieu, to", p.join(names))
      break


main()
