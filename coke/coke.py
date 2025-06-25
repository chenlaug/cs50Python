def main():
  amount = 50
  coinInsert = 0

  while coinInsert <= 50:
    print(f"Amount Due: {amount}")
    coin = int(input("Insert Coin: "))
    if verifCoin(coin):
      amount -= coin
      coinInsert += coin
    if coinInsert >= 50:
      print(f"Change Owed: {coinInsert-50}")
      break

def verifCoin(c):
  match c:
    case 50:
      return True
    case 25:
      return True
    case 10:
      return True
    case 5:
      return True
    case _:
      return False

main()
