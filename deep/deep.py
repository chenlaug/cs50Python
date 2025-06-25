val = input("What is the Answer to the Great Question of Life, the Universe, and Everything? \n")
val = val.strip()
val = val.lower()

if(val != "42" and val != "forty-two" and val != "forty two"):
    print("No")
else:
  print("Yes")
