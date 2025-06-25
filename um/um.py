import re
import sys


def main():
    print(count(input("Text: ")))
    sys.exit(1)


def count(s):
    pattern = r'\b(?:um)\b'
    nbMatch = len(re.findall(pattern,s, re.IGNORECASE))
    return nbMatch if nbMatch else 0

if __name__ == "__main__":
    main()
