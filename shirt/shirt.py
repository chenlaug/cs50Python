import sys
import os
from PIL import Image, ImageOps

def main():
  try:
    input,output=getArgv()
    openFile(input,output)
  except ValueError as e:
    print(e)
    sys.exit(1)
  except FileNotFoundError as e:
    print(e)
    sys.exit(1)


def getArgv():
  valid_extension = (".jpg", ".jpeg", ".png")
  if len(sys.argv) != 3:
    ValueError("Usage: python shirt.py input_image output_image")

  input_file = sys.argv[1]
  output_file = sys.argv[2]

  if not sys.argv[1].endswith(valid_extension):
    raise ValueError("Invalid input file extension")
  elif not sys.argv[2].endswith(valid_extension):
    raise ValueError("Invalid output file extension")

  input_ext = os.path.splitext(input_file)[1].lower()
  output_ext = os.path.splitext(output_file)[1].lower()

  if input_ext != output_ext:
    raise ValueError("Input and output have different extensions")
  return input_file, output_file

def openFile(input_file, output_file):
  Imageshirt = "shirt.png"
  if not os.path.exists(input_file):
    raise FileNotFoundError("Image backgound not found")
  if not os.path.exists(Imageshirt):
    raise FileNotFoundError("Image to paste not found")

  photo = Image.open(input_file)
  shirt = Image.open("shirt.png")
  resized = ImageOps.fit(photo, shirt.size)
  resized.paste(shirt, (0, 0), shirt)
  resized.save(output_file)

main()
