import sys
import requests

def main():
  value = getArgv()
  getBitcoin(value)

def getArgv():
  try:
    if len(sys.argv) > 2:
      raise IndexError ("Too many command-line arguments")
    if len(sys.argv) < 2:
      raise IndexError ("Missing command-line argument")

    value = float(sys.argv[1])
    return value

  except ValueError as e :
    print(e)
    sys.exit(1)
  except IndexError as e:
    print(e)
    sys.exit(1)


def getBitcoin(value):
  try:
    response = requests.get("https://rest.coincap.io/v3/assets/bitcoin?apiKey=0499ac79dc5722a4153ad9236471fc9373b91f4948b0899aced06282c6b1e19c")
    prixBtc = float(response.json()["data"]["priceUsd"])
    print(f"${value * prixBtc:,.4f}")
  except requests.RequestException as e:
    print(e)
    sys.exit(1)



main()

