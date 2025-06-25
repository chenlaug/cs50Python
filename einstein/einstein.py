def calcul(M):
  M = int(M)
  c = pow(300000000,2)
  return M * c

def main():
  val = input("m: ").strip()
  E = calcul(val)
  print(E)

main()
