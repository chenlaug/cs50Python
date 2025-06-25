
def convert(time):
  hours, minutes = time.split(":")
  hours = int(hours)
  minutes= int(minutes)
  if int(minutes) > 60:
    return print("Error")
  minutes/= 60
  minutes = round(minutes,2)
  return hours + minutes

def main():
  UserHour = input("What time is it? ").lower().strip()
  time = convert(UserHour)
  if 7 <= time <= 8:
    print("breakfast time")
  if 12 <= time <= 13:
    print("lunch time")
  if 18 <= time <= 19:
    print("dinner time")

if __name__ == "__main__":
    main()

