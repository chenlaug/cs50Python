fileName = input("File name: ").lower().strip()

def endNameFile(a):
  return fileName.endswith(f"{a}")

if endNameFile(".gif"):
  print("image/gif")
elif endNameFile(".jpg"):
  print("image/jpeg")
elif endNameFile(".jpeg"):
  print("image/jpeg")
elif endNameFile(".png"):
  print("image/png")
elif endNameFile(".png"):
  print("application/pdf")
elif endNameFile(".txt"):
  print("text/plain")
elif endNameFile(".zip"):
  print("application/zip")
elif endNameFile(".bin"):
  print("application/octet-stream")
elif endNameFile(".pdf"):
  print("application/pdf")

else:
  print("application/octet-stream")
