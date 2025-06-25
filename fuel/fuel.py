def main():
    while True:
        fraction = input("Fraction: ")
        try:
            percentage = convert(fraction)
            break
        except (ZeroDivisionError, ValueError):
            print("Try Again plz")

    print(f"{gauge(percentage)}")


def convert(fraction):
    x, y = map(int, fraction.strip().split("/"))

    if y == 0:
        raise ZeroDivisionError(f"{y} must not be zero.")

    if x > y:
        raise ValueError(f"{x} must not be greater than {y}.")

    return round((x / y) * 100)


def gauge(percentage):
    if percentage >= 99:
        return "F"
    elif percentage <= 1:
        return "E"
    return f"{percentage}%"


if __name__ == "__main__":
    main()
