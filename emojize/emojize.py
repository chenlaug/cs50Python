import emoji as em

def main():
  val = input("Input: ").strip()
  print(em.emojize(f"{val}",language="alias"))

main()
