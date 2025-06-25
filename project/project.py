import sys

from colorama import Fore, Style
from tabulate import tabulate

from Data.color_enum import Color
from Data.credential import Credential
from Data.password_manager import PasswordManager

colors = {
    Color.RED: Fore.RED,
    Color.GREEN: Fore.GREEN,
    Color.BLUE: Fore.BLUE,
    Color.YELLOW: Fore.YELLOW,
    Color.CYAN: Fore.CYAN,
    Color.MAGENTA: Fore.MAGENTA
}


def main() -> None:
    print("Welcome to the PyCryptBox !")
    pm = generate_key_password_manager()

    while True:
        menu()
        try:
            use_menu(input_color("➡️ Enter a command: \n"), pm)
            print(print_color("...", Color.MAGENTA))
        except ValueError as e:
            print()
            print(print_color(f"❌ Error: {e}", Color.RED))
        except KeyboardInterrupt:
            print()
            print(print_color("❌ Interrupted by user, exiting...", Color.RED))
            sys.exit(1)
        except EOFError:
            print()
            print(print_color("❌ End of file reached, exiting...", Color.RED))
            sys.exit(1)

def menu() -> None:
    print(print_color("✅ 1. Add a credential", Color.CYAN))
    print(print_color("🔍 2. Search for a credential", Color.CYAN))
    print(print_color("🔍 3. Search for a credential with the true password", Color.CYAN))
    print(print_color("❌ 4. Delete a credential", Color.CYAN))
    print(print_color("📋 5. List all credentials", Color.CYAN))
    print(print_color("💾 6. Save", Color.CYAN))
    print(print_color("🚪 7. Exit", Color.CYAN))

def use_menu(command: str, pm: PasswordManager) -> None:
    match command.strip().lower():
        case "1":
            print(print_color("Add new credentials", Color.BLUE))
            pm.add_credential(
                site=input_color("Enter the site name: "),
                username=input_color("Enter the username: "),
                password=input_color("Enter the password: ")
            )
        case "2":
            print(print_color("Search for a credential", Color.BLUE))
            print(pm.find_credential(input_color("Enter the site name: ")))
        case "3":
            print(print_color("Search for a credential with the true password", Color.BLUE))
            print(pm.show_credential_with_true_password(input_color("Enter the site name: ")))
        case "4":
            print(print_color("Delete a credential", Color.RED))
            print(pm.delete_credential(input_color("Enter the site name: ")))
        case "5":
            print(print_color("List all credentials", Color.BLUE))
            show_credentials(pm)
        case "6":
            print(print_color("Saving credentials...", Color.BLUE))
            pm.save()
        case "7":
            print(print_color(" See you soon !", Color.MAGENTA))
            sys.exit(1)
        case _:
            raise ValueError("❗ Unknown command, please try again.")

def show_credentials(pm: PasswordManager) -> None:
    credentials = pm.list_credentials()
    if credentials:
        data = [[c.site, c.username, c.password] for c in credentials]
        headers = ["Site", "Username", "Password"]
        print(tabulate(data, headers=headers, tablefmt="grid"))
    else:
        print(print_color("No credentials found.", Color.RED))


def generate_key_password_manager() -> PasswordManager:
    pm = PasswordManager()
    pm.generation_key()
    pm.load_key()
    pm.load()
    return pm

def print_color(txt: str | Credential, color: Color) -> str:
    return f"{colors.get(color)}{txt}{Style.RESET_ALL}"

def input_color(txt: str, color: Color = Color.YELLOW) -> str:
    return input(f"{colors.get(color)}{txt}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
