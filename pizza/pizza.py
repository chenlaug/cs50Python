import os
import sys
from tabulate import tabulate
import csv

def main():
  try:
    arg = getArgv()
    print(CreateTable(arg))
  except ValueError as e:
    print(e)
    sys.exit(1)
  except FileNotFoundError as e:
    print(e)
    sys.exit(1)

def getArgv():
  if len(sys.argv) > 2:
    raise ValueError("Too many command-line arguments")
  elif len(sys.argv) < 2:
    raise ValueError("Too few command-line arguments")
  if not sys.argv[1].endswith(".csv"):
    raise ValueError("Not a CSV file")

  return sys.argv[1]

def CreateTable(fileName):
  if not os.path.exists(fileName):
    raise FileNotFoundError("Le Fichier CSV est introuvable")
  with open(fileName, newline="") as file:
    reader = csv.DictReader(file)
    data = list(reader)
    return tabulate(data, headers="keys", tablefmt="grid")

main()
