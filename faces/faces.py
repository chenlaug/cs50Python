val = input().strip()
if ":)" in val and ":(" in val:
  val = val.replace(":)","🙂")
  val = val.replace(":(","🙁")
  print(val)
elif ":)" in val:
  print(val.replace(":)","🙂"))
elif ":(" in val:
  print(val.replace(":(","🙁"))

