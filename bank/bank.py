def main():
  welcome = input("Welcome \n").strip();
  print(f"${value(welcome)}")

def value(greeting):
  greeting = greeting.lower()
  if greeting.startswith("hello"):
    return 0
  elif greeting[0] == "h":
    return 20
  else:
    return 100


if __name__ == "__main__":
    main()
