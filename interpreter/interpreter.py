expression = input("Expression: ")
a,z,e = expression.split()
a = float(a)
e = float(e)
if z == "+":
  print(a + e)
elif z == "-":
  print(a - e)
elif z == "*":
  print(a * e)
elif z == "/":
  if e != 0.0:
    print(a/e)
  else:
    print("U can division by zero")
