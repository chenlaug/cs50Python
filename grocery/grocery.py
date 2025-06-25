def main():
  newLists = {}
  try:
    while True:
      val = input().strip().upper()
      if newLists.get(f"{val}"):
        newLists[f"{val}"] += 1
      else:
        newLists[val] = 1

  except EOFError:
    pass

  for x,y in sorted(newLists.items()):
    print(f"{y} {x}")
  return

main()
