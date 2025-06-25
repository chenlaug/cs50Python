def main():
  month = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]
  while True:
    try:
        val = input("Date: ").strip()
        val = val.split()

        if len(val) == 1:
          date = val[0]
          m,d,y = date.split("/")
          if not(m.isnumeric() and d.isnumeric() and y.isnumeric()):
            raise TypeError(f"{m} or {d} or {y} c'est pas des int")
          m = int(m)
          d = int(d)
          y = int(y)

          if m > 12:
            raise TypeError(f"{m} est plus grand que 12")
          elif d > 31:
            raise TypeError(f"{d} est plus grand que 31")

          else:
            print(f"{y}-{m:02}-{d:02}")
            break

        elif len(val) == 3:
          m,d,y = val

          if m.isnumeric():
            raise TypeError(f"{m} est un int est non un sting")

          if month.index(m):
            for t in range(len(month)):
              if month[t] == m:
                m = t+1
          else:
            raise TypeError(f"{m} N'est pas dans la liste")

          if not "," in d:
            raise TypeError("Error")
          else:
            d = int(d.replace(",",""))

          if d > 31:
            raise TypeError(f"{d} est plus grand que 31")

          print(f"{y}-{int(m):02}-{int(d):02}")
          break

    except TypeError as e:
          print(e)
          continue
    except EOFError:
      pass


main()
