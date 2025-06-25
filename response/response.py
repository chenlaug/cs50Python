import validators
def main():
  userEmail = input("What's your email address ? ")
  print(validateEmail(userEmail))

def validateEmail(email):
  if not validators.email(email):
    return "Invalid"
  return "Valid"

main()
