import sys

from colorama import Fore, Style
from tabulate import tabulate

from Data.color_enum import Color
from Data.credential import Credential
from Data.password_manager import PasswordManager
from pyfiglet import Figlet

colors = {
    Color.RED: Fore.RED,
    Color.GREEN: Fore.GREEN,
    Color.BLUE: Fore.BLUE,
    Color.YELLOW: Fore.YELLOW,
    Color.CYAN: Fore.CYAN,
    Color.MAGENTA: Fore.MAGENTA
}


def main() -> None:
    figlet = Figlet()
    print(figlet.renderText("PyCryptBox !"))
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
    print(print_color("🛠️ 6. Update a credentials", Color.CYAN))
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
            return None
        case "2":
            print(print_color("Search for a credential", Color.BLUE))
            credential = pm.find_credential(input_color("Enter the site name: "))
            if isinstance(credential, Credential):
                print(print_color(f"Site: {credential.site} Username: {credential.username} Password: {credential.password}", Color.MAGENTA))
            else:
                print(print_color(credential, Color.RED))
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
            print_color("Update credentials...", Color.BLUE)
            site = input_color("Enter the site name: ")
            credential = pm.find_credential(site)

            if not isinstance(credential, Credential):
                print(print_color(credential, Color.RED))
                return None

            print(print_color(
                f"Current → Site: {credential.site}, Username: {credential.username}, Password: {pm.decrypt_password(credential.password)}",
                Color.MAGENTA))

            print(print_color("1. Site", Color.CYAN))
            print(print_color("2. Username", Color.CYAN))
            print(print_color("3. Password", Color.CYAN))
            print(print_color("4. All", Color.CYAN))

            while True:
                try:
                    choice = input_color("What would you like to change? (1/2/3/4): ")
                    if choice not in {"1", "2", "3", "4"}:
                        raise ValueError("Invalid choice. Please enter 1, 2, 3, or 4.")

                    new_values = {}
                    if choice == "1":
                        new_values["site"] = input_color("Enter new site: ")
                    elif choice == "2":
                        new_values["username"] = input_color("Enter new username: ")
                    elif choice == "3":
                        new_values["password"] = input_color("Enter new password: ")
                    elif choice == "4":
                        new_values["site"] = input_color("Enter new site: ")
                        new_values["username"] = input_color("Enter new username: ")
                        new_values["password"] = input_color("Enter new password: ")

                    result = pm.update_credential(site, choice, new_values)
                    print_color(result, Color.GREEN if "successfully" in result else Color.RED)
                    break

                except ValueError as e:
                    print_color(f"❌ Error: {e}", Color.RED)
        case "7":
            print(print_color(" See you soon !", Color.MAGENTA))
            pm.save()
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

def print_color(txt: str, color: Color) -> str:
    return f"{colors.get(color)}{txt}{Style.RESET_ALL}"

def input_color(txt: str, color: Color = Color.YELLOW) -> str:
    return input(f"{colors.get(color)}{txt}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
