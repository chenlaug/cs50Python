from datetime import date, datetime
import inflect
import sys

def main():
    birth_str = input("Date of Birth (YYYY-MM-DD): ")
    birth_date = get_date(birth_str)
    minutes = get_minutes_since(birth_date)

    print(format_minutes_to_words(minutes))

def get_date(birth_str):
    try:
        return datetime.strptime(birth_str, "%Y-%m-%d").date()
    except ValueError:
        sys.exit("Invalid date format")

def get_minutes_since(birth_date):
    today = date.today()
    days_difference = (today - birth_date).days
    return round(days_difference * 24 * 60)

def format_minutes_to_words(minutes):
    p = inflect.engine()
    words = p.number_to_words(minutes, andword="")
    words = words[0].upper() + words[1:]
    return f"{words} minutes"



if __name__ == "__main__":
    main()
