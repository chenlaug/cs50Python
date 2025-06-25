import os
import sys
import csv

def main():
  try:
    rev, get = getArgv()
    openfile(rev, get)
  except ValueError as e:
    print(e)
    sys.exit(1)
  except FileNotFoundError as e:
    print(e)
    sys.exit(1)

def getArgv():
  if len(sys.argv) > 3:
    raise ValueError("Too many command-line arguments")
  elif len(sys.argv) < 2:
    raise ValueError("Too few command-line arguments")
  if not (sys.argv[1].endswith(".csv") and sys.argv[2].endswith(".csv")):
    raise ValueError("Not a CSV file")

  return sys.argv[1], sys.argv[2]

def openfile(fileName, newFile):
  if not os.path.exists(fileName):
    raise FileNotFoundError("Le Fichier CSV est introuvable")
  with open(fileName, 'r', newline='') as file:
    reader = csv.DictReader(file)
    fieldnames = ["first", "last", "house"]
    with open(newFile, 'w', newline='') as new_file:
            writer = csv.DictWriter(new_file, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                try:
                    last, first = row["name"].split(",")
                    house = row["house"]

                    first = first.strip()
                    last = last.strip()

                    writer.writerow({
                        "first": first,
                        "last": last,
                        "house": house
                    })
                except Exception as e:
                    print("Ligne ignorée (erreur de format) :", row)

if __name__ == "__main__":
    main()
