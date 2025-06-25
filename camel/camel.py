def main():
  val = input("camelCase: ")
  return print("snake_case: " + toSnakeCase(val))

def toSnakeCase(V):
  newVal = ""
  for x in V:
    if x.isupper():
      newVal += "_" + x.lower()
    else:
      newVal += x
  return newVal

main()
