def main():
    plate = input("Plate: ")
    if is_valid(plate):
        print("Valid")
    else:
        print("Invalid")


def is_valid(s):
    number_started = False
    if not s[0:2].isalpha():
        return False

    if not (2 <= len(s) <= 6):
        return False

    if not s.isalnum():
        return False

    for c in s:
        if c.isdigit():
            if not number_started:
                number_started = True
                if c == '0':
                    return False
        elif number_started:
            return False
    return True

if __name__ == "__main__":
    main()
