import sys

def main():
  try:
    fileName = getArgv()
    print(f"{openFile(fileName)}")
  except ValueError as e:
    print(e)
    sys.exit(1)

def getArgv():
  if len(sys.argv) < 2:
    raise ValueError("Too few command-line arguments")

  if len(sys.argv) > 2:
    raise ValueError("Too many command-line arguments")

  if not sys.argv[1].endswith(".py"):
     raise ValueError("Not a Python file")

  return sys.argv[1]

def openFile(nameFile):
  ligne_counter = 0
  with open(f"{nameFile}","r") as file:
    lines = file.readlines()
    for line in lines:
      line_strip = line.strip()
      if line_strip == "":
        continue
      if line_strip.startswith("#"):
        continue
      ligne_counter += 1
  return ligne_counter

main()
