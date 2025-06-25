import sys
from pyfiglet import Figlet

figlet = Figlet()

def main():
    a = sys.argv[1:]
    if len(a) > 2 or len(a) == 1:
      sys.exit("Invalid usage")

    if not (a[0] == "-f" or a[0] == "--font"):
      sys.exit("Invalid usage")

    a[1] = a[1].lower()
    if a[1] in figlet.getFonts():
          figlet.setFont(font = a[1])
    else:
        sys.exit("Invalid usage")

    val = input("Input: ").strip()
    print(figlet.renderText(val))

main()
