foods = [
  {"name":"apple","calories":"130"},
  {"name":"avocado","calories":"50"},
  {"name":"sweet cherries","calories":"100"},
  {"name":"kiwifruit","calories":"90"},
  {"name":"pear","calories":"100"}
]




def main():
  val = input("Item: ").strip().lower()
  findCalorie(val)

def findCalorie(name):
  for food in foods:
    if food.get("name") == f"{name}":
      print(f"Calories: {food.get("calories")}")
    else:
      print("")

main()
